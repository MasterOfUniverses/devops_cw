import main
from tornado.ioloop import IOLoop
main.app.listen(main.namespace.port, address=str(main.namespace.host))
IOLoop.current().start()
