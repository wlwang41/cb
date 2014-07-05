#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

import os
import sys
import logging
import SimpleHTTPServer
import SocketServer

from cb.tools import check_path_exists

logger = logging.getLogger(__name__)


class Reuse_TCPServer(SocketServer.TCPServer):
    allow_reuse_address = True


def preview(path, port=8000):
    if check_path_exists(path):
        os.chdir(path)
    else:
        logger.error("Path {} not exists".format(path))
    try:
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = Reuse_TCPServer(("", port), Handler)
    except OSError as e:
        logger.error("Could not listen on port {}".format(port))
        sys.exit(getattr(e, 'exitcode', 1))

    logger.info("Serving at port {}".format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt as e:
        logger.info("Shutting down server")
        httpd.socket.close()

if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    logger.debug("Testing server feature...")

    if len(sys.argv) == 3:
        path = os.path.realpath(sys.argv[1])
        port = int(sys.argv[2])
    elif len(sys.argv) == 2:
        path = os.path.realpath(sys.argv[1])
        port = 8000
    else:
        path = os.path.realpath("html")
        port = 8000

    preview(path, port)
