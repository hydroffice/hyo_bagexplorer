"""
Hydro-Package
BAG Explorer
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

__version__ = '0.2.4.dev1'
__doc__ = 'BAG Explorer'
__author__ = 'gmasetti@ccom.unh.edu, brc@ccom.unh.edu'
__license__ = 'BSD-like license'
__copyright__ = 'Copyright 2015 Giuseppe Masetti, Brian R. Calder (CCOM/JHC, UNH)'


# def hyo():
def hyo_app():
# def hyo_lib():
    return __doc__, __version__
