Description
===========
The  anonymous web application framework goal is to provide a web  application
environment that automatically publish itself to the Tor  network as a Tor
Hidden Service.


Functionalities
================
The  default web application built within the Anonymous Web Application
framework include several functionalities available trough a  minimalistic web
interface:
- Tor Hidden Service Setup
GlobaLeaks relies on Tor Hidden Services for exposing itself to the internet.
Tor can be configured to automatically create a Tor Hidden Service at startup.
The web application automatically detect if Tor has properly setup a Tor Hidden
Service and read it's .onion domain name.
- Tor Startup
The application let the user to see the status of Tor, to stop/start/restart it
- Tor Configuration
The application let the user edit the default Tor configuration file, save it.
- Tor Hidden Service reachability test
The  application let the user check if the Tor Hidden Service is properly
reachable by making a an outgoing connection and seeing as a Tor client  that
the Tor Hidden Service is working properly (make sure that the Tor  HS is
published
to the DA, by default this is done every 10 minutes, but can be tweaked to be
less).
- Tor2web publishing
Tor Hidden Services are automatically exposed trough the internet by the Tor2web
project (http://www.tor2web.org).
The  node by default is automatically exposed to via Tor2web, must it must  be
possible to disable inbound connection coming from Tor2web.
The web application let the user to disable/re-enable inbound connections via
Tor2web.
Tech: This can be done by looking at the X-Tor2web: HTTP header
- Configure Bind Address
The application let the user define the bind address of the application.
By default the application only bind to 127.0.0.1 but it may be possible to bind
it also on other IP address or 0.0.0.0 .
- User interface
The status of the node and the setup procedure should be configurable from a
user interface.
We  should figure out the best way to present this, but at least insert  into
the application logic the fact that the user will be guided through
a wizard to setup their node. They will also be shown the current status of the
node.
- Browser Startup
The application when started and initiatlized must automatically open the system
browser on http://localhost:8080 (or other port where the tornadoweb listen)


Build System
============

Creating a simple .exe/.app/.deb one-click installer should be done using
pyInstaller.
- http://www.pyinstaller.org/
