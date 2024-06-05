#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Name:        Reticule.py
# Purpose:     General access to and use of LX200 Reticule accesories
#
# Author(s):   R J Schumacher
#
# Created:     2006/01/28
# RCS-ID:      $Id: Reticule.py $
# Copyright:   (c) 2006
# Licence:     LGPL
#
# -----------------------------------------------------------------------------


class Reticule:
    """LX200 class for Reticule and properties

    """

    def __init__(self, comPort, debug=False):
        """Constructor.
        Arguments:
        """
        self.comPort = comPort

    def __repr__(self):
        """Return a representation string.
        """
        return "<LX200 Reticule instance>"

    # -------------------------------------------------------------------------------
    # B - Reticule/Accessory Control
    # -------------------------------------------------------------------------------
    def brighter(self):
        self.issue_command("B+")
        """ Increase reticule Brightness
        Return: Nothing"""

    def darker(self):
        self.issue_command("B-")
        """ Decrease Reticule Brightness
        Return: Nothing"""

    def setFlashRate(self):
        self.issue_command("B<n>")
        """ Set Reticle flash rate to <n> (an ASCII expressed number)
        <n> Values of 0..3 for LX200 series
        <n> Values of 0..9 for Autostar and LX200GPS
        Return: Nothing"""

    def setDutyCycle(self):
        self.issue_command("BDn")
        """ Set Reticule Duty flash duty cycle to <n> (an ASCII expressed digit) [LX200 GPS Only]
        <n> Values: 0 = On, 1..15 flash rate
        Return: Nothing"""
