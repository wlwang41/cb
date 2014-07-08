#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime
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

        self.template_path = os.path.join(
            os.getcwd(),
            self.site_config["themes_dir"],
            self.site_config["theme"]
        )
        try:
            self.env = Environment(
                loader=FileSystemLoader(self.template_path)
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
            "theme": "",
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
        _data = {}
        _data['site'] = self.site_config

        if template_file == 'page.html':
            _data['page'] = data
        elif template_file == 'index.html':
            _data['structure'] = data
        else:
            # TODO(crow): else template logic
            logger.error('Unsupported template.')

        try:
            template = self.env.get_template(template_file)
            html = template.render(_data)
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

    def _get_index_data(self, file_paths):
        # category and page
        rv = {}
        for i in file_paths:
            # TODO(crow): only support first category
            _ = i.split('/')
            category = _[-2]
            name = _[-1].split('.')[0]
            page_config, md = self._get_config_and_content(i)
            rv.setdefault(category, {})
            rv[category].update(
                {
                    i: {
                        'title': page_config.get('title', ''),
                        'name': name.decode('utf-8'),
                        'date': page_config.get('date', '')
                    }
                }
            )

        return rv

    def _generate_index(self, index_data):
        index_html = self._render_html('index.html', index_data)

        html_path = os.path.join(os.getcwd(), 'public', 'index.html')

        with codecs.open(html_path, 'wb', 'utf-8') as f:
        # with open(html_path, 'wb') as f:
            f.write(index_html)

    def _cp_static(self):
        src_static_path = os.path.join(self.template_path, 'static')

        dst_static_path = os.path.join(os.getcwd(), 'public', 'static')

        if tools.check_path_exists(dst_static_path):
            tools.emptytree(dst_static_path)
        else:
            tools.mkdir_p(dst_static_path)

        tools.copytree(src_static_path, dst_static_path)

    def build(self, filenames):
        # generate pages
        # get all target md files
        file_paths = []
        all_file_paths = []
        for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'source')):
            for i in files:
                if not tools.check_extension(i):
                    continue

                all_file_paths.append(os.path.join(root, i))

                if filenames:
                    if i in filenames:
                        file_paths.append(os.path.join(root, i))
                else:
                    file_paths.append(os.path.join(root, i))

        page_datas = self._get_page_data(file_paths)

        for k, v in page_datas.iteritems():
            self._generate_page(k.split('/')[-1], v)

        # cp static including to the theme
        self._cp_static()
        # generate index

        index_data = self._get_index_data(all_file_paths)
        self._generate_index(index_data)

    def _format_new_input(self, title, category, output_file):
        if not output_file:
            _ = title.replace(os.sep, " slash ")
            output_file = "{}.md".format("-".join(_.split()).lower())
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        title = title
        category = category

        return title, category, output_file, date

    def new(self, title, category, output_file):
        title, category, output_file, date = self._format_new_input(title, category, output_file)
        try:
            meta = "\n".join([
                "---",
                "title: \"{}\"".format(title),
                "date: {}".format(date),
                "---",
            ]) + "\n\n"
        except Exception, e:
            logger.error(str(e))
            sys.exit(1)

        category_path = os.path.join(os.getcwd(), 'source', category)
        if not tools.check_path_exists(category_path):
            tools.mkdir_p(category_path)
            logger.info("Creating category {}.".format(category))

        output_path = os.path.join(category_path, output_file)
        if tools.check_path_exists(output_path):
            logger.warning("file exists: {}".format(output_path))
        else:
            logger.info("Creating new post: {}".format(output_path))
            with open(output_path, "wb") as f:
            # with codecs.open(output_path, "wb", "utf-8") as f:
                f.write(meta)

    def deploy(self):
        logger.warn('You can deploy public to vps or github page.')


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
