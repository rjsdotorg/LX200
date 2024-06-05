#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Name:        Derotator.py
# Purpose:     Derotator commands for LX200 telescopes and accessories
#
# Author(s):   R J Schumacher
#
# Created:     2006/01/28
# RCS-ID:      $Id: pyLX200.py $
# Copyright:   (c) 2006
# Licence:     LGPL
#
# -----------------------------------------------------------------------------

class Derotator:
    """LX200 class for Derotator movement and properties

    """

    def __init__(self, comPort, debug=False):
        """Constructor.
        """
        self.comPort = comPort
    # -------------------------------------------------------------------------------
    # r - Field Derotator Commands
    # -------------------------------------------------------------------------------

    def setOn(self):
        """ Turn on Field Derotator [LX 16" and LX200GPS]
        Returns: Nothing"""
        self.comPort.CommandBlind("r+")

    def setOff(self):
        """ Turn off Field Derotator, halt slew in progress. [Lx 16" and LX200GPS]
        Returns Nothing"""
        self.comPort.CommandBlind("r-")
