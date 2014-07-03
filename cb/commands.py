#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from cb import tools

logger = logging.getLogger(__name__)
config_path = os.path.join(os.path.dirname(__file__), 'init_source', '_config.yml')
themes_path = os.path.join(os.path.dirname(__file__), 'themes')


def _get_config(path):
    pass


def init(path):
    # 1. create source folder
    tools.mkdir_p(os.path.join(path, 'source'))
    # put hello.md into it

    # 2. create public folder
    tools.mkdir_p(os.path.join(path, 'public'))

    # 3. cp _config.yml
    tools.copy_file(config_path, os.path.join(path, '_config.yml'))

    # 4. cp themes
    dst_themes_path = os.path.join(path, 'themes')
    tools.mkdir_p(dst_themes_path)
    tools.copytree(themes_path, dst_themes_path)


def server():
    pass


def build():
    pass


def new():
    pass


def deploy():
    pass
