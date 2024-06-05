#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Name:        LXSerial.py
# Purpose:     Access to and use of LX200 Serial port
#
# Author(s):   R J Schumacher
#
# Created:     2006/01/28
# RCS-ID:      $Id: LXSerial.py $
# Copyright:   (c) 2006
# Licence:     LGPL
#
# -----------------------------------------------------------------------------

import serial
import sys
from LX200.LX200Error import LX200Error


class LXSerial:
    def __init__(self, model='LX200', debug=False):
        """Constructor.
        Arguments: serial port where the LX200 is connected
        Note:
        two ports can be opened on the LX200
        - access to the port settings trough Python properties
        - port numbering starts at zero, no need to know the platform dependant port
          name in the user program
        - port name can be specified if access through numbering is inappropriate

        if self.debug == True, port reads will return the last command chars,
        and no scope need be connected
        """
        self.model = model
        self.debug = debug
        self.connectedPort = None
        self.repr = "<LX200 serial port instance, unconnected>"

    def __repr__(self):
        """Return a representation string.
        """
        return self.repr

    # -------------------------------------------------------------------------------
    # com port utility methods
    # -------------------------------------------------------------------------------

    def CommandBlind(self, cmd, *args):
        """simply packages up command letters in #: # and sends to telescope"""
        arg = ''.join([str() for s in args])
        if self.debug:
            self.connectedPort.seek(0)
        try:
            self.connectedPort.write('#:%s%s#' % (cmd, str(arg)))
        except IOError as xxx_todo_changeme:
            (errno, strerror) = xxx_todo_changeme.args
            print "I/O error(%s): %s" % (errno, strerror)
        except ValueError:
            print "bad arg value", arg
        except BaseException:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        else:
            print "CommandBlind", cmd, args, "succeeded"
            return True

    def read_to_hash(self):
        """reads from port until hash encountered and returns """
        if self.debug:
            self.connectedPort.seek(1)
        resp = self.connectedPort.read(1)
        try:
            while resp[-1] != '#':
                resp += self.connectedPort.read(1)
        except IndexError as xxx_todo_changeme1:
            (errno, strerror) = xxx_todo_changeme1.args
            print "IndexError error(%s): %s" % (errno, strerror)

        return resp[:-1]

    def CommandString(self, cmd, *args):
        """issues a command to the telescope, and awaits a string response
        terminated by a '#'. returns string"""
        self.CommandBlind(cmd, *args)
        return self.read_to_hash()

    def CommandBool(self, cmd, *args):
        """issues command and checks for '0' or '1' response. returns true
        on success. no hash returned in response."""
        self.CommandBlind(cmd, *args)
        if self.debug:
            self.connectedPort.seek(0)
        resp = self.connectedPort.read(1)
        if resp == '1' or self.debug:
            return True
        else:
            return False

    def connect(self, port, baud=9600, ptimeout=10):
        """Opens the port and checks for a telescope
        - port can be int: [0,...], or alpha: "COMn"
        - ptimeout>240 recommended for LX200GPS using auto_align"""
        if self.debug:
            import StringIO
            # something with read/write
            self.connectedPort = StringIO.StringIO(':A#')
        else:
            if self.model == 'LX200GPS':
                ptimeout = 240  # rqrd for auto_align
            try:
                self.connectedPort = serial.Serial(
                    port=port,  # number of device, numbering starts at
                    # zero. If everything fails, the user
                    # can specify a device string, note
                    # that this isn't portable anymore
                    # if no port is specified an unconfigured
                    # and closed serial port object is created
                    baudrate=baud,  # baudrate
                    bytesize=serial.EIGHTBITS,  # number of databits
                    parity=serial.PARITY_NONE,  # enable parity checking
                    stopbits=serial.STOPBITS_ONE,  # number of stopbits
                    timeout=ptimeout,  # set a timeout value, None for waiting forever
                    xonxoff=0,  # no software flow control
                    rtscts=0,  # no RTS/CTS flow control
                    writeTimeout=3,  # set a timeout for writes
                    dsrdtr=None,  # None: use rtscts setting, dsrdtr override if true or false
                )
            except serial.SerialException as s:
                print 'serial execption:', s
                raise LX200Error(str(s))

        # Query of alignment mounting mode.
        # A If in AltAz Mode,L If in Land Mode,P If in Polar Mode
        try:
            self.connectedPort.write(chr(0x06))
        except BaseException:
            raise LX200Error("port write error:  %s" % (sys.exc_info()[0]))
        if self.debug:
            print "connectedPort:", self.connectedPort, "(debug)"
            self.connectedPort.seek(0)
        mode = self.connectedPort.read(1)
        if self.debug:
            print 'mode:', mode
        if mode not in ['A', 'L', 'P', chr(0x06)]:
            print 'mode error:', mode
            raise LX200Error, "Port " + str(self.connectedPort) + " doesn't appear to be connected to an LX200 port; read returned \"" + mode + "\""
            self.connectedPort.close()
            return False

        self.repr = repr(self.connectedPort)
        return True

    def close(self):
        """ close the com port """
        self.connectedPort.close()  # ?

    def scan_ports(self):
        """ check all com ports possible for LX connections"""
        portList = []
        for portNum in range(4):
            try:
                print 'trying', portNum
                self.connect(portNum)
                portList.append(portNum)
                self.connectedPort.close()
            except BaseException:
                # quit looking for more
                break
        return portList

    def set_baud_rate(self, baud):
        """ Set Baud Rate n, where n is an ASCII digit (1..9) with the following interpertation
        1 56.7K
        2 38.4K
        3 28.8K
        4 19.2K
        5 14.4K
        6 9600
        7 4800
        8 2400
        9 1200
        Returns:
        1 At the current baud rate and then changes to the new rate for further communication"""
        rateDict = {56.7: 1, 38.4: 2, 28.8: 3, 19.2: 4, 14.4: 5, 9600: 6,
                    4800: 7, 2400: 8, 1200: 9}
        if baud in [1, 10]:
            res = self.CommandBool("SB", str(baud))
        elif baud in rateDict.keys:
            res = self.CommandBool("SB", str(rateDict[baud]))
        else:
            raise LX200Error(
                "baud " +
                str(baud) +
                " is not one of 56.7, 38.4, 28.8, 19.2, 14.4, 9600, 4800, 2400, 1200")
        return res

    def test_baud_rates(self, portNum):
        """ check com port for possible speeds
        blist[0] will be the fastest """
        blist = []
        for b in [4800, 9600, 19200, 38400, 57600, 115200]:
            try:
                print 'trying', b
                thisPort = self.connect(portNum, baud=b, ptimeout=2)
                if thisPort:
                    blist.append(b)
                    self.connectedPort.close()
            except BaseException:
                pass
        return blist
