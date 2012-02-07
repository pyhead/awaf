import os.path

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

    (r"^/tip/([\d\w]{5})/$", handlers.TipHandler),
    (r"^/tip/([\d\w]{5})/statistics$", handlers.TipHandler),
    # fuck shit this regexp doesnt work XXX
    (r"^/tip/([\d\w]{5})/comments/(\?([^#][\d\w]+))$", handlers.TipCommentsHandler),
    ],
    **settings
)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
