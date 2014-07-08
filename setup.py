#!/usr/bin/env python

from setuptools import setup, find_packages
import cb


entry_points = {
    "console_scripts": [
        "cb = cb.cli:main",
    ]
}

requires = [
    "Markdown",
    "Pygments",
    "Jinja2",
    "PyYAML",
    "docopt",
]

setup(
    name="cb",
    version=cb.__version__,
    url="https://github.com/wlwang41/cb",
    keywords=("blog", "static page"),
    author="crow",
    author_email="wlwang41@gmail.com",
    description="Cb is a blog building tool inspired by tankywoo/simiki.",
    license="MIT License",
    packages=find_packages(),
    # include_package_data=True,
    install_requires=requires,
    entry_points=entry_points,
)
