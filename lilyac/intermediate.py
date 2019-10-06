from typing import List, Tuple, Dict

from lilyac import Token, Error, SemanticAction, Type


class Intermediate:

    symbols_table: Dict[str, Type] = ...
    quadruples: List[Tuple] = ...
    factor_pile: List = ...
    operator_pile: List = ...
    jump_pile: List = ...
    counter: int = ...
    last_token: Token = ...

    def __init__(self):
        self.symbols_table = {}
        self.quadruples = []
        self.factor_pile = []
        self.operator_pile = []
        self.jump_pile = []
        self.counter = 0

    def step(self, symbol):
        if isinstance(symbol, SemanticAction):
            symbol(self)
        elif isinstance(symbol, Token):
            self.last_token = symbol

    def generate_quadruple(self, operator='', op1='', op2='', result=''):
        quadruple = (operator, op1, op2, result)
        result = check_quadruple(quadruple)
        if isinstance(result, Error):
            pass
        else:
            self.quadruples.append(quadruple)

    def check_quadruple(self, quadruple: Tuple):
        operator, op1, op2, result = quadruple
        if operator in unary_operators:
            type_1 = symbols_table[op1]
            operation = unary_operators[operator]
            type_r = operation(type_1)
        elif operator in binary_operators:
            type_1 = symbols_table[op1]
            type_2 = symbols_table[op2]
            operation = binary_operators[operator]
            type_r = operation(type_1, type_2)
        if type_r != Type.Error:
            symbols_table[result] = type_r
            return
        else:
            return Error(lilyac.ERRORTYPEOP)


unary_operators = {
    r'!': lambda x: not x,
    'JF': Type.JF,
    # Add rest of operations
}

binary_operators = {
    r'+': lambda x, y: x + y,
    r'-': lambda x, y: x - y,
    r'*': lambda x, y: x * y,
    r'/': lambda x, y: x / y,
    r'%': lambda x, y: x % y,
    r'||': lambda x, y: x or y,
    r'&&': lambda x, y: x and y,
    r'<': lambda x, y: x < y,
    r'<=': lambda x, y: x <= y,
    r'>': lambda x, y: x > y,
    r'>=': lambda x, y: x >= y,
    r'==': lambda x, y: x == y,
    r'!=': lambda x, y: x != y,
}
