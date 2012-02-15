import unittest

import tornado.httpserver
import tornado.httpclient
import tornado.ioloop

from www import app
from www import config
from www.anonymity import tor

# start tor
tor.start_tor()
tor.torsocks()

# start tornado server
server = tornado.httpserver.HTTPServer(app.exapp)
server.listen(config.hidport)

class TestWWWApp(unittest.TestCase):
    """
    Test the web application for GlobaLeaks.
    """

    def timed(func):
        """
        Testing on time delays is also important.
        This function provides a decorator for tests which
        needs a lag as short as possible.
        """
        def inner(*args, **kwargs):
            time0 = time.time()
            ret = func(*args, **kwargs)
            time = time.time() - time0

    def setUp(self):
        """
        Build a simple httpclient for testing
        """
        self.client = tornado.httpclient.AsyncHTTPClient()

    def tearDown(self):
        self.client.close()

    def urlfor(self, *page):
        """
        Construct an url using keywords given.
        """
        return 'http://localhost:%d/%s' % (config.hidport, '/'.join(page))

    def handle_request(self, message):
        """
        Callack for handling requests:
        save the message as class attribute, then close the socket.
        """
        self.response = message
        tornado.ioloop.IOLoop.instance().stop()

    def fetch(self, page, method='GET'):
        """
        Fetch an http page using self.client, then store the response to
        self.response.
        """
        self.client.fetch(self.urlfor(page), self.handle_request, method=method)
        tornado.ioloop.IOLoop.instance().start()

    def test_index(self):
        """
        Default index page should be accessible and with something wriitten on it.
        """
        self.fetch('')

        self.assertEqual(self.response.code, 200)
        self.assertEqual(self.response.request.url, self.urlfor(''))
        self.assertNotEqual(self.response.body, '')


    def test_tor_exposed(self):
        """
        An AWAF should be accessible also via its .onion domain.
        """
        onionhname = tor.get_hiddenurl()
        
        self.client.fetch('http://%s:%d/' % (onionhname, config.hidport),
                          self.handle_request)
        tornado.ioloop.IOLoop.instance().start()
        
        self.assertEqual(self.response.code, 200)
        self.assertTrue(self.response.body)


if __name__ == '__main__':
    unittest.main()
