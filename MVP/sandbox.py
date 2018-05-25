import resource

standard_module_import_whitelist = ('math', 'random', 'time', 'datetime',
                                    'functools', 'itertools', 'operator', 
                                    'string', 'collections', 're', 'json',
                                    'heapq', 'bisect', 'copy', 'hashlib')

custom_module_import_whitelist = ('graph',)

for m in standard_module_import_whitelist+custom_module_import_whitelist:
    __import__(m)

builtin_blacklist = ['reload', 'open', 'compile',
                   'file', 'eval', 'exec', 'execfile',
                   'exit', 'quit', 'help', 'dir', 
                   'globals', 'locals', 'vars']

def restricted_import(*args):
    # print("restricted_import with:", args, "hi")
    # print("restricted import with args of type", type(args), args[0])
    module_name = args[0]
    if module_name in standard_module_import_whitelist + custom_module_import_whitelist:
        imported_module = __import__(*args)
        return imported_module
    else:
        raise Exception("{0} is a banned import".format(module_name))

builtin_greylist = {
    '__import__': restricted_import
}

MAX_CPU_TIME = 3 # 3 seconds
MAX_MEMORY = 100000000 # 100 mega bytes



# see https://docs.python.org/3/library/resource.html
def set_resource_limits():
    resource.setrlimit(resource.RLIMIT_NOFILE, (10,10))
    resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
    resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_TIME, MAX_CPU_TIME))
    # pass


def banned_builtin_wrapper(banned_function_name):
    def wrapper(*args):
        raise Exception(banned_function_name+ " is a banned builtin function")
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
        '__builtins__': safe_builtins
    }

    return safe_globals

if __name__== '__main__':
    safe_globals(__builtins__)