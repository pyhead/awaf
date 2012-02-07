import unittest
import urllib
import httplib
import socket
import os

import tornado.web

from www.anonymity import tor

class TestTor(unittest.TestCase):
    """
    Tests tor processing works and tor controller handles events correctly.
    """

    def test_start_tor(self):
	"""
	Test a new tor instance, assuming tor is not running.
	"""
	self.assertTrue(tor.start_tor())
	self.assertIsNone(tor.start_tor())

	# TODO: do something in order to kill the process and restart it?
        
	# brutally reset start_tor.has_run
        tor.start_tor.has_run = False
        self.assertFalse(tor.start_tor())
        # once started, tor_start should return none everytime.
        self.assertIsNone(tor.start_tor())
	self.assertIsNone(tor.start_tor())

    def test_torsocks(self):
        """
        Once a new torctl is created -hence tor is running,
        perform various tests on the proxy.
        """
	self.assertTrue(tor.torsocks())
        
	try:
            urllib.urlopen('http://globaleaks.org')
        except IOError, e:
            self.fail("Unable to connect: <%s>" % str(e))


        conn = urllib.urlopen('http://check.torproject.org')
        for line in conn:
            if 'Sorry. You are not using Tor' in line:
                self.fail('Tor not running.')
            elif 'Congratulations. Your browser is configured to use Tor' in line:
                break
        else:
            self.fail('Unable to determine tor status.')

        # ensure re-calling this funciton does not have side-effects
        self.assertIsNone(tor.torsocks())
        # changes on socket should affect every library socket based.
        try:
            conn = httplib.HTTPConnection('globaleaks.org')
            conn.request('GET', '/index.html')
        except socket.gaierrror, e:
            self.fail('Unable to connect: <%s>' % str(e))


class TestTorListener(unittest.TestCase):
    """
    Test tor interface for event listeners.
    """
    
    def setUp(self):
	"""
	Set up a simple torctl listener.
	"""
	self.tor_listener = tor.TorListener()

    def test_tor_running(self):
	"""
	Test tor_running decorator.
	"""

	@tor.tor_running
	def inner(cheese):
	    """
	    Useless function which returns its argument
	    """
	    return cheese

	self.assertEqual(inner('cheese'), 'cheese')

	#TODO: stop tor and see if it works.

    def test_bool(self):
	"""
	Assert the connection with tor is alive.
	"""
	self.assertTrue(self.tor_listener)
	self.tor_listener.close()
	self.assertFalse(self.tor_listener)
    

if __name__ == '__main__':
    unittest.main()
