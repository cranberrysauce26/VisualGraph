import resource
import pygraph
# import io
from trace_entry import add_trace_entry

standard_module_import_whitelist = ('math', 'random', 'time', 'datetime',
                                    'functools', 'itertools', 'operator', 
                                    'string', 'collections', 're', 'json',
                                    'heapq', 'bisect', 'copy', 'hashlib')

custom_module_import_whitelist = tuple()

for m in standard_module_import_whitelist+custom_module_import_whitelist:
    __import__(m)

builtin_blacklist = ['reload', 'open', 'compile',
                   'file', 'eval', 'exec', 'execfile',
                   'exit', 'quit', 'help', 'dir', 
                   'globals', 'locals', 'vars']

def restricted_import(*args):
    module_name = args[0]
    if module_name in standard_module_import_whitelist + custom_module_import_whitelist:
        imported_module = __import__(*args)
        return imported_module
    else:
        raise Exception('{0} is a banned import'.format(module_name))

def print_wrapper(*args, **kwargs):
    '''
    Behaves exactly like the print statement, except nothing is printed.
    Instead, the a trace entry is added with the string to print
    '''
    buff = ''
    sep = ' ' if 'sep' not in kwargs else kwargs['sep']
    end = '\n' if 'end' not in kwargs else kwargs['end']
    argc = len(args)
    for i, s in enumerate(args):
        buff += str(s)
        buff += sep if i != argc-1 else end
    add_trace_entry(command_name='user_stdout', return_value=buff)

builtin_greylist = {
    '__import__': restricted_import,
    'print': print_wrapper
}

def banned_builtin_wrapper(banned_function_name):
    def wrapper(*args):
        raise Exception('{0} is a banned builtin function'.format(banned_function_name))
    return wrapper

# see this blog post http://mathamy.com/whats-the-deal-with-builtins-vs-builtin.html
def safe_globals(builtin_main):
    safe_builtins = {}

    for key in dir(builtin_main):
        val = getattr(builtin_main, key)
        if key in builtin_blacklist:
            safe_builtins[key] = banned_builtin_wrapper(key)
        elif key in builtin_greylist:
            safe_builtins[key] = builtin_greylist[key]
        else:
            safe_builtins[key] = val

    safe_globals = {
        '__name__': '__main__',
        '__builtins__': safe_builtins,
        'Graph': pygraph.Graph
    }

    return safe_globals

if __name__== '__main__':
    safe_globals(__builtins__)