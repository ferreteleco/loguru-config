"""Module public utilities"""

import sys
import configparser

from loguru import logger as LOG

from loguru_config.modules.internal import (
    _parse_activations,
    _get_sink_config,
)


def init_log(path):
    """Opens a .ini file from where to parse loguru config options.

    Arguments:
        path {String} -- Path to .ini file
    """

    config = configparser.ConfigParser()
    config.read(path)

    activations = _parse_activations(config["loggers"])

    sinks = config["sinks"]["keys"].split(",")
    map(str.strip, sinks)

    handlers = []
    for sink in sinks:
        if sink == "default":
            LOG.add(sys.stderr)
        else:
            sink_conf = config[sink]
            sink_conf = _get_sink_config(sink_conf)
            handlers.append(sink_conf)

    LOG.configure(handlers=handlers, activation=activations)
