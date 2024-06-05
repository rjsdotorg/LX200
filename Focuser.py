#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Name:        Focuser.py
# Purpose:     General access to and use of LX200 Focuser accessories
#
# Author(s):   R J Schumacher
#
# Created:     2006/01/28
# RCS-ID:      $Id: Focuser.py $
# Copyright:   (c) 2006
# Licence:     LGPL
#
# -----------------------------------------------------------------------------


class Focuser:
    """LX200 class for Focuser movement and properties

    """

    def __init__(self, comPort, debug=False):
        """Constructor.
        Arguments:
        """
        self.comPort = comPort

    def __repr__(self):
        """Return a representation string.
        """
        return "<LX200 Focuser instance>"

    # -------------------------------------------------------------------------------
    # F - Focuser Control
    # -------------------------------------------------------------------------------
    def Move(Position):
        """Position (Long) Step distance
        Return (Nothing) Does not return a value.
        Remarks
        If the Absolute property is True, then this is an absolute positioning
        focuser. The Move command tells the focuser to move to an exact step
        position, and the Position property is an integer between 0 and MaxStep.
        If the Absolute property is False, then this is a relative positioning
        focuser. The Move command tells the focuser to move in a relative direction,
        and the Position property is an integer between minus MaxIncrement and plus
        MaxIncrement. """
        # add speed compensation...
        if Position > 0:
            self.focus_in(speed=1, t=Position)
        elif Position < 0:
            self.focus_out(speed=1, t=Position)
        return None

    def SetupDialog(self, fileName='Focuser.cfg'):
        """ Mandatory, in advanced mode additional
        parameters, such as the scope position, guide rates etc. will be
        set.
        No dialog, just read config...
        """
        import configParser
        # start the Configparser module
        self.config = ConfigParser.ConfigParser()
        self.config.read(fileName)

    def focus_in(self, speed=1, t=0):
        """ Start Focuser moving inward (toward objective)
        Returns: None"""
        if speed:
            if self.model != 'LX200GPS':
                self.focus_speed(speed)
            elif speed in [1, 2]:
                self.focus_slow()
            elif speed in [3, 4]:
                self.focus_fast()
            else:
                raise LX200Error(
                    "unsupported speed: " +
                    speed +
                    " for focusser")
        self.comPort.CommandBlind("F+")
        if t:
            time.sleep(t)
            self.Halt()

    def focus_out(self):
        """ Start Focuser moving outward (away from objective)
        Returns: None"""
        if speed:
            if self.model != 'LX200GPS':
                self.focus_speed(speed)
            elif speed in [1, 2]:
                self.focus_slow()
            elif speed in [3, 4]:
                self.focus_fast()
            else:
                raise LX200Error(
                    "unsupported speed: " +
                    speed +
                    " for focusser")
        self.comPort.CommandBlind("F-")
        if t:
            time.sleep(t)
            self.focus_stop()

    def Halt(self):
        """ Halt Focuser Motion
        Returns: Nothing"""
        self.comPort.CommandBlind("FQ")
        return None

    def focus_fast(self):
        """ Set Focus speed to fastest setting
        Returns: Nothing"""
        self.comPort.CommandBlind("FF")

    def focus_slow(self):
        """ Set Focus speed to slowest setting
        Returns: Nothing"""
        self.comPort.CommandBlind("FS")

    def focus_speed(self, speed):
        """ Autostar & LX200GPS - set focuser speed to <n> where <n> is an ASCII digit 1..4
        Returns: Nothing
        LX200 - Not Supported"""
        if self.model != 'LX200GPS':
            raise LX200Error(
                "unsupported model: " +
                self.model +
                " for Optical Tube Assembly Temperature")
        self.comPort.CommandBlind("F", speed)
