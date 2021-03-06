#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from logging import (
    getLogger, Formatter, StreamHandler
)

from cb import tools


class ANSIFormatter(Formatter):
    """Use ANSI escape sequences to colored log"""

    def format(self, record):
        lvl2color = {
            "DEBUG": "blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bgred"
        }

        msg = record.getMessage()
        rln = record.levelname
        if rln in lvl2color:
            if isinstance(msg, unicode):
                return "[{}]: {}".format(tools.color_msg(lvl2color[rln], rln), msg.encode('utf-8'))
            else:
                return "[{}]: {}".format(tools.color_msg(lvl2color[rln], rln), msg)
        else:
            return msg


def logging_init(level=None, logger=getLogger(), handler=StreamHandler(), use_color=True):
    if use_color:
        fmt = ANSIFormatter()
    else:
        fmt = Formatter()
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    if level:
        logger.setLevel(level)
