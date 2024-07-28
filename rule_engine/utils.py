
from .ast import Node

class RuleParseException(Exception):
    pass

from .ast import Node

class RuleParseException(Exception):
    pass
def create_rule(rule_string):
    rule_string = rule_string.strip()
    
    if rule_string.startswith('(') and rule_string.endswith(')'):
        rule_string = rule_string[1:-1].strip()
    
    open_parens = 0
    main_operator = None
    main_operator_pos = -1
    found_and = False

    for i in range(len(rule_string)):
        if rule_string[i] == '(':
            open_parens += 1
        elif rule_string[i] == ')':
            open_parens -= 1
        elif open_parens == 0:
            if rule_string[i:i+4] == ' AND' and not found_and:
                main_operator = 'AND'
                main_operator_pos = i
                found_and = True
            elif rule_string[i:i+3] == ' OR' and not found_and:
                main_operator = 'OR'
                main_operator_pos = i

    if main_operator:
        left = rule_string[:main_operator_pos].strip()
        right = rule_string[main_operator_pos + len(main_operator):].strip()
        return Node(node_type='operator', left=create_rule(left), right=create_rule(right), value=main_operator)
    
    parts = rule_string.split(' ', 2)
    if len(parts) != 3:
        raise RuleParseException("Invalid operand format")
    return Node(node_type='operand', value=rule_string.strip())

def evaluate_rule(node, data):
    try:
        if node.type == 'operator':
            if node.value == 'AND':
                return evaluate_rule(node.left, data) and evaluate_rule(node.right, data)
            elif node.value == 'OR':
                return evaluate_rule(node.left, data) or evaluate_rule(node.right, data)
        else:
            attribute, operator, value = node.value.split(' ', 2)
            attribute_value = data.get(attribute)

            # Handle string comparisons
            if isinstance(attribute_value, str):
                value = value.strip("'")
                return eval(f"'{attribute_value}' {operator} '{value}'")
            else:
                return eval(f"{attribute_value} {operator} {value}")
    except Exception as e:
        raise RuleParseException(f"Error evaluating rule: {e}")
