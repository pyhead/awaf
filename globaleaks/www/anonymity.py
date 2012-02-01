"""
Handle the web app anonymity:
    - override socket.socket so that the application will pass though tor proxy;
    - start/stop/receive statistics about the current tor network;
    - create a new hidden node
"""
import socket
import os.path
import subprocess

import socks
from torctl import TorCtl

from globaleaks import basepath

_torpath = '/Applications/TorBrowser_en-US.app/Contents/MacOS/tor'
_torport = 9050


def once(func):
    """
    Closure for functions that should run only once.
    """
    def decorator(*args, **kwargs):
        if not func.has_run:
            func.has_run = True
            return func(*args, **kwargs)

    func.has_run = False
    return decorator


#@tor_running
@once
def start_tor():
    """
    Start tor daemon in a new process.
    Return True in case of success, None whether tor seems already running,
    Flase otherwise.
    """
    basecmd = ('%(cmd)s -f %(torrc)s --HiddenServiceDir %(hiddir)s '
               '--HiddenServicePort %(hidport)d') % dict(
                    cmd = _torpath,
                    torrc = os.path.join(basepath, '..', 'tor', 'torrc'),
                    hiddir = os.path.join(basepath, '..', 'tor', 'hiddenservice'),
                    hidport = 80,)

    proc = subprocess.Popen(basecmd.split(),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    for line in iter(proc.stdout.readline, ''):
        if 'Bootstrapped 100%:' in line:
            return True
        if '[err]' in line:
            return False
    else:
        return proc.pid > 0 # proc should have a pid < 0 in case of failure.

@once
def torsocks():
    """
    Change socket.socket to a socksproxy binded to tor proxy.
    """
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "localhost", _torport)
    socket.socket = socks.socksocket


def tor_running(func):
    """
    Closure for services requiring tor.
    If tor is active, return function funct, none otherwise
    """
    def no_tor(*args, **kwargs):
        return None

    conn = TorCtl.connect()
    if not conn:
        return
    else:
        conn.close()
        return func

class TorListener(object, TorCtl.PostEventListener):
    """
    Listener for tor events.
    """

    def __new__(cls, events=None, *args, **kwargs):
        """
        Before creating a new socket, we must check tor daemon is active, and
        otherwise lauch it.

        Return a new socketobject, None if launching tor daemon failed.
        """
        conn = TorCtl.connect(controlPort=_torport)

        if not conn and not start_tor():
            return None
        else:
            cls._conn = conn
            conn.set_events(events or ["BW"])
            return super(cls, TorCtl.EventListener).__new__(*args, **kwargs)

    def brandwith_event(self, event):
        """
        Log informations about current brandwidth.
        """

    def logtorevent(self, event):
        """
        Log informations about events on tor stream.
        """

    @property
    def running(self):
        return self._conn.is_alive()

    @property
    def has_hiddenservice(self):
        """
        """

