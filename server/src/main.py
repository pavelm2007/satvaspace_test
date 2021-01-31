import sys

from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import WebSocketServerFactory, listenWS
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from handles import ChatServerProtocol, ChatServerFactory

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = ChatServerFactory('ws://0.0.0.0:8080')
    factory.protocol = ChatServerProtocol

    resource = WebSocketResource(factory)

    # we server static files under '/' ..
    root = File('.')

    # and our WebSocket server under '/ws' (note that Twisted uses
    # bytes for URIs)
    root.putChild(b'ws', resource)

    # both under one Twisted Web Site
    site = Site(root)
    reactor.listenTCP(8080, site)

    reactor.run()
