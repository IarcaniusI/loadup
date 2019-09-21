
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
# import threading
# import tornado.platform.asyncio
# import asyncio
# import tornado.ioloop
from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

import restserver as restserver

if __name__ == "__main__":

#    asyncio.set_event_loop(asyncio.new_event_loop())
    # path to files
    html_path=os.path.join(os.path.dirname(__file__), "html")
    css_path=os.path.join(os.path.dirname(__file__), "css")
    js_path=os.path.join(os.path.dirname(__file__), "js")
    img_path=os.path.join(os.path.dirname(__file__), "img")

    # create web-application with settings
    # cookie_secret - start salt for cookies (must depend from time), static string is bad realization
    # But there are no functions that use cookies in this server
    app = tornado.web.Application( [
            (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": img_path}),
            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': css_path}),
            (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': js_path}),
            (r'/', restserver.MainHandler)
        ], template_path=html_path, cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__" )

    #start HTTP server
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print("WEB Server will start at port {}".format(options.port))
    tornado.ioloop.IOLoop.current().start()
