#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Name:        LX200Utils.py
# Purpose:     LX200 telescopes and accessories
#
# Author(s):   R J Schumacher
#
# Created:     2006/01/28
# RCS-ID:      $Id: LX200Utils.py $
# Copyright:   (c) 2006
# Licence:     LGPL
#
# -----------------------------------------------------------------------------
"""
class LX200Utils:
    ""LX200 class for methods other classes use
    Note:
    two ports can be opened on the LX200

    ""
    def __init__(self):

        pass
"""
DEG = chr(223)  # ASCII char for degree
# -------------------------------------------------------------------------------
# used by Telescope and Library classes, but also useful alone
# based on code from http://projgalileo.sourceforge.net/
# -------------------------------------------------------------------------------


def to_float(resp):
    """Converts a string in base-60 with any separator into a float"""
    # Split at any nondigit character, then add them up
    import re
    nondigit = re.compile(r'[^0-9+-]')
    if resp[0] != '+' and resp[0] != '-':
        parts = nondigit.split(str(resp))
    else:
        parts = nondigit.split(str(resp[1:]))
    tot = 0.0
    mult = 1
    for part in parts:
        tot += float(part) / mult
        mult *= 60
    if resp[0] == '-':
        tot -= 2 * tot
    return tot


def from_lx200_righta(resp):
    """Converts an lx200 righta response into an angle in degrees"""
    angle = _to_float(resp)
    return angle * 360 / 24


def to_lx200_righta(angle):
    """Converts float angle to HH:MM.M"""
    angle = angle * 24 / 360
    hours = int(angle)
    angle -= hours
    mins = angle * 60
    return '%02d:%03f' % (hours, mins)


def from_lx200_angle(resp):
    """Converts an lx200 declination response into an angle"""
    angle = _to_float(resp)
    return angle


def to_lx200_angle(angle):
    """Converts float angle to sDD*MM"""
    if angle < 0:
        angle = -angle
        sign = '-'
    else:
        sign = '+'
    mins = (angle - int(angle)) * 60.0
    return '%c%02d%c%02d' % (sign, int(angle), DEG, mins)


def to_lx200_long_angle(angle):
    """Converts float angle to sDD*MM:SS"""
    if angle < 0:
        angle = -angle
        sign = '-'
    else:
        sign = '+'
    mins = (angle - int(angle)) * 60.0
    secs = (mins - int(mins)) * 60.0
    return '%c%02d%c%02d:%02d' % (sign, int(angle), DEG, mins, secs)
