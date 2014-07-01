#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cb CLI

Usage:
  cb init [-p <path>]
  cb new -t <title> -c <category> [-f <file>]
  cb build [--delete]
  cb server
  cb -h | --help
  cb -V | --version

Options:
  -h, --help             Help information.
  -V, --version          Show version.
  -c <category>          Specify the category.
  -t <title>             Specify the new post title.
  -f <file>              Specify the new post filename.
  -p <path>              Destination path.
  --delete               Delete the contents of output directory before generate.

"""

import os
import logging

from docopt import docopt

from cb import __version__
from cb.log import logging_init

logger = logging.getLogger(__name__)


def main():
    logging_init(logging.DEBUG)
    # Get input info from docopt.
    args = docopt(__doc__, version='cb {}'.format(__version__))

    # Init the blog codes.
    if args['init']:
        # The generated blog code's path.
        blog_root_path = args['-p'] if args['-p'] else os.getcwd()

    # Start a web server to debug.
    elif args['server']:
        pass

    # Build the source.
    elif args['build']:
        pass

    # Post a new md.
    elif args['new']:
        pass

    logger.info('Done.')


if __name__ == '__main__':
    main()
