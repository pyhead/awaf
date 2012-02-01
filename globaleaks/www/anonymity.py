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

from globaleaks.www import config


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


@once
def start_tor():
    """
    Start tor daemon in a new process.
    Return tor process' pid in case of success, None whether tor seems already running,
    False otherwise.
    """
    basecmd = ('%(cmd)s -f %(torrc)s --HiddenServiceDir %(hiddir)s '
               '--HiddenServicePort %(hidport)d') % dict(
                    cmd = config.torpath,
                    torrc = config.torrc,
                    hiddir = config.hiddir,
                    hidport = config.hidport,
                    )

    proc = subprocess.Popen(basecmd.split(),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    for line in iter(proc.stdout.readline, ''):
#        print line # XXX: log.debug when logging will be setted.
        if 'Bootstrapped 100%:' in line:
            return proc.pid
        if '[err]' in line:
            return False
    else:
        return proc.pid # proc should have a pid < 0 in case of failure.

@once
def torsocks():
    """
    Change socket.socket to a socksproxy binded to tor proxy.
    """
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "localhost", config.torport)
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
        return no_tor
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

        torsocks()
        cls.torpid = start_tor()
        conn = TorCtl.connect(
                controlAddr='localhost',
                controlPort=config.torctlport,
                passphrase=None
        )

        if conn is not None:
            cls._conn = conn
            conn.set_events(events or ["BW"])
            print 'hehr'
            return object.__new__(cls, *args, **kwargs)
        else:
            return None

    def __nonzero__(self):
        """
        Return True if tor is active and torCtl is currently attached to it,
        False otherwise.
        """
        print self._conn.is_alive()
        return self._conn.is_live()

    def close(self):
        """
        Close tor process and listener.
        """
        if self:
            self._conn.close()
        if hasattr(self, '_pid'):
            os.kill(self._pid, signal.SIGQUIT)
    __del__ = close

    def brandwith_event(self, event):
        """
        Log informations about current brandwidth.
        """

    def logtorevent(self, event):
        """
        Log informations about events on tor stream.
        """

    @property
    def has_hiddenservice(self):
        """
        """
