import parsimonious
import operator
from Scope import Scope

class HCS(object):   

    def __init__(self, scope = None):
        self.scope = Scope() if scope is None else scope

    def parse(self, source):
        grammar = '\n'.join(v.__doc__ for k, v in vars(self.__class__).items()
                      if '__' not in k and hasattr(v, '__doc__') and v.__doc__)
        return parsimonious.Grammar(grammar)['program'].parse(source)

    def evaluate(self, source):
        node = self.parse(source.replace("\n", " ")) if isinstance(source, str) else source
        method = getattr(self, node.expr_name, lambda node, children: children)
        if node.expr_name in ['formal_parameters_and_body', 'ifelse']:
            return method(node)
        return method(node, [self.evaluate(n) for n in node])

#################################### RULES ####################################

    def add_op(self, node, children):
        'add_op = ~"[+-]"'
        add_operator = {"+": operator.add, "-": operator.sub}
        return add_operator[node.text]

    def anonymous_function(self, node, children):
        'anonymous_function = "def" _ formal_parameters_and_body'
        _, _, formal_params_and_body = children
        return formal_params_and_body

    def anonymous_function_assignment(self, node, children):
        'anonymous_function_assignment = identifier_name _ "=" _ anonymous_function'
        func_name, _, _, _, anonymous_func_result = children  
        params, stmts, anonymous_func = anonymous_func_result
        self.scope.add_function(func_name, params, stmts, anonymous_func)
        return anonymous_func   

    def anonymous_function_call(self, node, children):
        'anonymous_function_call = "(" _ anonymous_function _ ")" _ "(" _ arguments _ ")"'
        _, _, anonymous_func_result, _, _, _, _, _, args, _, _ = children
        params, stmts, anonymous_func = anonymous_func_result
        return self.scope.direct_function_call(params, stmts, anonymous_func, args)

    def arguments(self, node, children):
        'arguments = expression ( _ "," _ expression _ )*'
        expr, expr_list = children
        exprs = [expr]
        for _, _, _, expr, _ in expr_list:
            exprs.append(expr)
        return exprs

    def assignment(self, node, children):
        'assignment = anonymous_function_assignment / variable_assignment'
        return children[0]

    def expression(self, node, children):
        'expression = anonymous_function_call / function_call / assignment / prefix_expression / simple_expression'
        return children[0]

    def factor(self, node, children):
        'factor = number / postfix_expression / identifier_value / parenthesized_expression / string'
        return children[0]

    def formal_parameters_and_body(self, node):
        'formal_parameters_and_body = "(" _ parameters _ ")" _ "{" _ statements _ "}"'
        _, _, params, _, _, _, _, _, stmts, _, _ = node
        params = list(map(lambda x: x.strip(), ''.join([param.text.strip() for param in params]).split(',')))

        def anonymous_func(function_metadata, *args):   
            function_metadata.scope.add_variable_list(dict(zip(function_metadata.formal_params, args)))
            return HCS(function_metadata.scope).evaluate(function_metadata.statements)

        return (params, stmts, anonymous_func)        

    def function_call(self, node, children):
        'function_call = identifier_name _ "(" _ arguments _ ")"'
        name, _, _, _, args, _, _ = children
        return self.scope.call(name, args)

    def identifier_name(self, node, children):
        'identifier_name = ~"[a-z_][a-z_0-9]*"i _'
        return node.text.strip()

    def identifier_value(self, node, children):
        'identifier_value = ~"[a-z_][a-z_0-9]*"i _'
        name = node.text.strip()
        return self.scope.get_variable_value(name)  

    def statement_block(self, node, children):
        'statement_block = "{" _ statements _ "}"'
        _, _, stmt, _, _ = children
        return stmt

    def ifelse(self, node):
        'ifelse = "if" _ parenthesized_expression _  statement_block _ ( "else" _ statement_block )?'
        _, _, condition, _, if_true, _, if_false = node
        if self.evaluate(condition):
            return self.evaluate(if_true)
        elif len(if_false.children) > 0:
            return self.evaluate(if_false)

    def mul_op(self, node, children):
        'mul_op = "*" / "//" / "/" / "%"'
        mul_operator = {"*": operator.mul, "/": operator.truediv, "//": operator.floordiv, "%": operator.mod}        
        return mul_operator[node.text]

    def named_function(self, node, children):
        'named_function = "def" ws identifier_name _ formal_parameters_and_body'        
        _, _, func_name, _, func_result = children
        params, stmts, func = func_result
        self.scope.add_function(func_name, params, stmts, func)
        return func   

    def number(self, node, children):
        'number = ~"[+-]?\s*(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"'
        try:
            return int(node.text)
        except ValueError:
            return float(node.text)

    def optional_semicolon(self, node, children):
        'optional_semicolon = _ ";"? _'

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

    def postfix_expression(self, node, children):
        'postfix_expression = identifier_name pre_posfix_op'
        var_name, op = children
        current_value = self.scope.get_variable_value(var_name)
        self.scope.add_or_update_variable(var_name, op(current_value))
        return current_value

    def prefix_expression(self, node, children):
        'prefix_expression = pre_posfix_op identifier_name'
        op, var_name = children
        self.scope.add_or_update_variable(var_name, op(self.scope.get_variable_value(var_name)))
        return self.scope.get_variable_value(var_name)

    def pre_op(self, node, children):
        'pre_op = ~"[+-]"'
        pre_operator = {"+": lambda x: x, "-": operator.neg}
        return pre_operator[node.text]

    def pre_posfix_op(self, node, children):
        'pre_posfix_op = "++" / "--"'
        pre_posfix = {"++": lambda x: x + 1, "--": lambda x: x - 1,}        
        return pre_posfix[node.text]

    def program(self, node, children):
        'program = statements*'
        return children[0]

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

    def statement(self, node, children):
        'statement = ifelse / named_function / expression'
        return children[0]

    def statements(self, node, children):
        'statements = _ statement ( optional_semicolon statement )* optional_semicolon '
        _, stmt, stmt_list, _, = children
        result = stmt
        for _, stmt in stmt_list:
            result = stmt
        return stmt           

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
        self.scope.add_or_update_variable(var_name, expr)
        return expr

    def ws(self, node, children):
        'ws = ~"\s+"'

    def _(self, node, children):
        '_ = ~"\s*"'