from flask import Flask, request, render_template_string, jsonify
import re
import pdb

app = Flask(__name__)

index_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced AST Parser</title>
</head>
<body>
    <h1>Advanced AST Parser and Evaluator</h1>
    <form action="/create_rule" method="post">
        <label for="rule">Enter Rule:</label>
        <input type="text" id="rule" name="rule" required>
        <button type="submit">Parse Rule</button>
    </form>
    <form action="/evaluate_rule" method="post">
        <h3>Evaluate Rule</h3>
        <label for="eval_rule">Enter Rule to Evaluate:</label>
        <input type="text" id="eval_rule" name="eval_rule" required>
        <br>
        <label for="variables">Enter Variables (key=value, separated by commas):</label>
        <input type="text" id="variables" name="variables" required>
        <button type="submit">Evaluate</button>
    </form>
    <form action="/combine_rules" method="post">
        <h3>Combine Rules</h3>
        <label for="rules">Enter Rules (separated by commas):</label>
        <input type="text" id="rules" name="rules" required>
        <button type="submit">Combine</button>
    </form>
    <div id="result">
        {% if result %}
            <h2>Result:</h2>
            <pre>{{ result }}</pre>
        {% endif %}
    </div>
</body>
</html>
 '''



# class Token:
#     def __init__(self, type, value):
#         self.type = type
#         self.value = value

#     def __repr__(self):
#         return f"Token(type={self.type}, value={self.value})"

# def tokenize(rule_string):
#     tokens = []
#     token_spec = [
#         ('NUMBER', r'\b\d+(\.\d+)?\b'),
#         ('STRING', r'\'[^\']*\''),
#         ('BOOL', r'\b(True|False)\b'),
#         ('ID', r'\b\w+\b'),
#         ('OP', r'==|!=|<=|>=|<|>|='),
#         ('LOGIC', r'\bAND\b|\bOR\b'),
#         ('PAREN', r'[()]')
#     ]
#     token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_spec)
#     for match in re.finditer(token_regex, rule_string):
#         kind = match.lastgroup
#         value = match.group()
#         if kind == 'BOOL':
#             tokens.append(Token(kind, value == 'True'))
#         else:
#             tokens.append(Token(kind, value))
#     return tokens

# class ASTNode:
#     def __init__(self, value, left=None, right=None):
#         self.value = value
#         self.left = left
#         self.right = right

#     def __repr__(self):
#         left_str = repr(self.left) if self.left else 'None'
#         right_str = repr(self.right) if self.right else 'None'
#         return f"ASTNode(value={self.value}, left={left_str}, right={right_str})"

# def shunting_yard(tokens):
#     output = []
#     operator_stack = []
#     precedence = {'AND': 2, 'OR': 1, '>': 3, '<': 3, '>=': 3, '<=': 3, '=': 3}
#     associativity = {'AND': 'L', 'OR': 'L', '>': 'L', '<': 'L', '>=': 'L', '<=': 'L', '=': 'L'}

#     for token in tokens:
#         if token.type in ('NUMBER', 'STRING', 'ID', 'BOOL'):
#             output.append(token)
#         elif token.type in ('OP', 'LOGIC'):
#             while operator_stack and operator_stack[-1].type != 'PAREN' and (
#                 precedence[operator_stack[-1].value] > precedence[token.value] or
#                 (precedence[operator_stack[-1].value] == precedence[token.value] and associativity[token.value] == 'L')
#             ):
#                 output.append(operator_stack.pop())
#             operator_stack.append(token)
#         elif token.type == 'PAREN':
#             if token.value == '(':
#                 operator_stack.append(token)
#             elif token.value == ')':
#                 while operator_stack and operator_stack[-1].type != 'PAREN':
#                     output.append(operator_stack.pop())
#                 operator_stack.pop()  # Remove '('

#     while operator_stack:
#         output.append(operator_stack.pop())

#     return output


# # def build_ast(postfix_tokens, rule_string):
# #     """Build AST from postfix tokens with detailed debug information."""
# #     stack = []
# #     for token in postfix_tokens:
# #         print("Processing token:", token)
# #         if token.type not in ('LOGIC', 'OP'):
# #             print("Pushing operand token to stack:", token)
# #             stack.append(ASTNode(token.value, left=token))  # Store as left to keep token info
# #         else:
# #             print("Processing operator:", token.value)
# #             # Pop two operands for binary operator
# #             if len(stack) < 2:
# #                 raise ValueError(f"Insufficient operands for operator '{token.value}' in expression: '{rule_string}'")

# #             right = stack.pop()
# #             left = stack.pop()
# #             print(f"Creating ASTNode with operator {token.value}, left={left}, right={right}")
# #             stack.append(ASTNode(token.value, left=left, right=right))

# #     print("Stack:", stack)
# #     if len(stack) != 1:
# #         raise ValueError(f"Error in AST construction: Check expression syntax. Remaining stack: {stack}")

# #     print("Final AST root node:", stack[0])
# #     return stack.pop()

# def build_ast(postfix_tokens, rule_string):
#     stack = []
#     for node in postfix_tokens:
#         if node.type in ('NUMBER', 'STRING', 'ID', 'BOOL'):
#             stack.append(ASTNode(node.value, Token(node.type, node.value)))
#             print("Pushed operand:", stack[-1])
#         elif node.type in ('OP', 'LOGIC'):
#             if len(stack) < 2:
#                 raise ValueError(f"Insufficient operands for operator '{node.value}' in expression: '{rule_string}'")
#             right = stack.pop()
#             left = stack.pop()
#             stack.append(ASTNode(node.value, left, right))
#             print("Created ASTNode:", stack[-1])

#     if len(stack) != 1:
#         print("Remaining stack:", stack)
#         raise ValueError(f"Error in AST construction: Check expression syntax. Remaining stack: {stack}")

#     return stack.pop()


# # def evaluate_ast(node, data):
# #     if isinstance(node, Token):
# #         print("Your node is of token type!")
# #         if node.type == 'BOOL':
# #             print("bool")
# #             return node.value
# #         elif node.type == 'ID':
# #             value = data.get(node.value)
# #             print("ID")
# #             if value is None:
# #                 raise ValueError(f"Variable '{node.value}' not found in data")
# #             return value
# #         elif node.type == 'STRING':
# #             print("string")
# #             return node.value.strip("'")
# #         elif node.type == 'NUMBER':
# #             print("number")
# #             return float(node.value)

# #     elif isinstance(node, ASTNode):
# #         print("Your node is of AST Node type!")
# #         left_val = evaluate_ast(node.left, data)
# #         print(node.value)
# #         print("Left value : ",left_val)
# #         right_val = evaluate_ast(node.right, data)
# #         print("Right value: ", right_val)

# #         if node.value == 'AND':
# #             print(node.value)
# #             print("Comparing and")
# #             return bool(left_val) and bool(right_val)
# #         elif node.value == 'OR':
# #             print("Comparing or")
# #             return bool(left_val) or bool(right_val)

# #         if node.value == '=':
# #             print("==================================")
# #             return left_val == right_val
# #         if node.value == '>':
# #             print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
# #             return left_val > right_val
# #         if node.value == '<':
# #             print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
# #             return left_val < right_val
# #         if node.value == '>=':
# #             print(">>>>>>>>>>>>>>>>>>>====================")
# #             return left_val >= right_val
# #         if node.value == '<=':
# #             print("<<<<<<<<<<<<<<<<<<===================")
# #             return left_val <= right_val

# #     raise ValueError(f"Unexpected node type or comparison in ASTNode: {node}")

# def evaluate_ast(node, data):
#     """Evaluate AST nodes with enhanced debugging."""
#     if isinstance(node, Token):
#         print(f"Evaluating Token node: {node}")
#         if node.type == 'BOOL':
#             return node.value
#         elif node.type == 'ID':
#             value = data.get(node.value)
#             if value is None:
#                 raise ValueError(f"Variable '{node.value}' not found in data")
#             return value
#         elif node.type == 'STRING':
#             return node.value.strip("'")
#         elif node.type == 'NUMBER':
#             return float(node.value)

#     elif isinstance(node, ASTNode):
#         print(f"Evaluating ASTNode with operator: {node.value}")
        
#         # Evaluate left and right nodes, with debugging for each step
#         if node.left:
#             left_val = evaluate_ast(node.left, data)
#             print(f"Left value of node '{node.value}' evaluated to: {left_val}")
#         else:
#             left_val = None
#             print(f"No left child for node '{node.value}'")

#         if node.right:
#             right_val = evaluate_ast(node.right, data)
#             print(f"Right value of node '{node.value}' evaluated to: {right_val}")
#         else:
#             right_val = None
#             print(f"No right child for node '{node.value}'")

#         # Process logical operations
#         if node.value == 'AND':
#             return bool(left_val) and bool(right_val)
#         elif node.value == 'OR':
#             return bool(left_val) or bool(right_val)

#         # Process comparison operations with validation
#         if node.value == '=':
#             return left_val == right_val
#         if node.value == '>':
#             return left_val > right_val
#         if node.value == '<':
#             return left_val < right_val
#         if node.value == '>=':
#             return left_val >= right_val
#         if node.value == '<=':
#             return left_val <= right_val

#     # Raise error if node type or comparison is unexpected
#     raise ValueError(f"Unexpected node type or comparison in ASTNode: {node}")




# @app.route('/')
# def index():
#     return render_template_string(index_template)

# @app.route('/create_rule', methods=['POST'])
# def create_rule_endpoint():
#     rule_string = request.form['rule']
#     try:
#         tokens = tokenize(rule_string)
#         postfix_tokens = shunting_yard(tokens)
#         ast_root = build_ast(postfix_tokens, rule_string)
#         result = f"AST: {ast_root}"
#     except Exception as e:
#         result = f"Error: {str(e)}"
#     return render_template_string(index_template, result=result)

# @app.route('/evaluate_rule', methods=['POST'])
# def evaluate_rule_endpoint():
#     eval_rule = request.form['eval_rule']
#     variables_input = request.form['variables']
#     data = {}

#     try:
#         for var in variables_input.split(','):
#             key, value = var.split('=')
#             if value.lower() in ['true', 'false']:
#                 data[key.strip()] = value.lower() == 'true'
#             elif value.isdigit():
#                 data[key.strip()] = int(value)
#             else:
#                 try:
#                     data[key.strip()] = float(value)
#                 except ValueError:
#                     data[key.strip()] = value.strip("'")

#         tokens = tokenize(eval_rule)
#         postfix_tokens = shunting_yard(tokens)
#         ast_root = build_ast(postfix_tokens, eval_rule)
#         print("AST constructed successfully:", ast_root)
#         result = evaluate_ast(ast_root, data)
#         result_string = f"Evaluated Result: {result}"
#         # return f"Evaluated Result: {result}"
#     except Exception as e:
#         result_string = f"Error: {str(e)}"
    
#     return render_template_string(index_template, result=result_string)

# if __name__ == '__main__':
#     app.run(debug=True)
































class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token(type={self.type}, value={self.value})"

def tokenize(rule_string):
    tokens = []
    token_spec = [
        ('NUMBER', r'\b\d+(\.\d+)?\b'),
        ('STRING', r'\'[^\']*\''),
        ('BOOL', r'\b(True|False)\b'),  # Added boolean literal recognition
        ('ID', r'\b\w+\b'),
        ('OP', r'==|!=|<=|>=|<|>|='),
        ('LOGIC', r'\bAND\b|\bOR\b'),
        ('PAREN', r'[()]')
    ]
    token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_spec)
    for match in re.finditer(token_regex, rule_string):
        kind = match.lastgroup
        value = match.group()
        # Convert boolean strings to proper boolean tokens
        if kind == 'BOOL':
            tokens.append(Token(kind, value == 'True'))
        else:
            tokens.append(Token(kind, value))
    return tokens

class ASTNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        left_str = repr(self.left) if self.left else 'None'
        right_str = repr(self.right) if self.right else 'None'
        return f"ASTNode(value={self.value}, left={left_str}, right={right_str})"

def shunting_yard(tokens):
    output = []
    operator_stack = []
    precedence = {'AND': 2, 'OR': 1, '>': 3, '<': 3, '>=': 3, '<=': 3, '=': 3}
    associativity = {'AND': 'L', 'OR': 'L', '>': 'L', '<': 'L', '>=': 'L', '<=': 'L', '=': 'L'}

    for token in tokens:
        if token.type in ('NUMBER', 'STRING', 'ID', 'BOOL'):  # Added BOOL to operands
            output.append(token)
        elif token.type in ('OP', 'LOGIC'):
            while operator_stack and operator_stack[-1].type != '(' and (
                    precedence[operator_stack[-1].value] > precedence[token.value] or
                    (precedence[operator_stack[-1].value] == precedence[token.value] and
                     associativity[token.value] == 'L')
            ):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        elif token.type == '(':
            operator_stack.append(token)
        elif token.type == ')':
            while operator_stack and operator_stack[-1].type != '(':
                output.append(operator_stack.pop())
            if not operator_stack:
                raise ValueError("Mismatched parentheses")
            operator_stack.pop()

    while operator_stack:
        if operator_stack[-1].type == '(':
            raise ValueError("Mismatched parentheses")
        output.append(operator_stack.pop())

    return output

def build_ast(postfix_tokens, rule_string):
    stack = []
    for node in postfix_tokens:
        if node.value not in {'AND', 'OR', '>', '<', '>=', '<=', '='}:
            stack.append(node)
        else:
            if len(stack) < 2:
                raise ValueError(f"Insufficient operands for operator '{node.value}' in expression: '{rule_string}'")
            right = stack.pop()
            left = stack.pop()
            stack.append(ASTNode(node.value, left, right))

    if len(stack) != 1:
        raise ValueError(f"Error in AST construction: Check expression syntax. Remaining stack: {stack}")

    return stack.pop()

# def evaluate_ast(node, data):
#     print(node, data, type(node), type(data))
#     print("Evaluating Node:", node)
#     print("Data:", data)
#     if isinstance(node, Token):
#         if node.type == 'BOOL':
#             return node.value
#         if node.type == 'ID':
#             value = data.get(node.value)
#             if value is None:
#                 raise ValueError(f"Variable '{node.value}' not found in data")
#             return value
#         if node.type == 'STRING':
#             # Remove quotes from string literals
#             return node.value.strip("'")
#         try:
#             return float(node.value)
#         except ValueError:
#             return node.value

#     left_val = evaluate_ast(node.left, data)
#     print("Left value: ",left_val)
#     right_val = evaluate_ast(node.right, data)
#     print("Right value: ", right_val)

#     # Handle logical operations
#     if node.value == 'AND':
#         print("Performing AND operation")
#         return bool(left_val) and bool(right_val)
#     elif node.value == 'OR':
#         print("Performing OR operation")
#         return bool(left_val) or bool(right_val)

#     # # Handle equality comparison
#     # if node.value == '=':
#     #     # Convert string representations of booleans
#     #     if isinstance(left_val, str) and left_val.lower() in ['true', 'false']:
#     #         left_val = left_val.lower() == 'true'
#     #     if isinstance(right_val, str) and right_val.lower() in ['true', 'false']:
#     #         right_val = right_val.lower() == 'true'
        
#     #     # Now compare the values
#     #     if isinstance(left_val, bool) or isinstance(right_val, bool):
#     #         return bool(left_val) == bool(right_val)
#     #     elif isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
#     #         return left_val == right_val
#     #     else:
#     #         return str(left_val) == str(right_val)

#     # Handle equality comparison with type checking
#     if node.value == '=':
#         # Check if types are compatible for equality comparison
#         if type(left_val) != type(right_val):
#             raise ValueError(f"You are tyring to compare two different values: {left_val} ({type(left_val)}) and {right_val} ({type(right_val)})")
#             return False  # Return False if types are incompatible
#         # Now compare the values
#         print("Performing Equality Check")
#         return left_val == right_val

#     # Handle numeric comparisons
#     if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
#         if node.value == '>':
#             print("Performing Greater Than Check")
#             return left_val > right_val
#         elif node.value == '<':
#             print("Performing Less Than Check")
#             return left_val < right_val
#         elif node.value == '>=':
#             print("Performing Greater Than Equal to Check")
#             return left_val >= right_val
#         elif node.value == '<=':
#             print("Performing Less Than equal to Check")
#             return left_val <= right_val

#     raise ValueError(f"Invalid comparison between {left_val} ({type(left_val)}) and {right_val} ({type(right_val)})")


def evaluate_ast(node, data):
    if isinstance(node, Token):  # If node is a Token, evaluate directly
        print("Evaluating Token:", node)
        
        if node.type == 'BOOL':
            return node.value
        elif node.type == 'ID':
            # Fetch the variable's value from data
            value = data.get(node.value)
            if value is None:
                raise ValueError(f"Variable '{node.value}' not found in data")
            return value
        elif node.type == 'STRING':
            return node.value.strip("'")
        
        try:
            return float(node.value)
        except ValueError:
            return node.value

    elif isinstance(node, ASTNode):  # Check if the node is of type ASTNode
        print("Evaluating ASTNode:", node, "with value:", node.value)
        
        left_val = evaluate_ast(node.left, data)
        print("Left value evaluated:", left_val)
        
        right_val = evaluate_ast(node.right, data)
        print("Right value evaluated:", right_val)

        # Handle logical operations
        if node.value == 'AND':
            print("Performing AND operation")
            return bool(left_val) and bool(right_val)
        elif node.value == 'OR':
            print("Performing OR operation")
            return bool(left_val) or bool(right_val)

        # Handle equality comparison
        if node.value == '=':
            print("Performing Equality Check")
            # Check types and equality
            if isinstance(left_val, bool) or isinstance(right_val, bool):
                return bool(left_val) == bool(right_val)
            elif isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val == right_val
            else:
                return str(left_val) == str(right_val)

        # Handle numeric comparisons, ensuring type compatibility
        if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
            if node.value == '>':
                return left_val > right_val
            elif node.value == '<':
                return left_val < right_val
            elif node.value == '>=':
                return left_val >= right_val
            elif node.value == '<=':
                return left_val <= right_val

    # If node or type is unexpected, raise an error with details
    raise ValueError(f"Unexpected node type or invalid comparison: {node}, {node.value}, left={left_val}, right={right_val}")



def create_rule(rule_string):
    tokens = tokenize(rule_string)
    postfix_tokens = shunting_yard(tokens)
    return build_ast(postfix_tokens, rule_string)

def combine_rules(rules, operator="OR"):
    combined_rule = f" ({' ' + operator + ' '.join(rules)})" 
    return create_rule(combined_rule)

@app.route('/')
def index():
    return render_template_string(index_template)

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.form['rule']
    try:
        ast_root = create_rule(rule_string)
        result = f"AST: {ast_root}"
    except Exception as e:
        result = f"Error: {str(e)}"
    return render_template_string(index_template, result=result)

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    eval_rule = request.form['eval_rule']
    variables_input = request.form['variables']
    data = {}
    try:
        # Parse the variables input
        for var in variables_input.split(','):
            key, value = var.split('=')
            key = key.strip()
            value = value.strip().strip("'")  # Remove any surrounding single quotes

            # Handle boolean values
            if value.lower() in ['true', 'false']:
                data[key] = value.lower() == 'true'
            elif value.isdigit():
                data[key] = int(value)
            else:
                try:
                    data[key] = float(value)
                except ValueError:
                    data[key] = value

        ast_root = create_rule(eval_rule)
        result = evaluate_ast(ast_root, data)
        result_string = f"AST: {ast_root}\nEvaluated Result: {result}"
    except Exception as e:
        result_string = f"Error: {str(e)}"
    
    return render_template_string(index_template, result=result_string)

if __name__ == '__main__':
    app.run(debug=True)