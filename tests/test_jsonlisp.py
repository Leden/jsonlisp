import jsonlisp
import pytest
from jsonlisp import __version__


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture()
def env():
    return jsonlisp.default_env()


def test__defmacro(env):
    assert (
        jsonlisp.interp(
            ["begin", ["defmacro", "add-two", ["x"], ["+", 2, "x"]], ["add-two", 2]],
            env,
        )
        == 4
    )


def test__defproc(env):
    assert (
        jsonlisp.interp(
            ["begin", ["defproc", "add-two", ["x"], ["+", 2, "x"]], ["add-two", 2]], env
        )
        == 4
    )
