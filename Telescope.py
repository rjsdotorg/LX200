#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Name:        Telescope.py
# Purpose:     General access to and use of LX200 telescopes
#
# Author(s):   R J Schumacher
#
# Created:     2006/01/28
# RCS-ID:      $Id: Telescope.py $
# Copyright:   (c) 2006
# Licence:     LGPL
#
# -----------------------------------------------------------------------------

import time
import LX200
from .LX200Utils import *
# from LX200.LXSerial import LXSerial
from LX200.LX200Error import LX200Error

DEG = chr(223)  # ASCII char for degree
GUIDE = "G"
CENTRE = "C"
FIND = "M"
MAX = "S"
SUPPORTED_MODELS = ('AutoStar', 'LX200', 'LX16', 'LX200GPS')


class Telescope:
    """LX200 class for scope movement and properties
    Note:
    - two ports can be opened on the LX200
    - as many scopes as COM ports available can be driven
    """

    def __init__(self, comPort, model='LX200', debug=False):
        """Constructor.
        """
        try:
            import configparser
        except BaseException:
            print('the ConfigParser module is needed for storing setup info.')
            print('do not use the setup* methods')
        if model in SUPPORTED_MODELS:
            self.model = model
        else:
            raise LX200Error("unsupported model: " + model)

        self.comPort = comPort
        self.AlignmentMode = None  # 'A','L','P'
        self.pointingMode = "LOW PRECISION"
        self.displayPrecision = ""
        self.debug = debug

    def __repr__(self):
        """Return a representation string.
        """
        return "<LX200 Telescope instance>"

    def setup_dialog(self, fileName='LX200.cfg'):
        """ Mandatory, in advanced mode additional
        parameters, such as the scope position, guide rates etc. will be
        set.
        No dialog, just read config...
        """
        # start the Configparser module
        self.config = configparser.ConfigParser()
        self.config.read(fileName)

    # -------------------------------------------------------------------------------
    # utility methods
    # -------------------------------------------------------------------------------

    def determine_model(self, model="LX200"):
        """ TO DO
        run a series of commands to test for pass/fail
        """
        return model

    def set_time_lon(self, time, lon):
        """ Since the time setting in seconds is 4x better than the Lon setting
        of minutes, I propose using the combination of Lon and time to minimize
        error of rounding: ie, if Lon is 117deg15'19" use the time setting to
        compensate for the 19".
        """
        return False

    # -------------------------------------------------------------------------------
    # ACK - Alignment Query
    # -------------------------------------------------------------------------------

    def get_alignment(self):
        """ Query of alignment mounting mode.
        Returns:
        A If scope in AltAz Mode
        L If scope in Land Mode
        P If scope in Polar Mode"""
        try:
            self.comPort.connectedPort.write(chr(0x06))
        except BaseException:
            raise LX200Error(
                "get_alignment - port write error:  %s" %
                (sys.exc_info()[0]))

        if not self.debug:
            return self.comPort.connectedPort.read(1)
        else:
            return 'L'

    # -------------------------------------------------------------------------------
    # A - Alignment Commands
    # -------------------------------------------------------------------------------
    def auto_align(self):
        """ Start Telescope Automatic Alignment Sequence [LX200GPS only]
        Returns:
        1: When complete (can take several minutes).
        0: If scope not AzEl Mounted or align fails"""
        align_res = self.get_alignment()
        if align_res != "A":
            raise LX200Error(
                "unsupported alignment: " +
                align_res +
                " for auto_align")
        if self.model != 'LX200GPS':
            raise LX200Error(
                "unsupported model: " +
                self.model +
                " for auto_align")
        result = self.comPort.CommandBool('A', 'a')
        if result != 1:
            raise LX200Error("auto_align failed")

        return result

    def set_align_mode(self, mode):
        """Sets method of alignment used
        L Land alignment mode
        P Polar alignment mode
        A AltAz alignment mode
        Returns: nothing"""
        if mode not in ['A', 'L', 'P']:
            raise LX200Error("mode not in ['A','L','P']")
        self.comPort.CommandBlind('A', mode)
        self.AlignmentMode = mode

    # -------------------------------------------------------------------------------
    # C - Sync Control
    # -------------------------------------------------------------------------------

    def lunar_sync(self, coords=None):
        """ Synchonize the telescope with the current Selenographic coordinates."""
        self.comPort.CommandBlind("CL")

    # -------------------------------------------------------------------------------
    # D - Distance Bars
    # -------------------------------------------------------------------------------
    def get_distance(self):
        dist = self.comPort.CommandString("D")
        return len(dist.strip())

    # -------------------------------------------------------------------------------
    # f - Fan Command
    # -------------------------------------------------------------------------------

    def fan_on(self):
        """
        LX 16"- Turn on the tube exhaust fan

        LX200GPSTurn on power to accessor panel
        LX200 7" Maksutov - Turn on cooling fan
        Autostar & LX200 < 16" - Not Supported
        Returns: nothing"""
        # if self.model!='LX200GPS' and self.model!='LX16':
        #    raise LX200Error("unsupported model: "+self.model+" for fan/power")
        self.comPort.CommandBlind("f", "+")

    def fan_off(self):
        """ LX 16"- Turn off tube exhaust fan
        LX200GPS - Turn off power to accessory panel
        LX200 7" Maksutov - Turn off cooling fan
        Autostar & LX200 < 16" - Not Supported
        Returns: Nothing"""
        # if self.model!='LX200GPS' and self.model!='LX16':
        #    raise LX200Error("unsupported model: "+self.model+" for fan/power")
        self.comPort.CommandBlind("f", "-")

    def get_temperature(self):
        """ LX200GPS - Return Optical Tube Assembly Temperature
        Returns <sdd.ddd>  - a '#' terminated signed ASCII real number
        indicating the Celsius ambient temperature.
        All others - Not supported"""
        if self.model != 'LX200GPS':
            raise LX200Error(
                "unsupported model: " +
                self.model +
                " for Optical Tube Assembly Temperature")
        return self.comPort.CommandString("f", "T")

    # -------------------------------------------------------------------------------
    # G - Get Telescope Information
    # -------------------------------------------------------------------------------

    def get_menu_entry(self, entry):
        """ Get Alignment Menu Entry
        Returns: A '#' Terminated ASCII string. [LX200 legacy command]"""
        return self.comPort.CommandString("G", entry)

    def get_Altitude(self):
        """ Get Telescope Altitude
        Returns: sDD*MM#
        or sDD*MM'SS#
        The current scope altitude.
        The returned format depending on the current precision setting."""
        return self.comPort.CommandString("GA")

    def get_local_time12(self):
        """ Get Local Telescope Time In 12 Hour Format
        Returns: HH:MM:SS#
        The time in 12 format"""
        return self.comPort.CommandString("Ga")

    def get_date(self):
        """ Get current date.
        Returns: MM/DD/YY#
        The current local calendar date for the telescope."""
        return returnself.comPort.CommandString("GC")

    def get_calendar_format(self):
        """ Get Calendar Format
        Returns: 12#
         or 24#
        Depending on the current telescope format setting."""
        return self.comPort.CommandString("Gc")

    def get_Dec(self):
        """ Get Telescope Declination.
        Returns: sDD*MM#
        or sDD*MM'SS#
        Depending upon the current precision setting for the telescope."""
        return self.comPort.CommandString("GD")

    def get_UTC_offset(self):
        """ Get UTC offset time
        Returns: sHH#
         or sHH.H#
        The number of decimal hours to add to local time to convert it to UTC.
        If the number is a whole number the  sHH#
         form is returned, otherwise the longer form is return. On Autostar and
         LX200GPS, the daylight savings setting in effect is factored into
         returned value."""
        return self.comPort.CommandString("GG")

    def get_current_long(self):
        """ Get Current Site Longitude
        Returns: sDDD*MM")
        The current site Longitude. East Longitudes are expressed as negative"""
        return self.comPort.CommandString("Gg")

    def get_high_limit(self):
        """ Get High Limit
        Returns: sDD*
        The minimum elevation of an object above the horizon to which the
        telescope will slew with reporting a
        "Below Horizon" error."""
        return self.comPort.CommandString("Gh")

    def get_local_time_24(self):
        """ Get Local Time in 24 hour format
        Returns: HH:MM:SS#
        The Local Time in 24-hour Format"""
        return self.comPort.CommandString("GL")

    def get_lower_limit(self):
        """ Get Lower Limit
        Returns: DD*#
            The highest elevation above the horizon that the telescope will be
            allowed to slew to without a warning message."""
        return self.comPort.CommandString("Go")

    def get_site_names(self):
        """ return all names in a List
        """
        siteList = []
        siteList.append(self.get_site1())
        siteList.append(self.get_site2())
        siteList.append(self.get_site3())
        siteList.append(self.get_site4())
        return siteList

    def get_site(self, siteNum):
        """ return site name
        """
        return self.get_site_names()[siteNum - 1]

    def get_site1(self):
        """ Get Site 1 Name
        Returns: <string>#
        A '#' terminated string with the name of the requested site."""
        return self.comPort.CommandString("GM")

    def get_site2(self):
        """ Get Site 2 Name
        Returns: <string>#
        A '#' terminated string with the name of the requested site."""
        return self.comPort.CommandString("GN")

    def get_site3(self):
        """ Get Site 3 Name
        Returns: <string>#
        A '#' terminated string with the name of the requested site."""
        return self.comPort.CommandString("GO")

    def get_site4(self):
        """ Get Site 4 Name
        Returns: <string>#
        A '#' terminated string with the name of the requested site."""
        return self.comPort.CommandString("GP")

    def get_RA(self):
        """ Get Telescope RA
        Returns: HH:MM.T#
         or HH:MM:SS#
        Depending which precision is set for the telescope"""
        return self.comPort.CommandString("GR")

    def get_sidereal_time(self):
        """ Get the Sidereal Time
        Returns: HH:MM:SS#
        The Sidereal Time as an ASCII Sexidecimal value in 24 hour format"""
        return self.comPort.CommandString("GS")

    def get_tracking_rate(self):
        """ Get tracking rate
        Returns: TT.T#
        Current Track Frequency expressed in hertz assuming a synchonous motor design where a 60.0 Hz motor clock
        would produce 1 revolution of the telescope in 24 hours.
        """
        return self.comPort.CommandString("GT")

    def get_site_lat(self):
        """ Get Current Site Latitude
        Returns: sDD*MM#
        The latitude of the current site. Positive inplies North latitude."""
        return self.comPort.CommandString("Gt")

    def get_AZ(self):
        """ Get telescope azimuth
        Returns: DDD*MM#T or DDD*MM'SS#
        The current telescope Azimuth depending on the selected precision."""
        return self.comPort.CommandString("GZ")

    # -------------------------------------------------------------------------------
    # h - Home Position Commands
    # -------------------------------------------------------------------------------
    def store_home(self):
        """ LX200GPS and LX 16" Seeks Home Position and stores the encoder values
        from the aligned telescope at the home position in the nonvolatile memory of the
        scope.
        Returns: Nothing
        Autostar,LX200 - Ignored ???"""
        self.comPort.CommandBlind("hS")

    def align_home(self):
        """ LX200GPS and LX 16" Seeks the Home Position of the scope and sets/aligns
        the scope based on the encoder values stored in non-volatile memory
        Returns: Nothing
        Autostar,LX200 - Igrnored ???"""
        if self.model in ['Autostar']:
            raise LX200Error(
                "unsupported model: " +
                self.model +
                " for home command")
        self.comPort.CommandBlind("hF")

    def FindHome(self):
        """ Autostar, LX200GPS and LX 16"Slew to Park Position
        Returns: Nothing"""
        self.comPort.CommandBlind("hP")
        while True:
            res = self.get_home_status()
            if res == 0:
                raise LX200Error("FindHome failed")
            elif res == 1:
                break
            time.sleep(.5)

    def get_home_status(self):
        """ Autostar, LX200GPS and LX 16" Query Home Status
        Returns:
        0 Home Search Failed
        1 Home Search Found
        2 Home Search in Progress
        LX200 Not Supported"""
        return self.comPort.CommandString("h?")

    # ---------------------------------------------------------------------------
    # H - Time Format Command
    # ---------------------------------------------------------------------------
    def toggle_time_format(self):
        """ Toggle Between 24 and 12 hour time format
        Returns: Nothing"""
        self.comPort.CommandBlind("H")

    # -------------------------------------------------------------------------------
    # M - Telescope Movement Commands
    # -------------------------------------------------------------------------------
    def axis_rates(Axis):
        """Axis (TelescopeAxes) The axis about which rate information is desired
        Return (Object) Collection of Rate objects describing the supported
        rates of motion that can be supplied to the MoveAxis() method for the
        specified axis.         """
        return (GUIDE, CENTRE, FIND, MAX)

    def can_move_axis(Axis):
        """Axis (TelescopeAxes) The identifier for the axis to be tested
        Return (Boolean) True if the telescope can be controlled about the
        specified axis via the MoveAxis() method.         """
        return True

    def move_to_current_target(self):
        """ Autostar, LX 16", LX200GPS - Slew to target Alt and Az
        Returns:
        0 - No fault
        1 - Fault
        LX200 - Not supported"""
        return self.comPort.CommandBool("MA")

    def move_East(self, rate=None, t=None):
        """ Move Telescope East at current slew rate
        Returns: Nothing"""
        self.comPort.CommandBlind("Me")

    def move_North(self):
        """ Move Telescope North at current slew rate
        Returns: Nothing"""
        self.comPort.CommandBlind("Mn")

    def move_South(self):
        """ Move Telescope South at current slew rate
        Returns: Nothing"""
        self.comPort.CommandBlind("Ms")

    def move_West(self):
        """ Move Telescope West at current slew rate
        Returns: Nothing"""
        self.comPort.CommandBlind("Mw")

    def move_to_object(self):
        """ Slew to Target Object
        Returns:
        0 Slew is Possible
        1<string> Object Below Horizon w/string message
        2<string> Object Below Higher w/string message"""
        return self.comPort.CommandString("MS")

    # -------------------------------------------------------------------------------
    # P - High Precision Toggle
    # -------------------------------------------------------------------------------
    def set_pointing_mode(self, mode=None):
        """ set or toggle precision
        in high precision mode -- requires centering"""
        if not mode:
            resp = self.toggle_precision()
        elif mode == 'HIGH PRECISION':
            resp = self.toggle_precision()
            if resp == 'LOW PRECISION':
                resp = self.toggle_precision()
        elif mode == 'LOW PRECISION':
            resp = self.toggle_precision()
            if resp == 'HIGH PRECISION':
                resp = self.toggle_precision()
        self.pointingMode = resp
        return resp

    def toggle_precision(self):
        """ Toggles High Precsion Pointing. When High precision pointing is
        enabled scope will first allow the operator to center a
        nearby bright star before moving to the actual taget.
        Returns: <string>
        "HIGH PRECISION" Current setting after this command.
        "LOW PRECISION" Current setting after this command."""
        self.comPort.CommandBlind("P")

        if not self.debug:
            return self.comPort.connectedPort.read(14)
        else:
            return 'HIGH PRECISION'

    # -------------------------------------------------------------------------------
    # Q- Smart Drive Control
    # -------------------------------------------------------------------------------
    def smart_PEC_toggle(self):
        """Toggles Smart Drive PEC on and off for both axis
        Returns: Nothing
        Not supported on Autostar"""
        self.comPort.CommandBlind("$Q")

    # -------------------------------------------------------------------------------
    # Q - Movement Commands
    # -------------------------------------------------------------------------------

    def AbortSlew(self, direction=None):
        """ Halt all current slewing
        Returns:Nothing"""
        self.comPort.CommandBlind("Q", direction)

    def AbortSlew_East(self):
        """ Halt eastward Slews
        Returns: Nothing"""
        self.comPort.CommandBlind("Qe")

    def AbortSlew_North(self):
        """ Halt northward Slews
        Returns: Nothing"""
        self.comPort.CommandBlind("Qn")

    def AbortSlew_South(self):
        """ Halt southward Slews
        Returns: Nothing"""
        self.comPort.CommandBlind("Qs")

    def AbortSlew_West(self):
        """ Halt westward Slews
        Returns: Nothing"""
        self.comPort.CommandBlind("Qw")

    # -------------------------------------------------------------------------------
    # R - Slew Rate Commands
    # -------------------------------------------------------------------------------

    def set_slew_rate(self, rate):
        """Sets slew rate, use one of  GUIDE,  CENTRE,  FIND,
         MAX -- in order slowest to fastest"""
        self.comPort.CommandBlind('R', rate)

    def set_slew_centering(self):
        """ Set Slew rate to Centering rate (2nd slowest)
        Returns: Nothing"""
        CommandBlind("RC")

    def ser_slew_guide(self):
        """ Set Slew rate to Guiding Rate (slowest)
        Returns: Nothing"""
        self.comPort.CommandBlind("RG")

    def set_slew_find(self):
        """ Set Slew rate to Find Rate (2nd Fastest)
        Returns: Nothing"""
        self.comPort.CommandBlind("RM")

    def set_slew_max(self):
        """ Set Slew rate to max (fastest)
        Returns: Nothing"""
        self.comPort.CommandBlind("RS")

    # -------------------------------------------------------------------------------
    # S - Telescope Set Commands
    # -------------------------------------------------------------------------------
    def set_site(self, site):
        """Set current site to <n>, an ASCII digit in the range 0..3
        Returns: Nothing"""
        self.comPort.CommandBlind('W', site)

    def set_target_alt(self, alt):
        """Set target object altitude to sDD*MM# or sDD*MM'SS"
         [LX 16", Autostar, LX200GPS]
        Returns:
        0 Object within slew range
        1 Object out of slew range"""
        return self.comPort.CommandBool("Sa", alt)

    def change_date(self, date):
        """Change Handbox Date to MM/DD/YY
        Returns: <D><string>
        D = '0' if the date is invalid. The string is the null string.
        D = '1' for valid dates and the string is "Updating Planetary Data"
             #"
        Note: For LX200GPS this is the UTC data!"""
        return self.comPort.CommandBool("SC", date)

    def set_target_DEC(self, angle):
        """Set target object declination to sDD*MM or sDD*MM:SS depending on
        the current precision setting
        Accepts float or sDD:MM or sDD:MM:SS
        Returns:
        1 - Dec Accepted
        0 - Dec invalid"""
        if str(angle).count(':') == 0:
            if self.displayPrecision == "High":
                s = to_lx200_long_angle(angle)  # got a float, convert
            else:
                s = to_lx200_angle(angle)  # got a float, convert
            return self.comPort.CommandBool("Sd", s)
        else:  # a string
            degs, rest = angle.split(':', 1)
            s = "%s%c%s" % (degs, DEG, rest)  # sub the DEG symbol
        if self.displayPrecision == "High" and angle.count(':') == 2:
            return self.comPort.CommandBool("Sd", s)
        elif self.displayPrecision == "Low" and angle.count(':') == 1:
            return self.comPort.CommandBool("Sd", s)
        else:
            return False

    def set_lunar_latitude(self, lat):
        """Sets target object to the specificed selenographic latitude on the Moon.
        Returns 1- If moon is up and coordinates are accepted. sDD*MM
        0 - If the coordinates are invalid"""
        return self.comPort.CommandBool("SE", lat)

    def set_lunar_longitude(self, lon):
        """Sets the target object to the specified selenogrphic longitude on the Moon
        Returns 1 - If the Moon is up and coordinates are accepted. sDDD*MM
        0 - If the coordinates are invalid for any reason."""
        return self.comPort.CommandBool("Se", lon)

    def set_site_longitude(self, angle):
        """Set current site's longitude to DDD*MM an ASCII position string
        Returns:
        0 - Invalid
        1 - Valid"""
        if angle < 0:
            angle += 360
        deg = int(angle)
        angle -= deg
        mins = int(angle * 60)
        long = '%03d%c%02d' % (deg, DEG, mins)

        if not CommandBool('Sg', int):
            raise LX200Error("Invalid longitude: %s" % int)
        else:
            return True

    def set_UTC_offset(self, hours):
        """Set the number of hours added to local time to yield UTC "sHH.H"
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("SG", "%+2.1f" % (hours))

    def set_local_time(self, ltime):
        """Set the local Time "HH:MM:SS"
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("SL", strftime("%H:%M:%S", ltime))

    def set_site_name(self, site, name):
        """Set site name to be <string>. LX200s only accept 3 character strings. Other scopes accept up to 15 characters.
        Returns:
        0 - Invalid
        1 - Valid"""
        if '#' in name:
            raise LX200Error('Site name cannot contain "#"')
        if self.model == "LX200":
            name = name[:3]
        if not self.comPort.CommandBool('S', chr(ord('M') + site - 1), name):
            raise LX200Error("Invalid site name:" + name)
        else:
            return True

    def set_max_elev(self, elev):
        """Set highest elevation to which the telescope will slew - DD
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("So" + str(elev) + "*")

    def set_target_RA(self, angle):
        """Set target object RA to HH:MM.T or HH:MM:SS depending on the current precision setting.
        Angle is a float or HH:MM.T or HH:MM:SS
        Returns:
        0 - Invalid
        1 - Valid"""
        if str(angle).count(':') == 0:
            hrs = int(angle)
            mins = (angle - hrs) * 60.
            secs = (mins - int(mins)) * 60.
        else:
            hrs, mins, secs = angle.split(':')
        if self.displayPrecision == "High":
            return self.comPort.CommandBool(
                "Sr", "%02d:%02d:%02d" %
                (int(hrs), int(mins), int(secs)))
        else:
            return self.comPort.CommandBool(
                "Sr", "%02d:%04.1f" %
                (int(hrs), mins + secs / 60.))

    def set_sideral_time(self, stime):
        """Sets the local sideral time to HH:MM:SS
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("SS", strftime("%H:%M:%S", stime))

    def set_site_latitude(self, angle):
        """Sets the current site latitude to sDD*MM#
        Returns:
        0 - Invalid
        1 - Valid"""
        dms = to_lx200_angle(angle)
        pair = dms.split(' ')
        if not CommandBool('St', pair[0]):
            raise LX200Error("Invalid latitude: %s" % int)
        else:
            return True

    def set_tracking_rate(self, rate):
        """Sets the current tracking rate to TT.T hertz, assuming a model where a 60.0 Hertz synchronous motor will cause the RA
        axis to make exactly one revolution in 24 hours.
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("ST", "%2.1f" % (rate))

    def set_slew_rate(self, N):
        """Set maximum slew rate to N degrees per second. N is the range (2..8)
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("Sw", N)

    def set_target_AZ(self, az):
        """Sets the target Object Azimuth [LX 16" and LX200GPS only]
        Returns:
        0 - Invalid
        1 - Valid"""
        return self.comPort.CommandBool("Sz", az)

    # -------------------------------------------------------------------------------
    # T - Tracking Commands
    # -------------------------------------------------------------------------------
    def track_rate_incr(self):
        """ Increment Manual rate by 0.1 Hz
        Returns: Nothing"""
        self.comPort.CommandBlind("T+")

    def track_rate_dec(self):
        """ Decrement Manual rate by 0.1 Hz
        Returns: Nothing"""
        self.comPort.CommandBlind("T-")

    def track_lunar(self):
        """ Set Lunar Tracking Rate
        Returns: Nothing"""
        self.comPort.CommandBlind("TL")

    def track_custom(self):
        """ Select custom tracking rate
        Returns: Nothing"""
        self.comPort.CommandBlind("TM")

    def track_default(self):
        """ Select default tracking rate
        Returns: Nothing"""
        self.comPort.CommandBlind("TQ")

    def set_manual_track_rate(self, rate):
        """Set Manual rate do the ASCII expressed decimal DDD.DD
        Returns: '1'"""
        return self.comPort.CommandBlind("TD", rate)

    # -------------------------------------------------------------------------------
    # U - Precision Toggle
    # -------------------------------------------------------------------------------
    def precision_toggle(self):
        """ Toggle between low/hi precision positions
        Low - RA displays and messages HH:MM.T sDD*MM
        High - Dec/Az/El displays and messages HH:MM:SS sDD*MM:SS
        Returns Nothing"""
        if self.model == 'LX200':
            raise LX200Error(
                "unsupported model: " +
                self.model +
                " for precision_toggle")
        self.comPort.CommandBlind("U")
        strLen = len(self.comPort.CommandString(self.comPort, 'GA'))
        if strLen > 6:
            self.displayPrecision = "High"
        else:
            self.displayPrecision = "Low"

    def set_precision_type(self, pType):
        """Sets telescope to give various position responses
         No command to check precision, so read something"""
        strLen = len(self.comPort.CommandString(self.comPort, 'GA'))
        if pType == "Low" and strLen > 6:
            self.comPort.CommandBlind('U')
        self.displayPrecision = pType

    # -------------------------------------------------------------------------------
    # W - Site Select
    # -------------------------------------------------------------------------------
    def set_site_num(self, num):
        """Set current site to <n>, an ASCII digit in the range 0..3
        Returns: Nothing"""
        self.comPort.CommandBlind("W", num)

    # -------------------------------------------------------------------------------
    # ? - Help Text Retrieval
    # -------------------------------------------------------------------------------
    def help_start(self):
        """ Set help text cursor to the start of the first line.
        Returns: <string>#
        The <string> contains first string of the general handbox help file."""
        return self.comPort.CommandString("??")

    def help_next(self):
        """ Retrieve the next line of help text
        Returns: <string>#
        The <string> contains the next string of general handbox help file"""
        return self.comPort.CommandString("?+")

    def help_prev(self):
        """ Retreive previous line of the handbox help text file.
        Returns: <string>#
        The <string> contains the next string of general handbox help file"""
        return self.comPort.CommandString("?-")
