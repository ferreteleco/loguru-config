"""Module internal utilities"""

import importlib
from json import loads

from loguru_config.modules.errors import InvalidSinkCallable


def _parse_activations(loggers):

    enable_logs = loggers["enable"].split(",")
    disable_logs = loggers["disable"].split(",")

    map(str.strip, enable_logs)
    map(str.strip, disable_logs)

    activation_list = []

    # First, disable loggers
    if "all" in disable_logs:
        activation_list.append(("", False))
        while "all" in disable_logs:
            disable_logs.remove("all")
    for item in disable_logs:
        activation_list.append((item, False))

    # Then, enable loggers
    if "all" in enable_logs:
        activation_list.append(("", True))
        while "all" in enable_logs:
            enable_logs.remove("all")
    for item in enable_logs:
        activation_list.append((item, True))

    return activation_list


def _get_sink_config(sink_conf):

    dest = sink_conf["dest"]
    if dest.startswith("$"):
        sink = _get_func_from_str(dest)
    else:
        sink = dest

    filt = sink_conf["filter"]

    filt_handler = _parse_filter(filt)

    handler = dict(
        sink=sink,
        level=sink_conf["level"],
        format=sink_conf["format"],
        enqueue=sink_conf.getboolean("enqueue"),
        serialize=sink_conf.getboolean("serialize"),
        colorize=sink_conf.getboolean("colorize"),
        filter=filt_handler,
    )

    return handler


def _get_func_from_str(string):
    if string.startswith("$"):
        chunks = string[1:].split(".")
        if len(chunks) == 1:
            module_str = "builtins"
        else:
            module_str = ".".join(chunks[:-1])

        module = importlib.import_module(module_str)
        try:
            callable_obj = getattr(module, chunks[-1])
        except AttributeError:
            raise InvalidSinkCallable(string)
    else:
        raise ValueError("Path string ill-formed (begin with '$')")

    return callable_obj


def _parse_filter(filt):
    if filt:
        if filt.startswith("$"):
            filt_handler = _get_func_from_str(filt)
        elif filt.startswith("{"):
            filt_handler = loads(filt)
        else:
            filt_handler = filt
    else:
        filt_handler = None
    return filt_handler
