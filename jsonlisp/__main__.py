import atexit
import os
import readline
import sys

def setup_rl():
    histfile = os.path.join(os.path.expanduser("~"), ".jsonlisp_history")

    try:
        readline.read_history_file(histfile)
        h_len = readline.get_current_history_length()
    except FileNotFoundError:
        open(histfile, 'wb').close()
        h_len = 0

    def save(prev_h_len, histfile):
        new_h_len = readline.get_current_history_length()
        readline.set_history_length(1000)
        readline.append_history_file(new_h_len - prev_h_len, histfile)
    atexit.register(save, h_len, histfile)


from . import repl
from . import run_file

if sys.argv[1:]:
    run_file(sys.argv[1])
else:
    setup_rl()
    repl()
