def evaluate_ast(ast_root: dict) -> int:
    stack = []
    pre_order(ast_root, stack)
    
    if len(stack) != 1 or not isinstance(stack[0], int):
        raise Exception("Final stack did not reduce to a single number.")

    return stack[0]

def pre_order(node: dict, stack: list):
    if node is None:
        return

    token = node['value']['token']
    token_type = node['value']['tokenType']
    
    if token_type == 'number':
        stack.append(int(token))
    elif token_type == 'symbol' and token in ['+', '-', '*', '/']:
        stack.append(token)
    elif token_type == 'identifier':
        raise Exception(f"Identifier '{token}' is not supported.")
    
    try_reduce_stack(stack)

    for child in node.get('children', []):
        pre_order(child, stack)
        try_reduce_stack(stack)

def try_reduce_stack(stack: list):
    if len(stack) < 3:
        return

    if isinstance(stack[-1], int) and isinstance(stack[-2], int) and isinstance(stack[-3], str):
        right = stack.pop()
        left = stack.pop()
        op = stack.pop()
        result = apply_operator(op, left, right)
        stack.append(result)

def apply_operator(op: str, left: int, right: int) -> int:
    if op == '+':
        return left + right
    elif op == '-':
        return max(0, left - right)
    elif op == '*':
        return left * right
    elif op == '/':
        if right == 0:
            raise ZeroDivisionError("Division by zero")
        return left // right
    else:
        raise Exception(f"Unknown operator '{op}'")
    
