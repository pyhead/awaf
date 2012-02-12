"""
Simple Anonymous Web application Template.
"""
import logging

import tornado.ioloop

from www import config, handlers
from www.anonymity import tor
from www.node import Node

stdsett = dict(
        static_path = config.staticpath,
)

node = Node(
     name = 'Globaleaks 0.2',
     title = 'Almudena edition',
     description = 'Fooo',
     type='gangbang',
)

# an anonymous application should have at least 
# these small configurable components
exapp = tornado.web.Application([
    (r"^/$", handlers.IndexHandler),
    (r"^/info/$", handlers.InfoHandler(node)),
    (r"^/stats/$", handlers.StatsHandler(node)),
    ],
    **stdsett
)
exapp.hidhostname = tor.get_hiddenurl()

def main(application):
    """
    Simple main which starts the application and
    TODO: provides a simple list of arguments.
    """
    # set up the logger. Be careful with these, we do not expect to have logs.
    logging.basicConfig(
        format = config.logformat,
        level = logging.DEBUG,
    )

    # start tor
    tor.torsocks()
    tor.start_tor()

    # launch web app    
    try:
        application.listen(config.hidport)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        # quit with exitcode 1
        exit(1)


if __name__ == '__main__':
    main(exapp)
