########
JsonLisp
########

JsonLisp is a primitive Lisp-like language using JSON as its syntax. Be a real
JSON programmer!

Repl
****

After installing JsonLisp, try it out in a built-in repl environment:
::

    $ python -m jsonlisp
    {λ}> ["defproc", "fact", ["n"], ["if", ["<=", "n", 1], 1, ["*", "n", ["fact", ["-", "n", 1]]]]]
    ["lambda", ["n"], ["if", ["<=", "n", 1], 1, ["*", "n", ["fact", ["-", "n", 1]]]]]
    {λ}> ["map", "fact", ["range", 0, 10]]
    [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
