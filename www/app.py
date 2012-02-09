"""
Simple Anonymous Web application Template.
"""
import tornado.ioloop

from www import config, handlers

settings = dict(
        static_path = config.staticpath,
)

# a anonymous application should have at least 
# these small configurable components
application = tornado.web.Application([
    (r"^/$", handlers.IndexHandler),
    (r"^/info/$", handlers.InfoHandler),
    (r"^/stats/$", handlers.StatsHandler),
    ],
    **settings
)

if __name__ == '__main__':
    from www.anonymity import tor
    tor.torsocks()
    tor.start_tor()
    application.listen(config.hidport)
    tornado.ioloop.IOLoop.instance().start()
