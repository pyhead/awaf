import unittest
import urllib

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
            self.fail(str(e))


        conn = urllib.urlopen('http://check.torproject.org')
        for line in conn:
            if 'Sorry. You are not using Tor' in line:
                self.fail('Tor not running.')
            elif 'Congratulations. Your browser is configured to use Tor' in line:
                break
        else:
            raise NotImplementedError

        # ensure re-calling this funciton does not have side-effects
        anonymity.torsocks()


if __name__ == '__main__':
    unittest.main()
