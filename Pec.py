#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Name:        Pec.py
# Purpose:     LX200 telescope periodic error correction
#
# Author(s):   R J Schumacher
#
# Created:     2006/01/28
# RCS-ID:      $Id: Pec.py $
# Copyright:   (c) 2006
# Licence:     LGPL
#
# -----------------------------------------------------------------------------


class Pec:
    """LX200 class for periodic error correction
    """

    def __init__(self, comPort, debug=False):
        """Constructor.
        """
        self.comPort = comPort

    def pec_train(self, clear=False):
        """ accumulate and save to disk pec errors - polar mode
        average over sessions a-la LX200 function, or clear and start new
        """
        align_res = self.get_alignment()
        if align_res != "P":
            raise LX200Error("unsupported mode: " + align_res + " for pec")
        return True

    def pec(self):
        """ apply pec
        """
        align_res = self.get_alignment()
        if align_res != "P":
            raise LX200Error("unsupported mode: " + align_res + " for pec")
        return True
