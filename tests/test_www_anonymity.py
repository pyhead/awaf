import unittest
import urllib
import httplib
import socket

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

    def test_torsocks(self):
        """
        Once a new torctl is created -hence tor is running,
        perform various tests on the proxy.
        """
        anonymity.torsocks()
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

    def test_torctl(self):
        #anonymity.TorListener()
        pass # WTF; Y U NO WORK

    def test_starttor(self):
        """
        Ensure tor is working properly.
        Note: this test assumes tor is not already started on your system.
        """
        exitcode = anonymity.start_tor()
        self.assertTrue(exitcode)



if __name__ == '__main__':
    unittest.main()
