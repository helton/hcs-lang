from collections import namedtuple

Function = namedtuple('Function', 'scope formal_params statements anonymous_function')
FunctionMetadata = namedtuple('FunctionMetadata', 'scope formal_params statements')

class Scope(object):

    def __init__(self, functions = None, variables = None):
        self.functions = {} if functions is None else functions
        self.variables = {} if variables is None else variables 
        self.builtin_functions = {}        
        self.builtin_functions['avg']   = lambda *args: sum(args) / len(list(args))        
        self.builtin_functions['count'] = lambda *args: len(list(args))
        self.builtin_functions['max']   = lambda *args: max(args)
        self.builtin_functions['min']   = lambda *args: min(args)
        self.builtin_functions['print'] = lambda x: print(x)
        self.builtin_functions['sqr']   = lambda x: x ** x
        self.builtin_functions['sqrt']  = lambda x: sqrt(x)
        self.builtin_functions['sum']   = lambda *args: sum(args)

    def can_add_in_scope(self, name):
        if name in self.builtin_functions:
            raise NameError('Identifier "%s" is a builtin function, it cannot be overriden.' % (name))
        return True        

    def add_function(self, name, formal_params, stmts, anonymous_function):
        if self.can_add_in_scope(name):
            self.functions[name] = Function(None, formal_params, stmts, anonymous_function)

    def call(self, name, args):
        if name in self.builtin_functions:
            return self.builtin_functions[name](*args)
        else:
            if not name in self.functions:
                raise NameError("Function '%s' is not defined." % (name))
            else:
                function = self.functions[name]
                return self.direct_function_call(function.formal_params, function.statements, function.anonymous_function, args)

    def add_or_update_variable(self, name, value):
        if self.can_add_in_scope(name):
            self.variables[name] = value

    def add_variable_list(self, variable_list):
        for name, value in variable_list.items():
            self.add_or_update_variable(name, value)

    def get_variable_value(self, name):
        if not name in self.variables:
            raise NameError("Variable '%s' is not defined." % (name))
        else:
            return self.variables[name]

    def direct_function_call(self, formal_params, stmts, anonymous_function, args):
        metadata = FunctionMetadata(Scope(self.variables, self.functions), formal_params, stmts)        
        return anonymous_function(metadata, *args)        
