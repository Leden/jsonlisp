import pytest

import jsonlisp


@pytest.fixture
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
