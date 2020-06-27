from collections import ChainMap
from pprint import pprint
import functools
import ipdb
import json
import logging
import operator

logger = logging.getLogger(__name__)

Symbol = str
List = list
Number = (int, float)
Dict = dict


class Env(ChainMap):
    def __json__(self):
        return self.maps


class Proc:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args):
        env = Env(dict(zip(self.params, args)), self.env)
        return interp(self.body, env)

    def __json__(self):
        return ["lambda", self.params, self.body]


class Macro:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def expand(self, *args, env):
        static_env = Env(dict(zip(self.params, args)), self.env)
        exp = interp(self.body, static_env)
        return interp(exp, env)

    def __json__(self):
        return ["macro", self.params, self.body]


std_env = {
    "!": operator.not_,  # not x
    "&": operator.and_,  # x and y
    "*": operator.mul,  # x * y
    "+": operator.add,  # x + y
    "-": operator.sub,  # x - y
    "/": operator.truediv,  # x / y
    "<": operator.lt,  # x < y
    "<=": operator.le,  # x <= y
    "=": operator.eq,  # x == y
    ">": operator.gt,  # x > y
    ">=": operator.ge,  # x >= y
    "^": operator.xor,  # x ^ y
    "apply": lambda proc, args: proc(*args),  # x(*y)
    "begin": lambda *x: x[-1],
    "cons": lambda x, y: [x, *y],  # [x, *y]
    "dict": lambda x: dict(x),
    "dict-del": lambda d, k: {_k: d[_k] for _k in d if k != _k},
    "dict-get": lambda d, k: d.get(k),
    "dict-items": lambda x: list(x.items()),
    "dict-set": lambda d, k, v: {**d, k: v},
    "dict?": lambda x: isinstance(x, Dict),
    "in": lambda x, y: x in y,
    "len": len,
    "list": lambda *x: list(x),  # list(x)
    "list?": lambda x: isinstance(x, List),
    "macro?": lambda x: isinstance(x, Macro),
    "map": lambda *args: list(map(*args)),  # list(map(x))
    "null?": lambda x: x is None,
    "number?": lambda x: isinstance(x, Number),
    "print": pprint,
    "proc?": callable,
    "symbol?": lambda x: isinstance(s, Symbol),
    "|": operator.or_,  # x or y
    "head": lambda x: x[0],
    "tail": lambda x: x[1:],
    "defmacro": [
        "macro",
        ["name", "params", "body"],
        [
            "list",
            ["quote", "def"],
            "name",
            ["list", ["quote", "macro"], "params", "body"],
        ],
    ],
    "defproc": [
        "macro",
        ["name", "params", "body"],
        [
            "list",
            ["quote", "def"],
            "name",
            ["list", ["quote", "lambda"], "params", "body"],
        ],
    ],
}


def parse(line):
    return json.loads(line)


def unparse(expr):
    return json.dumps(expr, default=to_json)


def to_json(obj):
    if hasattr(obj, "__json__"):
        return obj.__json__()
    return repr(obj)


def interp(x, env):
    if isinstance(x, Symbol):
        return env[x]

    if not isinstance(x, List):
        return x

    if x == []:
        return x

    if x[0] == "quote":
        _, exp = x
        return exp

    if x[0] == "if":
        _, test, conseq, alt = x
        exp = conseq if interp(test, env) else alt
        return interp(exp, env)

    if x[0] == "def":
        _, var, exp = x
        val = env[var] = interp(exp, env)
        return val

    if x[0] == "lambda":
        _, params, body = x
        return Proc(params, body, env)

    if x[0] == "macro":
        _, params, body = x
        return Macro(params, body, env)

    proc_or_macro_exp, *args = x
    proc = interp(proc_or_macro_exp, env)
    if isinstance(proc, Macro):
        return proc.expand(*args, env=env)
    else:
        args = [interp(exp, env) for exp in args]
        return proc(*args)


def repl(prompt=r"{λ}> "):
    env = Env()
    env.update(std_env)
    env["__env__"] = env

    while True:
        try:
            line = input(prompt)
            debug = line.startswith(":dbg")
            if debug:
                line = line.replace(":dbg", "").strip()
                ipdb.set_trace()
            print(unparse(interp(parse(line), env)))
        except EOFError:
            print("Bye")
            break
        except Exception as err:
            print(repr(err))
