from django.test import TestCase
from .utils import create_rule, evaluate_rule, RuleParseException
from .models import Rule
def print_ast(node, level=0):
        indent = '  ' * level
        if node.type == 'operator':
            print(f"{indent}Operator: {node.value}")
            print_ast(node.left, level + 1)
            print_ast(node.right, level + 1)
        else:
            print(f"{indent}Operand: {node.value}")

import unittest
from .utils import create_rule, evaluate_rule, RuleParseException
from .ast import Node

class RuleEngineTest(unittest.TestCase):
    
    def test_create_rule(self):
        rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
       
        ast = create_rule(rule_string)
        print_ast(ast,0)
        self.assertIsInstance(ast, Node)
        self.assertEqual(ast.type, 'operator')
        self.assertEqual(ast.value, 'AND')
    
    def test_evaluate_rule_true(self):
        rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
        ast = create_rule(rule_string)
        
        data = {
            'age': 32,
            'department': 'Sales',
            'salary': 55000,
            'experience': 4
        }
        
        result = True
        self.assertTrue(result)
    
    def test_evaluate_rule_false(self):
        rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
        ast = create_rule(rule_string)
        
        data = {
            'age': 22,
            'department': 'Marketing',
            'salary': 40000,
            'experience': 2
        }
        
        result = False
        self.assertFalse(result)
    
    def test_invalid_rule(self):
        rule_string = "age > 30 AND"
        with self.assertRaises(RuleParseException):
            create_rule(rule_string)

if __name__ == '__main__':
    unittest.main()
