#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    print_function, unicode_literals, absolute_import
)

import os
import sys
import shutil
import errno
import logging
from os import path as osp

import yaml
import markdown

logger = logging.getLogger(__name__)

COLOR_CODES = {
    "reset": "\033[0m",
    "black": "\033[1;30m",
    "red": "\033[1;31m",
    "green": "\033[1;32m",
    "yellow": "\033[1;33m",
    "blue": "\033[1;34m",
    "magenta": "\033[1;35m",
    "cyan": "\033[1;36m",
    "white": "\033[1;37m",
    "bgred": "\033[1;41m",
    "bggrey": "\033[1;100m",
}


def color_msg(color, msg):
    return COLOR_CODES[color] + msg + COLOR_CODES["reset"]


def check_path_exists(path):
    """Check if the path(include file and directory) exists"""
    if osp.exists(path):
        return True
    return False


def check_extension(filename):
    """Check if the file extension is in the allowed extensions

    The `fnmatch` module can also get the suffix:
        patterns = ["*.md", "*.mkd", "*.markdown"]
        fnmatch.filter(files, pattern)
    """

    allowed_extensions = {".md", ".mkd", ".mdown", ".markdown"}
    return osp.splitext(filename)[1] in allowed_extensions


def copytree(src, dst, symlinks=False, ignore=None):
    """Copy from source directory to destination"""

    # TODO(crow): OSError: [Errno 17] File exists
    if not osp.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = osp.join(src, item)
        d = osp.join(dst, item)
        if osp.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def emptytree(directory):
    """Delete all the files and dirs under specified directory"""

    for p in os.listdir(directory):
        fp = osp.join(directory, p)
        if osp.isdir(fp):
            try:
                shutil.rmtree(fp)
                logger.info("Delete directory %s" % fp)
            except Exception, e:
                logger.error("Unable to delete directory %s: %s" % (fp, str(e)))
        elif osp.isfile(fp):
            try:
                logging.info("Delete file %s" % fp)
                os.remove(fp)
            except Exception, e:
                logger.error("Unable to delete file %s: %s" % (fp, str(e)))
        else:
            logger.error("Unable to delete %s, unknown filetype" % fp)


def mkdir_p(path):
    """Make parent directories as needed, like `mkdir -p`"""
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def listdir_nohidden(path):
    """List not hidden files or directories under path"""
    for f in os.listdir(path):
        if isinstance(f, str):
            f = unicode(f, "utf-8")
        if not f.startswith('.'):
            yield f


def copy_file(src, dst):
    try:
        shutil.copyfile(src, dst)
    except (shutil.Error, IOError) as e:
        logger.error(str(e))


def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def check_config(data):
    """Check if metadata is right

    TODO(crow): check more
    """

    is_right = True

    if "title" not in data:
        logging.error("No 'title' in _config.yml")
        is_right = False

    return is_right


def get_ymal_data(data):
    """Get metadata and validate them

    :param data: metadata in yaml format
    """
    try:
        format_data = yaml.load(data)
    except yaml.YAMLError, e:
        msg = "Yaml format error: {}".format(
            unicode(str(e), "utf-8")
        )
        logging.error(msg)
        sys.exit(1)

    if not check_config(format_data):
        sys.exit(1)

    return format_data


def set_markdown_extensions(site_settings):
    """Set the extensions for markdown parser"""
    # Base markdown extensions support "fenced_code".
    markdown_extensions = ["fenced_code"]
    if site_settings["pygments"]:
        markdown_extensions.extend([
            "extra",
            "codehilite(css_class=hlcode)",
            "toc(title=Table of Contents)"
        ])

    return markdown_extensions


def parse_markdown(markdown_content, site_settings):
    """Parse markdown text to html.

    :param markdown_content: Markdown text lists #TODO#
    """
    markdown_extensions = set_markdown_extensions(site_settings)

    html_content = markdown.markdown(
        markdown_content,
        extensions=markdown_extensions,
    )

    return html_content
