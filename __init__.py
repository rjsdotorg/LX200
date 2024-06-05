#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Name:        pyLX200.py
# Purpose:     General access to and use of LX200 telescopes and accesories
#
# Author(s):   R J Schumacher
#
# Created:     2006/01/28
# RCS-ID:      $Id: pyLX200.py $
# Copyright:   (c) 2006
# Licence:     LGPL
#
# -----------------------------------------------------------------------------

from __version__ import version
from Focuser import Focuser
from Derotator import Derotator
from Reticule import Reticule
from LX200Error import LX200Error
from LX200Utils import *
from LXGPS import LXGPS
from LXSerial import LXSerial
from Library import Library
from Telescope import Telescope
from sys import argv
help_comment = """
Meade Telescope Serial Command Protocol
Revision L
9 October 2002
Introduction
The Meade Telescope Serial Control Protocol utilized to
remotely command and control Meade Telescopes. This command language contains a
core of common commands supported by all telescopess. Due to different
implementation and technological advances the command has extensions that are not
supported by all models. The differences are noted in the descriptive text for
the commands. Finally, there are a series of new commands for the
LX200GPS. These commands are in the LXGPS module.

As an extension to the Telescope Protocol beginning with the LX200GPS, a
possible response to any command is ASCII NAK (0x15). Should the telescope
control chain be busy and unable to accept an process the command, a NAK will
be sent within 10 msec of the receipt of the # terminating the command. In this
event, the controller should wait a reasonable interval and retry the command.

Telescope Command Groupings: ------------------ Supported ------------
Command Group
Command Designator     Symbol   AutoStar LX200<16" LX 16" LX200GPS
Alignment Query         <ACK>       x         x      x      x
Alignment*              A           x         x      x      x
Active Backlash         $B          -         -      -      x
Reticule Control*       B           x         p      p      x
Sync Control            C           p         p      p      x
Distance Bars           D           x         x      x      x
Fan*                    f           -         -      p      x
Focus Control Commands  F           p         p      p      x
GPS Commands            g           -         -      -      x
Get Information         G           x         x      x      x
Home Position Commands* h           x         -      x      x
Hour                    H           x         x      x      x
Initialize Telescope    I           -         -      -      x
Library                 L           p         p      p      x
Movement                M           x         p      x      x
High Precision          P           x         x      x      x
Smart Drive Control*    $Q          x         x      x      x
Quit Command            Q           x         x      x      x
Field De-rotator        r           -         -      p      x
Rate Control            R           p         p      p      x
Set Information         S           x         x      x      x
Tracking Frequency      T           p         p      p      x
User Format Control     U           p         x      x      x
Way point (Site)        W           x         x      x      x
Help Commands           ?           -         x      x      -
Notes:
Commands accepted by the telescopes are shown in the table above indicated by an x entry. This means that
the telescope will accept these commands and respond with a syntactically valid response where required.
A "p" indicated only a subset of this command class is supported. Due to the differing implementations of
the telescopes, some of the commands may provide static responses or may do nothing in response to the
command. See the detailed description of the commands to determine the exact behavior.

Command line example:

from LX200 import *
port = LXSerial(debug=True)
port.connect("COM1")
scope = Telescope(port, "LX200", debug=True) #
scope.set_site(1)
scope.set_align_mode("P")
scope.set_slew_rate(Telescope.FIND)
if scope.determine_model=="LX200GPS": #optional
    scope.model = 'LX200GPS'
    scope.auto_align()
else:
    raw_input("do your alignment, then press enter ")

scope.set_pointing_mode(mode='HIGH PRECISION')
library = Library(port, scope)
library.set_M_object(101)
#fine adjust
raw_input("center the object, then press enter ")

library.sync_object()
# etc...
port.close()

or, just run
>python LX200.py  do basic setup in main()

This code is not safe for multi-threaded serial port operation...
The author(s) bear no responsibility for equipment, financial, or psychological
damages due to use of this code.
"""


__all__ = ['Derotator',
           'Focuser',
           'Library',
           'LXSerial',
           'LXGPS',
           'LX200Utils',
           'LX200Error',
           'Reticule',
           'Telescope',
           '__version__']


def main(argv):
    if len(argv) == 1:
        argv.append('LX200')  # LX200 "classic" is default
    port = LXSerial(debug=False)
    try:
        port.connect('COM1')
    except BaseException:
        print 'COM1 connect failed'
        return
    scope = Telescope(port, argv[1], debug=False)
    scope.set_site(1)
    scope.set_align_mode('P')
    scope.set_slew_rate('FIND')
    if scope.model == 'LX200GPS':
        scope.auto_align()
    else:
        raw_input("do your alignment, then press enter ")

    scope.set_pointing_mode('HIGH PRECISION')
    library = Library(port, scope)
    library.set_M_object(101)
    # fine adjust
    raw_input("center the object, then press enter ")
    library.sync_object()


if __name__ == '__main__':
    try:
        if argv[1] in ('-h', '-help'):
            print help_comment
    except BaseException:
        pass
    main(argv)
