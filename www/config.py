"""
Anonymous Web Application Configuration.

Do not Change these unless you know what you are doing, fool.
"""
import os.path
import logging
import sys

basepath = os.path.dirname(os.path.abspath(__file__)).rsplit('www', 1)[0]

# extend pythonpath with www/ and site-packages/
sys.path.append(os.path.join(basepath, 'www'))
sys.path.append(os.path.join(basepath, 'site-packages'))

# tor configuration
torpath = 'tor'
torrc = os.path.join(basepath, 'tor', 'torrc')
torport = 9050
torctlport = 9051
hiddir = os.path.join(basepath, 'tor', 'hiddenservice')
hidport = 8888

# web application
staticpath = os.path.join(basepath, 'static')

# logging
logformat = '%(levelname)s: %(name)s: %(message)s'
