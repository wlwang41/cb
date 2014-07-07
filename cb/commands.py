#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import codecs
from copy import deepcopy

from jinja2 import (
    Environment, FileSystemLoader, TemplateError
)

from cb import tools
from cb.server import preview

logger = logging.getLogger(__name__)


class Command(object):
    def __init__(self, config_path):
        self.site_config = self._get_config(config_path)
        # self.site_config = self._get_config(os.path.join(os.getcwd(), '_config.yml'))

        _template_path = os.path.join(
            os.getcwd(),
            self.site_config["themes_dir"],
            self.site_config["theme"]
        )
        try:
            self.env = Environment(
                loader=FileSystemLoader(_template_path)
            )
        except TemplateError, e:
            logging.error(str(e))
            sys.exit(1)

    def _set_default_configs(self):
        configs = {
            "url": "",
            "title": "",
            "keywords": "",
            "description": "",
            "author": "",
            "root": "/",
            "source": "content",
            "destination": "output",
            "themes_dir": "themes",
            "theme": "yasimple",
            "default_ext": "md",
            "pygments": True,
            "debug": False,
            "index": False
        }
        return configs

    def _format_config(self, configs):
        for k, v in configs.iteritems():
            if v is None:
                configs[k] = ""

        if configs["url"].endswith("/"):
            configs["url"] = configs["url"][:-1]

        return configs

    def _get_config(self, config_file):
        default_configs = self._set_default_configs()

        if not tools.check_path_exists(config_file):
            logging.error("{} not exists".format(config_file))
            sys.exit(1)

        configs = tools.get_ymal_data(tools.read_file(config_file))

        default_configs.update(configs)
        configs = self._format_config(deepcopy(default_configs))

        return configs

    def _get_config_and_content(self, path):
        config, content = self._split_source_page(path)

        config = tools.get_ymal_data("".join(config))

        return config, "".join(content)

    def _split_source_page(self, path):
        """Split the source file texts by triple-dashed lines.

        shit code
        """
        with codecs.open(path, "rb", "utf-8") as fd:
            textlist = fd.readlines()

        metadata_notation = "---\n"
        if textlist[0] != metadata_notation:
            logging.error(
                "{} first line must be triple-dashed!".format(path)
            )
            sys.exit(1)

        metadata_textlist = []
        metadata_end_flag = False
        idx = 1
        max_idx = len(textlist)
        # TODO(crow): BE PYTHONIC!!!
        while not metadata_end_flag:
            metadata_textlist.append(textlist[idx])
            idx += 1
            if idx >= max_idx:
                logging.error(
                    "{} doesn't have end triple-dashed!".format(path)
                )
                sys.exit(1)
            if textlist[idx] == metadata_notation:
                metadata_end_flag = True
        content = textlist[idx + 1:]

        return metadata_textlist, content

    def _get_page_data(self, file_paths):
        # TODO(crow): get metadata in page.md
        rv = {}
        for i in file_paths:
            rv[i] = {}
            page_config, md = self._get_config_and_content(i)

            parsed_md = tools.parse_markdown(md, self.site_config)

            rv[i]['title'] = page_config.get('title', '')
            rv[i]['date'] = page_config.get('date', '')
            rv[i]['content'] = parsed_md
            # TODO(crow): only support first category
            rv[i]['category'] = i.split('/')[-2]

        return rv

    def _render_html(self, template_file, data):
        data['site'] = self.site_config
        data['page'] = data
        try:
            template = self.env.get_template(template_file)
            html = template.render(data)
        except TemplateError, e:
            logging.error("Unable to load template {}: {}"
                          .format(template_file, str(e)))
            sys.exit(1)

        return html

    def _generate_page(self, filename, page_data):
        page_html = self._render_html('page.html', page_data)

        html_path = os.path.join(os.getcwd(), 'public', 'content', page_data['category'])

        if not tools.check_path_exists(html_path):
            tools.mkdir_p(html_path)

        with codecs.open(os.path.join(html_path, filename.split('.')[0] + '.html'), 'wb', 'utf-8') as f:
            f.write(page_html)

    def _get_index_data(self):
        pass

    def _generate_index(self):
        pass

    def build(self, filenames):
        # generate pages
        # generate index
        # move css
        if filenames:
            # get all target md files
            file_paths = []
            for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'source')):
                for i in files:
                    if i in filenames and tools.check_extension(i):
                        file_paths.append(os.path.join(root, i))

            page_datas = self._get_page_data(file_paths)

            for k, v in page_datas.iteritems():
                self._generate_page(k.split('/')[-1], v)

        else:
            # build all
            # delete all files in public
            # convert to html
            # move to public
            pass

    def new(self):
        pass

    def deploy(self):
        pass


def init(path):
    config_path = os.path.join(os.path.dirname(__file__), 'init_source', '_config.yml')
    hello_md_path = os.path.join(os.path.dirname(__file__), 'init_source', 'hello.md')
    themes_path = os.path.join(os.path.dirname(__file__), 'themes')

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
