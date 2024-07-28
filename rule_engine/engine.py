import re
import json

def parse_rule(rule_string):
    tokens = tokenize(rule_string)
    return parse_expression(tokens)

def tokenize(rule_string):
    token_pattern = r"\s*(AND|OR|[()]|[a-zA-Z_][a-zA-Z_0-9]*|<=|>=|!=|==|>|<|=|\d+|'[^']*')\s*"
    return re.findall(token_pattern, rule_string)

def parse_expression(tokens):
    stack = []
    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            right = stack.pop()
            operator = stack.pop()
            left = stack.pop()
            stack.pop()  # Remove opening '('
            stack.append(Node('operator', operator, left, right))
        elif token in ('AND', 'OR'):
            stack.append(token)
        else:
            stack.append(Node('operand', token))
    return stack.pop()

def evaluate_ast(ast, data):
    if ast['type'] == 'operator':
        if ast['value'] == 'AND':
            return evaluate_ast(ast['left'], data) and evaluate_ast(ast['right'], data)
        elif ast['value'] == 'OR':
            return evaluate_ast(ast['left'], data) or evaluate_ast(ast['right'], data)
    elif ast['type'] == 'operand':
        return evaluate_condition(ast['value'], data)
    return False

def evaluate_condition(condition, data):
    match = re.match(r"(\w+)\s*(==|!=|<=|>=|<|>)\s*('[^']*'|\d+)", condition)
    if not match:
        return False

    attr, operator, value = match.groups()
    attr_value = data.get(attr)

    if value.startswith("'"):
        value = value.strip("'")
    else:
        value = int(value)

    operators = {
        '==': lambda a, b: a == b,
        '!=': lambda a, b: a != b,
        '<=': lambda a, b: a <= b,
        '>=': lambda a, b: a >= b,
        '<': lambda a, b: a < b,
        '>': lambda a, b: a > b
    }

    return operators[operator](attr_value, value)

def evaluate_rule(rule, data):
    ast = json.loads(rule.ast)
    return evaluate_ast(ast, data)
