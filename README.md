# Cb

[![Latest Version](http://img.shields.io/badge/pypi-v1.0-blue.svg?style=flat)](https://pypi.python.org/pypi/cb)
[![The MIT License](http://img.shields.io/badge/license-MIT-red.svg?style=flat)](https://github.com/wlwang41/cb/blob/master/LICENSE)

Cb is my blog building tool inspired by [simiki](https://github.com/tankywoo/simiki), written in [python](https://www.python.org/).

* Easy to use, it only takes few a steps to generate your blog.
* [Markdown](http://daringfireball.net/projects/markdown/) support.
* You can write your own themes.

-----

## Quick Start

### Install

    pip install cb

### Update

    pip install --upgrade cb

### Init your blog

    mkdir YOUR_BLOG_PATH && cb YOUR_BLOG_PATH
    cb init

After initialization, you should add your own info in *_config.yml* file.

### New topic

    cb new -t 'first blog' -c 'note'

### Build to html

    cb build

### preview

    cb server

> For more detail, type `cb -h`.
