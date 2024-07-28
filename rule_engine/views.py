from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Rule
from .utils import create_rule, evaluate_rule,RuleParseException
from django.shortcuts import render

def create_rule_view(request):
    if request.method == 'POST':
        rule_string = request.POST.get('rule_string')
        try:
            ast_root = create_rule(rule_string)
            Rule.objects.create(name='New Rule', rule_string=rule_string)
            return JsonResponse({'message': 'Rule created', 'AST': str(ast_root)})
        except RuleParseException as e:
            return JsonResponse({'error': str(e)})
    return render(request, 'create_rule.html')

def evaluate_rule_view(request):
    if request.method == 'POST':
        rule_id = request.POST.get('rule_id')
        data = request.POST.get('data')
        try:
            rule = Rule.objects.get(id=rule_id)
            ast_root = create_rule(rule.rule_string)
            result = evaluate_rule(ast_root, eval(data))
            return JsonResponse({'result': result})
        except Rule.DoesNotExist:
            return JsonResponse({'error': 'Rule not found'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return render(request, 'evaluate_rule.html')
import re

def validate_rule_string(rule_string):
    # Basic validation to check for balanced parentheses and valid operators
    if rule_string.count('(') != rule_string.count(')'):
        raise RuleParseException("Unbalanced parentheses")
    if not re.match(r"^[\w\s><=()ANDOR']+$", rule_string):
        raise RuleParseException("Invalid characters in rule string")

def create_rule(rule_string):
    validate_rule_string(rule_string)
    # Parsing logic remains the same
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Rule, Node
import json

@csrf_exempt
def create_rule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rule_string = data.get('rule_string')
            rule_name = data.get('name')
            rule_description = data.get('description')

            if not rule_string or not rule_name:
                return HttpResponseBadRequest('Rule string and name are required.')

            rule = Rule.objects.create(name=rule_name, description=rule_description)
            root_node = parse_rule_string_to_ast(rule_string, rule)
            
            return JsonResponse({'message': 'Rule created', 'rule_id': rule.id})

        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON format.')
        except Exception as e:
            return HttpResponseBadRequest(str(e))

def parse_rule_string_to_ast(rule_string, rule):
    tokens = tokenize_rule_string(rule_string)
    if not tokens:
        raise ValidationError("Invalid rule string.")
    root_node = build_ast(tokens, rule)
    return root_node

@csrf_exempt
def evaluate_rule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rule_id = data.get('rule_id')
            user_data = data.get('user_data')

            if not rule_id or not user_data:
                return HttpResponseBadRequest('Rule ID and user data are required.')

            rule = Rule.objects.get(id=rule_id)
            root_node = rule.nodes.filter(left_child__isnull=True, right_child__isnull=True).first()

            result = evaluate_ast(root_node, user_data)
            
            return JsonResponse({'result': result})

        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON format.')
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Rule not found.')
        except Exception as e:
            return HttpResponseBadRequest(str(e))

def evaluate_ast(node, user_data):
    if node.node_type == 'operand':
        if node.value.isdigit():
            return int(node.value)
        if node.value not in user_data:
            raise ValidationError(f"Missing attribute: {node.value}")
        return user_data.get(node.value)

    left_value = evaluate_ast(node.left, user_data)
    right_value = evaluate_ast(node.right, user_data)

    if node.value == 'and':
        return left_value and right_value
    if node.value == 'or':
        return left_value or right_value

    # Assuming basic comparison operators
    if node.value in ['>', '<', '==', '!=', '>=', '<=']:
        return eval(f'{left_value} {node.value} {right_value}')

    return False
