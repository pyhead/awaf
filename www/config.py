"""
Anonymous Web Application Configuration.

Do not Change these unless you know what you are doing, fool.
"""
import os.path
import logging

basepath = os.path.dirname(os.path.abspath(__file__)).rsplit('www', 1)[0]

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
logging.basicConfig(format=logformat)
