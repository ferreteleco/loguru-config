
from pytest import raises
from loguru_config.modules.internal import _get_func_from_str
from loguru_config.modules.errors import InvalidSinkCallable


def test_raise_invalid_sink():

    with raises(InvalidSinkCallable):
        _get_func_from_str("$dodle")


def test_valid_sink_builtin():
    true_print = _get_func_from_str("$print")

    assert callable(true_print)


def test_valid_sink_non_builtin_module(capsys):

    import io

    true_stderr = _get_func_from_str("$sys.stderr")

    # Temporarily disables pytest stdout capture
    with capsys.disabled():
        assert isinstance(true_stderr, io.TextIOWrapper)


def test_valid_sink_custom_module():

    func = _get_func_from_str("$loguru_config.modules.internal._get_func_from_str")
    assert callable(func)