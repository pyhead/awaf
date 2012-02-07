"""
Test config modules, working on a new cfg file.
"""
import unittest

from globaleaks.core import config


class TestConfig(unittest.TestCase):
    """
    Performs various tests on the config class.
    """
    _testcfgpath = 'test_cfg.cfg'

    def setUp(self):
        """
        Create a new config file based on the examples.
        """
        cfg = config.Config(self._testcfgpath)

    def tearDown(self):
        """
        Remove the config file.
        """
        try:
            os.remove(self._testcfgpath)
        except OSError:
            pass

