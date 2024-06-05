#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Name:        run_lx.py
# Purpose:     General access to and use of LX200 telescopes and accesories
#
# Author(s):   R J Schumacher
#
# Created:     2007/11/11
# Copyright:   none
# Licence:     LGPL
# 
#-----------------------------------------------------------------------------
"""
>> run_lx.py --ra=14:33:33 --dec=+27:55:55 --rate=FIND --port=0
- rate is one of [GUIDE,CENTRE,FIND,MAX]
- port is the port name for your system: 
    can be int: [0,...], or alpha: "COMn" 
- default precision_type == 'High'
"""

import sys
from LX200 import *

    
def main():
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['ra=','dec=','rate=','port='])
    except getopt.error, msg:
        print msg
        return
    if len(opts)<4:
        print "Script usage:", __doc__
        print 
        print "You entered:", opts
        print "Command argument list:", sys.argv
        return
        
    for opt, arg in opts:
        if opt == '--ra':
            targetRA = arg
        elif opt == '--dec':
            targetDEC = arg
        elif opt == '--rate':
            slewRate = arg
        elif opt == '--port':
            portName = arg
    print "\nStarting..."
    #port = LXSerial(debug=True) ## to test without a scope connected
    port = LXSerial(debug=False) ## an LX200 must be on and connected!
    port.connect(portName)
    scope = Telescope(port, "LX200", debug=True) 
    scope.set_precision_type('High')
    
    scope.set_target_RA(targetRA) ## uses decimal notation
    scope.set_target_DEC(targetDEC)  ## uses decimal notation
    
    scope.set_slew_rate(slewRate)
    
    #scope.set_site(1)
    #scope.set_align_mode("P")
    #raw_input("do your alignment, then press enter ")

    #scope.set_pointing_mode('HIGH PRECISION')
    #library = Library(port, scope)
    #library.set_M_object(101)

    # etc...
    port.close()


if __name__ == '__main__':
    main()