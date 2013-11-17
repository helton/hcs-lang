from collections import namedtuple

Function = namedtuple('Function', 'scope formal_params statements lambda_function')
FunctionMetadata = namedtuple('FunctionMetadata', 'scope formal_params statements')

class Scope(object):

    def __init__(self, functions = None, variables = None):
        self.functions = {} if functions is None else functions
        self.variables = {} if variables is None else variables 

    def add_builtin_functions(self):
        pass
        """
        add_function('sum',   [], lambda *args: sum(args))
        add_function('max',   [], lambda *args: max(args))
        add_function('min',   [], lambda *args: min(args))
        add_function('print', [], lambda x: print(x))
        add_function('sqr',   [], lambda x: x ** x)
        add_function('sqrt',  [], lambda x: sqrt(x))
        """

    def add_function(self, name, formal_params, stmts, lambda_function):
        self.functions[name] = Function(None, formal_params, stmts, lambda_function)

    def call(self, name, args):
        if not name in self.functions:
            raise LookupError('Function "%s" is not defined in the scope.' % (name))
        else:
            function = self.functions[name]
            metadata = FunctionMetadata(Scope(self.variables, self.functions), function.formal_params, function.statements)
            return function.lambda_function(metadata, *args)

    def add_variable(self, name, value):
        self.variables[name] = value

    def add_variable_list(self, variable_list):
        for name, value in variable_list.items():
            self.add_variable(name, value)

    def get_variable_value(self, name):
        if not name in self.variables:
            raise LookupError('Variable "%s" is not defined in the scope.' % (name))
        else:
            return self.variables[name]
