import unittest
import urllib
import httplib
import socket
import os

import tornado.web

from globaleaks.www import anonymity

class TestAnonimity(unittest.TestCase):
    """
    Test hidden service and tor socket works.
    """
    def setUp(self):
        """
        Create a new TorCtl.
        """
        self.tor = anonymity.TorListener()

    def tearDown(self):
        """
        Delete current TorCtl instance.
        """
        del self.tor

    def test_torctl(self):
        # tor controller should be up and running
        self.assertTrue(bool(self.tor))


    def test_start_tor(self):
        """
        Ensure tor is working properly.
        Note: this test assumes tor is not already started on your system.
        """
        # brutally reset start_tor.has_run
        anonymity.start_tor.has_run = False

        pid = anonymity.start_tor()
        self.assertTrue(pid and pid > 0) # pid < 0 in case of failure
        self.assertIsNone(anonymity.start_tor())

        os.kill(pid, signal.SIGKILL)


        self.assertIsNone(anonymity.start_tor())
        # once started, tor_start should return none everytime.
        self.assertIsNone(anonymity.start_tor())

    def test_torsocks(self):
        """
        Once a new torctl is created -hence tor is running,
        perform various tests on the proxy.
        """
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
        anonymity.torsocks()
        # changes on socket should affect every library socket based.
        try:
            conn = httplib.HTTPConnection('globaleaks.org')
            conn.request('GET', '/index.html')
        except socket.gaierrror, e:
            self.fail('Unable to connect: <%s>' % str(e))


if __name__ == '__main__':
    unittest.main()
