#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cb CLI

Usage:
  cb init [-p <path>]
  cb new -t <title> -c <category> [-f <file>]
  cb build [-s <files> ...]
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
  -s <files>             Specify the files to build.

"""

import os
import logging

from docopt import docopt

from cb import __version__
from cb.log import logging_init
from cb.commands import (
    Command, init, server
)

logger = logging.getLogger(__name__)


def main():
    logging_init(logging.DEBUG)
    # Get input info from docopt.
    args = docopt(__doc__, version='cb {}'.format(__version__))

    # Init the blog codes.
    if args['init']:
        # The generated blog code's path.
        blog_root_path = args['-p'] if args['-p'] else os.getcwd()
        init(blog_root_path)
        logger.info('Init your blog.')
        return

    command = Command(os.path.join(os.getcwd(), '_config.yml'))

    # Start a web server to debug.
    if args['server']:
        server(os.path.join(os.getcwd(), 'public'))

    # Build the source.
    elif args['build']:
        build_files = args['-s'] if args['-s'] else None
        command.build(build_files)
        logger.info('Build done.')

    # Post a new md.
    elif args['new'] and args['-t']:
        command.new(args['-t'], args['-c'], args['-f'])
        logger.info('New topic.')

    logger.info('Done.')


if __name__ == '__main__':
    main()
