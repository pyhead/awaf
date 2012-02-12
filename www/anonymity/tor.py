"""
Handle the web app anonymity:
    - override socket.socket so that the application will pass though tor proxy;
    - start/stop/receive statistics about the current tor network;
    - create a new hidden node
"""
from __future__ import with_statement

import socket
import subprocess
import logging
import os.path

import socks

from www import config

logger = logging.getLogger('Tor Controller')

__PID = None
@property
def pid(): 
    """
    We are all adults, Guido van Rossum
    Return current tor process id.
    """
    return __PID

@pid.deleter
def delpid():
    """
    __PID should be removed only when the application closes.
    In any case, kill the current tor daemon.
    """
    logger.debug('Killing tor process %d' % __PID)
    os.kill(__PID)

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

def tor_running(func):
    """
    Closure for services requiring tor.
    If tor is active, return function func, None otherwise
    """
    def no_tor(*args, **kwargs):
        return None
    return func if pid else no_tor


@once
def start_tor():
    """
    Start tor daemon in a new process.
    Return tor process' pid in case of success, None whether tor seems already running,
    False otherwise.
    """
    global __PID

    basecmd = ('%(cmd)s -f %(torrc)s --HiddenServiceDir %(hiddir)s '
               '--HiddenServicePort %(hidport)d') % dict(
                    cmd = config.torpath,
                    torrc = config.torrc,
                    hiddir = config.hiddir,
                    hidport = config.hidport,
                    )
    try:
        proc = subprocess.Popen(basecmd.split(),
	                        stdout=subprocess.PIPE,
		                stderr=subprocess.PIPE)
    except OSError:
        logger.error('Unable to lunch command %s. Please edit config' % 
		     config.torpath)
        return None

    for line in iter(proc.stdout.readline, ''):
        logger.debug(line)
        if 'Bootstrapped 100%:' in line:
            __PID = proc.pid
            return proc.pid > 0
        if '[err]' in line:
            return False
    else:
        __PID = proc.pid
        return proc.pid > 0  # proc should have a pid < 0 in case of failure.

@once
def torsocks():
    """
    Change socket.socket to a socksproxy binded to tor proxy.
    If the operation succeeds, return True, 
    """
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "localhost", config.torport)
    socket.socket = socks.socksocket
    return True

@tor_running
def get_hiddenurl():
    """
    Retrive the onion url from hiddenservice directory specified in www.config.
    Raise OSError in case of Failure, 
    None if hiddenservice hostname seems corrupted.
    """
    with open(os.path.join(config.hiddir, 'hostname')) as f:
        url = f.readline().strip()
    return url
