import parsimonious
import operator
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

class HCS(object):   

    def __init__(self, scope = None):
        if scope is None:
            self.scope = Scope()
            self.scope.add_builtin_functions()
        else:
            self.scope = scope

    def parse(self, source):
        grammar = '\n'.join(v.__doc__ for k, v in vars(self.__class__).items()
                      if '__' not in k and hasattr(v, '__doc__') and v.__doc__)
        return parsimonious.Grammar(grammar)['goal'].parse(source)

    def eval(self, source):
        node = self.parse(source.replace("\n", " ")) if isinstance(source, str) else source
        method = getattr(self, node.expr_name, lambda node, children: children)
        if node.expr_name in ['lambda_function']:
            return method(node)
        return method(node, [self.eval(n) for n in node])

#################################### RULES ####################################

    def add_op(self, node, children):
        'add_op = ~"[+-]"'
        add_operator = {"+": operator.add, "-": operator.sub}
        return add_operator[node.text]

    def arguments(self, node, children):
        'arguments = expression ( _ "," _ expression _ )*'
        expr, expr_list = children
        exprs = [expr]
        for _, _, _, expr, _ in expr_list:
            exprs.append(expr)
        return exprs

    def assignment(self, node, children):
        'assignment = lambda_function_assignment / variable_assignment'
        return children[0]

    def expression(self, node, children):
        'expression = function_call / assignment / simple_expression'
        return children[0]

    def factor(self, node, children):
        'factor = number / identifier_value / parenthesized_expression / string'
        return children[0]

    def function_call(self, node, children):
        'function_call = identifier_name _ "(" _ arguments _ ")"'
        name, _, _, _, args, _, _ = children
        return self.scope.call(name, args)

    def goal(self, node, children):
        'goal = statements*'
        return children[0]

    def identifier_name(self, node, children):
        'identifier_name = ~"[a-z_][a-z_0-9]*"i _'
        return node.text.strip()

    def identifier_value(self, node, children):
        'identifier_value = ~"[a-z_][a-z_0-9]*"i _'
        name = node.text.strip()
        return self.scope.get_variable_value(name)

    def lambda_function(self, node):
        'lambda_function = "def" _ "(" _ parameters _ ")" _ "{" _ statements _ "}"'
        _, _, _, _, params, _, _, _, _, _, stmts, _, _ = node
        params = list(map(lambda x: x.strip(), ''.join([param.text.strip() for param in params]).split(',')))

        def lambda_func(function_metadata, *args):   
            function_metadata.scope.add_variable_list(dict(zip(function_metadata.formal_params, args)))
            return HCS(function_metadata.scope).eval(function_metadata.statements)

        return (params, stmts, lambda_func)

    def lambda_function_assignment(self, node, children):
        'lambda_function_assignment = identifier_name _ "=" _ lambda_function'
        func_name, _, _, _, lambda_func_result = children
        params, stmts, lambda_func = lambda_func_result
        self.scope.add_function(func_name, params, stmts, lambda_func)
        return lambda_func      

    def mul_op(self, node, children):
        'mul_op = "*" / "//" / "/" / "%"'
        mul_operator = {"*": operator.mul, "/": operator.truediv, "//": operator.floordiv, "%": operator.mod}        
        return mul_operator[node.text]

    def number(self, node, children):
        'number = ~"[+-]?\s*(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"'
        try:
            return int(node.text)
        except ValueError:
            return float(node.text)

    def parameters(self, node, children):
        'parameters = identifier_name ( _ "," _ identifier_name)*'
        first_id, id_list = children
        ids = [first_id]
        for _, _, _, cur_id in id_list:
            ids.append(cur_id)
        return ids

    def parenthesized_expression(self, node, children):
        'parenthesized_expression = "(" _ expression _ ")"'
        return children[2]  

    def pre_op(self, node, children):
        'pre_op = ~"[+-]"'
        pre_operator = {"+": lambda x: x, "-": operator.neg}
        return pre_operator[node.text]

    def simple_expression(self, node, children):
        'simple_expression = pre_op? _ term ( _ add_op _ term )*'
        p_op, _, term, term_list = children
        if len(p_op) > 0:
            result = p_op[0](term)
        else:
            result = term
        for _, a_op, _, term in term_list:
            result = a_op(result, term)
        return result    

    def statements(self, node, children):
        'statements = expression ( _ ";" _ expression )* _'
        expr, expr_list, _ = children
        result = expr
        for _, _, _, expr in expr_list:
            result = expr
        return expr           

    def string(self, node, children):
        'string = ~"\\".*?\\""'
        return node.text

    def term(self, node, children):
        'term = factor ( _ mul_op _ factor )*'        
        factor, factor_list = children
        result = factor
        for _, m_op, _, factor in factor_list:
            result = m_op(result, factor)
        return result          

    def variable_assignment(self, node, children):
        'variable_assignment = identifier_name _ "=" _ expression'
        var_name, _, _, _, expr = children
        self.scope.add_variable(var_name, expr)
        return expr

    def _(self, node, children):
        '_ = ~"\s*"'