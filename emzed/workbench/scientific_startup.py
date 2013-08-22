
# -*- coding: utf-8 -*-
#
# Copyright © 2011 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see spyderlib/__init__.py for details)

"""
Scientific Python startup script

Requires NumPy, SciPy and Matplotlib
"""
import emzed.config

if emzed.config._is_first_start():
    emzed.config.edit()
#
import emzed.updaters
 
import emzed.db
emzed.db.init_pubchem() # registers updater

emzed.updaters.check_emzed_updates()
emzed.updaters.print_update_status()

import emzed.abundance
import emzed.adducts
import emzed.align
import emzed.batches
import emzed.core
import emzed.db
import emzed.elements
import emzed.gui
import emzed.stats
import emzed.utils

# from __future__ import division

#print "load patched scientific startup"

# Pollute the namespace but also provide MATLAB-like experience:
#from pylab import *  #analysis:ignore

# Enable Matplotlib's interactive mode:
#ion()

# Import modules following official guidelines:
#import numpy as np
#import scipy as sp
#import matplotlib as mpl
#import matplotlib.pyplot as plt  #analysis:ignore

#print ""
#print "Imported NumPy %s, SciPy %s, Matplotlib %s" %\
      #(np.__version__, sp.__version__, mpl.__version__),

#import emzed.core

import external_shell_patches
external_shell_patches.patch_external_shell()

from emzed.core.explorers import inspect

a = emzed.utils.toTable("a", [1,2,3])

import os
if os.environ.get('QT_API') != 'pyside':
    try:
        import guiqwt
        import guiqwt.pyplot as plt_
        import guidata
        plt_.ion()
        print "+ guidata %s, guiqwt %s" % (guidata.__version__,
                                           guiqwt.__version__)
    except ImportError:
        print
else:
    print

def setscientific():
    """Set 'scientific' in __builtin__"""
    import __builtin__
    from site import _Printer
    infos = """\
This is a standard Python interpreter with preloaded tools for scientific 
computing and visualization:

>>> import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)
>>> import scipy as sp  # SciPy (signal and image processing library)

>>> import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
>>> import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax
>>> from pylab import *              # Matplotlib's pylab interface
>>> ion()                            # Turned on Matplotlib's interactive mode
"""
    try:
        import guiqwt  #analysis:ignore
        infos += """
>>> import guidata  # GUI generation for easy dataset editing and display

>>> import guiqwt                 # Efficient 2D data-plotting features
>>> import guiqwt.pyplot as plt_  # guiqwt's pyplot: MATLAB-like syntax
>>> plt_.ion()                    # Turned on guiqwt's interactive mode
"""
    except ImportError:
        pass
    infos += """
Within Spyder, this interpreter also provides:
    * special commands (e.g. %ls, %pwd, %clear)
    * system commands, i.e. all commands starting with '!' are subprocessed
      (e.g. !dir on Windows or !ls on Linux, and so on)
"""
    __builtin__.scientific = _Printer("scientific", infos)

setscientific()
del setscientific
