import resource

ALLOWED_STDLIB_MODULE_IMPORTS = ('math', 'random', 'time', 'datetime',
                          'functools', 'itertools', 'operator', 'string',
                          'collections', 're', 'json',
'heapq', 'bisect', 'copy', 'hashlib')

ALLOWED_CUSTOM_MODULE_IMPORTS = ('graph',)

MAX_CPU_TIME = 3 # 3 seconds
MAX_MEMORY = 100000000 # 100 mega bytes


for m in ALLOWED_STDLIB_MODULE_IMPORTS+ALLOWED_CUSTOM_MODULE_IMPORTS:
	__import__(m)

# see https://docs.python.org/3/library/resource.html
def set_resource_limits():
	resource.setrlimit(resource.RLIMIT_NOFILE, (0,0))
	resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
	resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_TIME, MAX_CPU_TIME))

unsafe_builtins = ['reload', 'open', 'compile',
                   'file', 'eval', 'exec', 'execfile',
                   'exit', 'quit', 'help', 'dir', 
                   'globals', 'locals', 'vars']

def banned_builtin_wrapper(banned_function_name):
	def wrapper(*args):
		raise Exception("YOU ARE VIOLATING MY RULES!!!! "+banned_function_name+ " is a banned builtin function")
	return wrapper

# see this blog post http://mathamy.com/whats-the-deal-with-builtins-vs-builtin.html
def safe_globals(builtin_main):
	safe_builtins = {}

	for key in dir(builtin_main):
		val = getattr(builtin_main, key)
		if key in unsafe_builtins:
			safe_builtins[key] = banned_builtin_wrapper(key)
		else:
			safe_builtins[key] = val

	safe_globals = {
		'__name__': '__main__',
		'__builtins__': safe_builtins
	}

	return safe_globals