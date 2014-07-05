#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging

from cb import tools
from cb.server import preview

logger = logging.getLogger(__name__)
config_path = os.path.join(os.path.dirname(__file__), 'init_source', '_config.yml')
hello_md_path = os.path.join(os.path.dirname(__file__), 'init_source', 'hello.md')
themes_path = os.path.join(os.path.dirname(__file__), 'themes')


def _get_config(path):
    pass

# read the config yml
# conf = get_config(os.path.join(os.getcwd(), '_config.yml'))


def init(path):
    # 1. create source folder
    tools.mkdir_p(os.path.join(path, 'source'))
    tools.mkdir_p(os.path.join(path, 'source', 'notes'))
    tools.copy_file(hello_md_path, os.path.join(path, 'source', 'notes', 'hello.md'))

    # 2. create public folder
    tools.mkdir_p(os.path.join(path, 'public'))

    # 3. cp _config.yml
    tools.copy_file(config_path, os.path.join(path, '_config.yml'))

    # 4. cp themes
    dst_themes_path = os.path.join(path, 'themes')
    tools.mkdir_p(dst_themes_path)
    tools.copytree(themes_path, dst_themes_path)


def server(path):
    # TODO(crow): not need
    if not tools.check_path_exists(path):
        logger.error('Running on the wrong path.')
        sys.exit(1)

    preview(path)


def build():
    pass


def new():
    pass


def deploy():
    pass
