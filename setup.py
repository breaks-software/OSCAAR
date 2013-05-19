# -*- coding: utf-8 -*-

""" Made by Luuk Visser, University of Leiden and Delft University of 
    Technology. Initial version (5-19-2013). """
    
import os
import sys
import shutil
from setuptools import setup
import subprocess
import atexit

""" Checking for all required packages and if these are recent enough """
minimum_numpy_version = "1.6"
minimum_matplotlib_version = "1.0"
minimum_pyfits_version = "2.4.0" # lower versions may work (not tested)
minimum_scipy_version = "0.10" # lower versions may work (not tested)
minimum_wxpython_version = "2.0" # lower versions may work (not tested)

""" Currently only Python 2.7.x is supported """
if sys.version_info[:2] != (2, 7):
    raise RuntimeError("must use python 2.7.x")

try:
    import numpy as np
except:
    raise RuntimeError("Numpy not found")
if np.__version__ < minimum_numpy_version:
    print("*Error*: NumPy version is lower than needed: %s < %s" %
          (np.__version__, minimum_numpy_version))
    sys.exit(1)

try:
    import scipy
except:
    raise RuntimeError("Scipy not found")
if scipy.__version__ < minimum_scipy_version:
    print("*Error*: Scipy version is lower than needed: %s < %s" %
          (scipy.__version__, minimum_scipy_version))
    sys.exit(1)  
    
try:
    import matplotlib
except:
    raise RuntimeError("matplotlib not found")
if matplotlib.__version__ < minimum_matplotlib_version:
    print("*Error*: matplotlib version is lower than needed: %s < %s" %
          (matplotlib.__version__, minimum_matplotlib_version))
    sys.exit(1)
    
try:
    import pyfits
except:
    raise RuntimeError("PyFITS not found")
if pyfits.__version__ < minimum_pyfits_version:
    print("*Error*: PyFITS version is lower than needed: %s < %s" %
          (pyfits.__version__, minimum_pyfits_version))
    sys.exit(1)  
    
try:
    import wxPython
except:
    raise RuntimeError("wxPython not found")
if wxPython.__version__ < minimum_wxpython_version:
    print("*Error*: wxPython version is lower than needed: %s < %s" %
          (wxPython.__version__, minimum_wxpython_version))
    sys.exit(1)  
  
""" Walk through the subdirs and add all non-python scripts to MANIFEST.in """
def create_manifest():    
    print 'creating manifest.in'
    matches = []
    for root, dirnames, filenames in os.walk('oscaar'):
        if ('.git' in str(root)) == False:
            for filename in filenames:
                if filename.endswith(('.py', '.pyc')) == False:
                  matches.append(os.path.join(root, filename))
    
    with open('MANIFEST.in', 'w') as f:
        f.writelines(("include %s\n" % l.replace(' ','?') for l in matches))
    
""" To remove the manifest file after installation """
def delete_manifest():
    if os.path.exists('MANIFEST.in'):
        os.remove('MANIFEST.in')
    
""" Create list for Python scripts directories to include """
def get_packages():
    print 'searching for packages'
    matches = []
    for root, dirnames, filenames in os.walk('oscaar'):
        if ('.git' in str(root)) == False:
            for filename in filenames:
                if filename.endswith(('.py', '.pyc')) == True:
                    matches.append(root)
    matches = list(set(matches))
    return matches
    
def del_dir(dirname):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    
""" The setup configuration for installing OSCAAR """
def setup_package():
    create_manifest()
    setup(
        name = "OSCAAR",
        version = "2.0prebeta",
        author = "Core Developer: Brett Morris. Contributors: Daniel Galdi, Nolan Matthews, Sam Gross, Luuk Visser",
        author_email = "oscaarUMD@gmail.com",
        description = ("oscaar is an open source project aimed at helping you begin to study transiting extrasolar planets with differential photometry."),
        license = 'LICENSE',
        keywords = "oscaar transit astronomy photometry exoplanets",
        url = "https://github.com/OSCAAR/OSCAAR/wiki",
        packages=get_packages(),
        include_package_data = True,
        zip_safe = False,
        long_description=open(os.path.join(os.path.dirname(__file__),'oscaar','README')).read(),
        download_url='https://github.com/OSCAAR/OSCAAR/archive/master.zip',
        classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: C',
          'Programming Language :: Python :: 2.7',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics'
      ],
    )

def to_do_at_exit():
    delete_manifest()
    del_dir('build')
    del_dir('dist')
    del_dir('OSCAAR.egg-info')
        
    'Installation finished. Starting DS9 downloader and C code builder'
    subprocess.Popen(['python', 'post_setup.py'])
    
atexit.register(to_do_at_exit)
    
if __name__ == '__main__':
    setup_package()