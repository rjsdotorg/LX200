#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Name:        LX200Error.py
# Purpose:     LX200 Exception handling
#
# Author(s):   R J Schumacher
#
# Created:     2006/01/28
# RCS-ID:      $Id: LX200Error.py $
# Copyright:   (c) 2006
# Licence:     LGPL
# 
#-----------------------------------------------------------------------------
       
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class LX200Error(Error): 
    """Exception raised for telescope specific errors

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    pass
    #def __init__(self, message):
        #self.expression = expression
        #self.message = message
