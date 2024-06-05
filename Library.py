#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Name:        Library.py
# Purpose:     General access to and use of LX200 Object Library
#
# Author(s):   R J Schumacher
#
# Created:     2006/01/28
# RCS-ID:      $Id: Library.py $
# Copyright:   (c) 2006
# Licence:     LGPL
#
# -----------------------------------------------------------------------------


class Library:
    """Class for the LX200 built-in object library     """

    def __init__(self, comPort, debug=False):
        """Constructor.

        Arguments: a COM port object instance from LXSerial to talk through
        """
        self.comPort = comPort

    def __repr__(self):
        """Return a representation string.
        """
        return "<LX200 Library instance>"

    # -------------------------------------------------------------------------------
    # G - Get Commands
    # -------------------------------------------------------------------------------

    def getMagBrightLimit(self):
        """ Get Browse Brighter Magnitude Limit
        Returns: sMM.M#
        The magnitude of the brightest object to be returned from the telescope FIND/BROWSE command.
        Command when searching for objects in the Deep Sky database."""
        self.comPort.CommandString("Gb")

    def get_object_Dec(self):
        """ Get Currently Selected Object/Target Declination
        Returns: sDD*MM#
         or sDD*MM'SS#
        Depending upon the current precision setting for the telescope."""
        self.comPort.CommandString("Gd")

    def getFindField(self):
        """ Get Find Field Diameter
        Returns: NNN#
        An ASCIi interger expressing the diameter of the field search used
        in the IDENTIFY/FIND commands."""
        self.comPort.CommandString("GF")

    def getMagFaintLimit(self):
        """ Get Browse Faint Magnitude Limit
        Returns: sMM.M")
        The magnitude or the faintest object to be returned from the telescope
        FIND/BROWSE command."""
        self.comPort.CommandString("Gf")

    def get_min_quality(self):
        """ Get Minimum Quality For Find Operation
        Returns:
        SU# Super
        EX# Excellent
        VG# Very Good
        GD# Good
        FR# Fair
        PR# Poor
        VP# Very Poor
        The mimum quality of object returned by the FIND command."""
        self.comPort.CommandString("Gq")

    def get_smallest_limit(self):
        """ Get Larger Size Limit
        Returns: NNN'#
        The size of the smallest object to be returned by a search of the
        telescope using the BROWSE/FIND commands."""
        self.comPort.CommandString("Gl")

    def get_target_RA(self):
        """ Get current/target object RA
        Returns: HH:MM.T#
         or HH:MM:SS
        Depending upon which precision is set for the telescope"""
        return self.comPort.CommandString("Gr")

    def get_largest_limit(self):
        """ Get Smaller Size Limit
        Returns: NNN'#
        The size of the largest object returned by the FIND command expressed in arcminutes."""
        return self.comPort.CommandString("Gs")

    def get_search_string(self):
        """ Get deepsky object search string
        Returns: GPDCO#
            A string indicaing the class of objects that should be returned by the FIND/BROWSE command. If the character
        is upper case, the object class is return. If the character is lowercase, objects of this class are ignored. The
        character meanings are as follws:
        G - Galaxies
        P - Planetary Nebulas
        D - Diffuse Nebulas
        C - Globular Clusters
        O - Open Clusters"""
        return self.comPort.CommandString("Gy")

    # -------------------------------------------------------------------------------
    # L - Object Library Commands
    # -------------------------------------------------------------------------------

    def set_prev(self):
        """ Find previous object and set it as the current target object.
        Returns: Nothing
        LX200GPS & Autostar - Performs no function"""
        self.comPort.CommandBlind("LB")

    def set_target_object(self, num):
        """Set current target object to deep sky catalog object number NNNN
        Returns : Nothing
        LX200GPS & Autostar - Implemented in later firmware revisions"""
        self.comPort.CommandBlind("LC", "%4d" % (num))

    def find_obj(self):
        """ Find Object using the current Size, Type, Upper limit, lower limt
        and Quality contraints and set it as current target object.
        Returns: Nothing
        LX200GPS & Autostar - Performs no function """
        self.comPort.CommandBlind("LF")

    def identify(self):
        """ Identify object in current field.
        Returns: <string>")
        Where the string contains the number of objects in field & object in center field.
        LX200GPS & Autostar - Performs no function.
        Returns static string "0 - Objects found"."""
        self.comPort.CommandBlind("Lf")

    def get_obj_info(self):
        """ Get Object Information
        Returns: <string>")
        Returns a string containing the current target object's name and object type.
        LX200GPS & Autostar - performs no operation. Returns static description of Andromeda Galaxy."""
        self.comPort.CommandBlind("LI")

    def set_M_object(self, num):
        """Set current target object to Messier Object NNNN, an ASCII expressed decimal number.
        Returns: Nothing.
        LX200GPS and Autostar - Implemented in later versions."""
        self.comPort.CommandBlind("LM", "%4d" % (num))

    def find_next_obj(self):
        """ Find next deep sky target object subject to the current constraints.
        LX200GPS & AutoStar - Performs no function"""
        self.comPort.CommandBlind("LN")

    def set_library(self, libNum):
        """ Select deep sky Library where D specifices
        0 - Objects CNGC / NGC in Autostar & LX200GPS
        1 - Objects IC
        2 - UGC
        3 - Caldwell (Autostar & LX200GPS)
        4 - Arp (LX200 GPS)
        5 - Abell (LX200 GPS)
        Returns:
        1 Catalog available
        0 Catalog Not found
        LX200GPS & AutoStar - Performs no function always returns "1" """
        return self.comPort.CommandBool("Lo", libNum)

    def set_star_catalog(self, num):
        """ Select star catalog D, an ASCII integer where D specifies:
        0 STAR library (Not supported on Autostar I & II)
        1 SAO library
        2 GCVS library
        3 Hipparcos (Autostar I & 2)
        4 HR (Autostar I & 2)
        5 HD (Autostar I & 2)
        Returns:
        1 Catalog Available
        2 Catalog Not Found"""
        return self.comPort.CommandString("Ls", num)

    def set_star_object(self, num):
        """Select star NNNN as the current target object from the currently selected catalog
        Returns: Nothing
        LX200GPS & AutoStar - Available in later firmwares"""
        self.comPort.CommandBlind("LS", "%4d" % (num))

    # -------------------------------------------------------------------------------
    # S - Telescope Set Commands
    # -------------------------------------------------------------------------------
    def set_bright_limit(self, lim):
        """    Set Brighter limit to the ASCII decimal magnitude string. SMM.M
        Returns:
        0 - Valid
        1 - invalid number"""
        return self.comPort.CommandBool("Sb", lim)

    def set_faint_limit(self, lim):
        """Set faint magnitude limit to sMM.M
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("Sf", lim)

    def set_field_dia(self, mins):
        """Set FIELD/IDENTIFY field diamter to NNNN arc minutes.
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("SF", mins)

    def set_min_obj(self, elev):
        """Set the minimum object elevation limit to DD")
            Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("Sh", elev)

    def set_smallest_size(self, size):
        """Set the size of the smallest object returned by FIND/BROWSE to NNNN arc minutes
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("Sl", size)

    def step_quality(self):
        """Step the quality of limit used in FIND/BROWSE through its cycle of
        VP ... SU. Current setting can be queried with :Gq#
        Returns: Nothing"""
        self.comPort.CommandBlind("Sq")

    def set_largest_size(self, size):
        """Set the size of the largest object the FIND/BROWSE command will return to NNNN arc minutes
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("Ss", size)

    def set_obj_select(self):
        """Sets the object selection string used by the FIND/BROWSE command.
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("SyGPDCO")

    # -------------------------------------------------------------------------------
    # C - Sync Control
    # -------------------------------------------------------------------------------

    def sync_object(self, object=None):
        """ Synchronizes the telescope's position with the currently selected database object's coordinates.
        Returns:
        LX200's - a "#" terminated string with the name of the object that was sync'd.
        Autostars & LX200GPS - A static string: " M31 EX GAL MAG 3.5 SZ178.0'#" """
        return self.comPort.CommandString("CM")
