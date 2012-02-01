"""
Anonymous Web Application Configuration.

Do not Change these unless you know what you are doing, fool.
"""
import os.path


basepath, _ = os.path.dirname(os.path.abspath(__file__)).rsplit('globaleaks', 1)

# tor configuration
torpath = '/Applications/TorBrowser_en-US.app/Contents/MacOS/tor'
torrc = os.path.join(basepath, 'tor', 'torrc')
torport = 9050
torctlport = 9051
hiddir = os.path.join(basepath, 'tor', 'hiddenservice')
hidport = 80

# web application
staticpath = os.path.join(basepath, 'static')
