import parsimonious
import operator

class HCS(object):

    def __init__(self):
        self.environment = {}

    def parse(self, source):
        grammar = '\n'.join(v.__doc__ for k, v in vars(self.__class__).items()
                      if '__' not in k and hasattr(v, '__doc__') and v.__doc__)
        return parsimonious.Grammar(grammar)['goal'].parse(source)

    def eval(self, source):
        node = self.parse(source) if isinstance(source, str) else source
        method = getattr(self, node.expr_name, lambda node, children: children)
        return method(node, [self.eval(n) for n in node])

    def goal(self, node, children):
        'goal = statements*'
        return children[0]

    def statements(self, node, children):
        'statements = statement ( _ ";" _ statement )*'
        stmt, stmt_list = children
        result = stmt
        for _, _, _, stmt in stmt_list:
            result = stmt
        return stmt

    def statement(self, node, children):
        'statement = _ ( function_def / assignment / expression )'
        return children[1][0]

    def assignment(self, node, children):
        'assignment = identifier_name _ "=" _ expression'
        id_name, _, _, _, expr = children
        self.environment[id_name] = expr
        return expr

    def function_def(self, node, children):
        'function_def = "def" ws identifier_name "(" _ arguments _ ")" _ "{" _ statements? _ "}"'
        _, _, func_name, _, _, args, _, _, _, _, _, stmts, _, _ = children
        return None

    def arguments(self, node, children):
        'arguments = identifier_list'
        return children[0]

    def identifier_list(self, node, children):
        'identifier_list = identifier_name (_ "," _ identifier_name)*'
        id_1, id_list = children
        ids = [id_1]
        for _, _, _, cur_id in id_list:
            ids.append(cur_id)
        return ids

    def expression(self, node, children):
        'expression = pre_op? _ term ( _ add_op _ term )*'
        p_op, _, term, term_list = children
        if len(p_op) > 0:
            result = p_op[0](term)
        else:
            result = term
        for _, a_op, _, term in term_list:
            result = a_op(result, term)
        return result

    def pre_op(self, node, children):
        'pre_op = ~"[+-]"'
        pre_operator = {"+": lambda x: x, "-": operator.neg}
        return pre_operator[node.text]       

    def term(self, node, children):
        'term = factor ( _ mul_op _ factor )*'        
        factor, factor_list = children
        result = factor
        for _, m_op, _, factor in factor_list:
            result = m_op(result, factor)
        return result        

    def factor(self, node, children):
        'factor = number / identifier_value / parentesized_expression'
        return children[0]

    def parentesized_expression(self, node, children):
        'parentesized_expression = "(" _ expression _ ")"'
        return children[2]

    def add_op(self, node, children):
        'add_op = ~"[+-]"'
        add_operator = {"+": operator.add, "-": operator.sub}
        return add_operator[node.text]
        
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

    def identifier_value(self, node, children):
        'identifier_value = ~"[a-z_][a-z_0-9]*"i _'
        name = node.text.strip()
        if not name in self.environment:
            raise LookupError('Variable "%s" not defined in scope.' % (name))
        else:
            return self.environment[name]

    def identifier_name(self, node, children):
        'identifier_name = ~"[a-z_][a-z_0-9]*"i _'
        return node.text.strip()

    def ws(self, nodee, children):
        'ws = ~"\s+"'

    def _(self, node, children):
        '_ = ~"\s*"'
