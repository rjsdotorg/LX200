#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Name:        LXGPS.py
# Purpose:     General access to and use of LX200GPS and GPS accesories
#
# Author(s):   R J Schumacher
#
# Created:     2006/01/28
# RCS-ID:      $Id: LXGPS.py $
# Copyright:   (c) 2006
# Licence:     LGPL
# 
#-----------------------------------------------------------------------------
import time

class LXGPS:
    """LX200 class for GPS and properties 
    TO DO: implement the NAK wait
    
    """
    
    def __init__(self, comPort, debug=False):
        """Constructor.
        """
        self.comPort = comPort

    def __repr__(self):
        """Return a representation string.
        """
        return "<LX200 GPS instance>"

    #-------------------------------------------------------------------------------        
    # B - Active Backlash Compensation
    #-------------------------------------------------------------------------------        
    
    def set_dec_backlash(self, seconds): 
        """Set Altitude/Dec Antibacklash
        Returns Nothing"""
        if self.model!='LX200GPS':
            raise LX200Error("unsupported model: "+self.model+" for active backlash  ")
        self.comPort.CommandBlind("$BA", abs(seconds))
    
    def set_ra_backlash(self, seconds): 
        """Set Azimuth/RA Antibacklash
        Returns Nothing"""
        if self.model!='LX200GPS':
            raise LX200Error("unsupported model: "+self.model+" for active backlash  ")
        self.comPort.CommandBlind("$BZ", abs(seconds))
    

   
    #-------------------------------------------------------------------------------        
    # g - GPS/Magnetometer commands
    #-------------------------------------------------------------------------------        
    def GPS(self, state="on", data=None):
        if self.model=='LX200GPS': 
            if state=="on": self.GPS_on()
            else: self.GPS_off()
        else:
            ##attempt to use a connected GPS
            pass
        return
    
    def GPS_on(self): 
        """ LX200GPS Only - Turn on GPS
        Returns: Nothing"""
        if self.model=='LX200GPS': 
            self.comPort.CommandBlind("g+")
    
    def GPS_off(self): 
        """ LX200GPS Only - Turn off GPS"""
        if self.model=='LX200GPS': 
            self.comPort.CommandBlind("g-")
    
    def get_GPS_data(self): 
        """ LX200GPS Only - Turns on NMEA GPS data stream.
        Returns: The next string from the GPS in standard NEMA format followed by a '#' key"""
        if self.model=='LX200GPS': 
            return self.comPort.CommandString("gps")
    
    def get_GPS_time(self): 
        """ Powers up the GPS and updates the system time from the GPS stream. 
        The process my take several minutes to complete.
        During GPS update, normal handbox operations are interrupted. [LX200gps only]
        Returns: '0' In the event that the user interrupts the process, or the GPS times out.
        Returns: '1' After successful updates"""
        if self.model=='LX200GPS': 
            return self.comPort.CommandBool("gT")
        else:
            ##attempt to use a connected GPS
            pass
 
    def version_info(self):
        if self.model!='LX200GPS':
            raise LX200Error("unsupported model: "+self.model+" for version")
        return "%s (ver. %s -- %s %s)" % (self.get_product_name(), 
                                          self.get_firmware_num(), 
                                          self.get_firmware_date(), 
                                          self.get_firmware_time())
 
    def version_info_list(self):
        return [self.get_product_name(),
                self.get_firmware_num(),
                self.get_firmware_date(),
                self.get_firmware_time()]

    def get_firmware_date(self): 
        """ Get Telescope Firmware Date
        Returns: mmm dd yyyy# """
        if self.model!='LX200GPS':
            raise LX200Error("unsupported model: "+self.model+" for version")
        return self.comPort.CommandString("GVD")
    
    def get_firmware_num(self): 
        """ Get Telescope Firmware Number
        Returns: dd.d#"""
        if self.model!='LX200GPS':
            raise LX200Error("unsupported model: "+self.model+" for version")
        return self.comPort.CommandString("GVN")
    
    def get_product_name(self): 
        """ Get Telescope Product Name
        Returns: <string>#"""
        if self.model!='LX200GPS':
            raise LX200Error("unsupported model: "+self.model+" for version")
        return self.comPort.CommandString("GVP")
    
    def get_firmware_time(self):
        """ Get Telescope Firmware Time
        returns: HH:MM:SS#""" 
        if self.model!='LX200GPS':
            raise LX200Error("unsupported model: "+self.model+" for version")
        return self.comPort.CommandString("GVT")
    
    #-------------------------------------------------------------------------------        
    # h - Home Position Commands
    #-------------------------------------------------------------------------------        
    def sleep(self, t=None): 
        """ LX200GPS only: Sleep Telescope. Power off motors, encoders, displays and lights. Scope
        remains in minimum power mode until a keystroke is received or a wake command is sent.
        Takes optional param time in seconds"""
        self.comPort.CommandBlind("hN")
        if t is not None:
            time.sleep(t)
            self.wake()

    def wake(self): 
        """ LX200 GPS Only: Wake up sleeping telescope."""
        self.comPort.CommandBlind("hW")

    #---------------------------------------------------------------------------    
    #I - Initialize Telescope Command
    #---------------------------------------------------------------------------    
    def restart(self): 
        """ LX200 GPS Only - Causes the telescope to cease current operations 
        and restart at its power on initialization."""
        self.comPort.CommandBlind("I")
        
    #-------------------------------------------------------------------------------        
    # Q- Smart Drive Control
    #------------------------------------------------------------------------------- 
    def toggle_smart_PEC(self):
        """Toggles Smart Drive PEC on and off for both axis
        Returns: Nothing
        Not supported on Autostar"""
        self.comPort.CommandBlind("$Q")
    
    def enable_DEC_PEC(self): 
        """  Enable Dec/Alt PEC [LX200gps only]
        Returns: Nothing"""
        self.comPort.CommandBlind("$QA+")
    
    def disable_DEC_PEC(self): 
        """  disable Dec/Alt PEC [LX200gps only]
        Returns: Nothing"""
        self.comPort.CommandBlind("$QA-")
    
    def enable_RA_PEC(self): 
        """  Enable RA/AZ PEC compensation [LX200gps only]
        Returns: Nothing"""
        self.comPort.CommandBlind("$QZ+")
    
    def disable_RA_PEC(self): 
        """  Disable RA/AZ PEC Compensation [LX200gpgs only]
        Return: Nothing""" 
        self.comPort.CommandBlind("$QZ-")
        
   
    #-------------------------------------------------------------------------------        
    # R - Slew Rate Commands
    #-------------------------------------------------------------------------------        
    def set_guide_rate(self, rate): 
        """Set guide rate to +/- SS.S to arc seconds per second. This rate is added to or subtracted from the current tracking
        Rates when the CCD guider or handbox guider buttons are pressed when the guide rate is selected. Rate shall not exceed
        sidereal speed (approx 15.0417"/sec)[ LX200GPS only]
        Returns: Nothing"""
        self.comPort.CommandBlind("Rg", rate)
    
    def set_RA_slew_rate(self, rate): 
        """Set RA/Azimuth Slew rate to DD.D degrees per second [LX200GPS Only]
        Returns: Nothing"""
        self.comPort.CommandBlind("RA", rate)
            
    def set_DEC_slew_rate(self, rate): 
        """Set Dec/Elevation Slew rate to DD.D degrees per second [ LX200GPS only]
        Returns: Nothing"""
        self.comPort.CommandBlind("RE", rate)

    #-------------------------------------------------------------------------------        
    # Appendix A: LX200GPS Command Extensions
    #-------------------------------------------------------------------------------        
    def auto_align(self): 
        """ Automatically align scope"""
        self.comPort.CommandBlind("Aa")
    
    def set_DEC_backlash(self, dd): 
        """ Set Altitude/Dec Antibacklash"""
        self.comPort.CommandBlind("$BA", dd)
    
    def set_RA_backlash(self, dd): 
        """ Set Azimuth/RA Antibacklash"""
        self.comPort.CommandBlind("$BZ", dd)
    
    def reticule_duty(self, n): 
        """ Programmable Reticule Duty Cycle"""
        self.comPort.CommandBlind("BD", n)
    
    def GPS_on(self): 
        """ Turn on GPS power"""
        self.comPort.CommandBlind("g+")
    
    def GPS_off(self): 
        """ Turn off GPS power"""
        self.comPort.CommandBlind("g-")
    
    def TO_DO(self): 
        """ Stream GPS data"""
        self.comPort.CommandBlind("gps")
    
    def update_time(self): 
        """ Updates Time of Day from GPS"""
        self.comPort.CommandBlind("gT")
    
    def init_scope(self): 
        """ Initialize Telescope"""
        self.comPort.CommandBlind("I")
    
    def enable_RA_PEC(self): 
        """ RA PEC Enable"""
        self.comPort.CommandBlind("$QZ+")
    
    def disable_RA_PEC(self): 
        """ RA PEC Disable"""
        self.comPort.CommandBlind("$QZ-")
    
    def enable_DEC_PEC(self): 
        """ Dec PEC Enable"""
        self.comPort.CommandBlind("$QA+")
    
    def deisable_DEC_PEC(self): 
        """ Dec PEC Disable"""
        self.comPort.CommandBlind("$QA-")
    
    def set_RA_slew_rate(self, r): 
        """ Programmable Slew Rates"""
        self.comPort.CommandBlind("RA", r)
    
    def set_DEC_slew_rate(self, r): 
        """ Programmable Slew Rates"""
        self.comPort.CommandBlind("RE", r)
    
    def set_guide_rate(self, r): 
        """ Programmable Guiding Rates"""
        self.comPort.CommandBlind("Rg", r)
    
    def set_baud_rate(self, r): 
        """ Set Baud Rate"""
        self.comPort.CommandBlind("SB", r)
        