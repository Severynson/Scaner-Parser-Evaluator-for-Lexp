# Student: Severyn Kurach
# Project Phase: 3.1

from scaner import TokenType, scan_file_to_tokenized_lines
from parser import write_tokens, write_ast, parser
import os, sys, argparse

output_file = "test_output.txt"


def error(message):
    with open(output_file, "w") as file_to_write:
        file_to_write.write(f"Evaluation Error: {message}\n")
    sys.exit(1)


def evaluate_ast(ast_root):
    stack = []
    pre_order(ast_root, stack)

    if len(stack) != 1 or not isinstance(stack[0], int):
        error("Stack doesn't reduce to a single number.")

    return stack[0]


def pre_order(node, stack):
    if node is None:
        return

    token = node["value"]["token"]
    token_type = node["value"]["tokenType"]

    match token_type:
        case TokenType.NUM.value:
            try:
                stack.append(int(token))
            except ValueError:
                error(f"Invalid number literal: '{token}'")
        case TokenType.SYM.value if token in ["+", "-", "*", "/"]:
            stack.append(token)
        case TokenType.ID.value:
            error(f"Identifier '{token}' is not yet supported.")

    reduce_stack(stack)

    for child in node.get("children", []):
        pre_order(child, stack)
        reduce_stack(stack)


def reduce_stack(stack):
    if len(stack) < 3:
        return

    if (
        isinstance(stack[-1], int)
        and isinstance(stack[-2], int)
        and isinstance(stack[-3], str)
    ):
        right = stack.pop()
        left = stack.pop()
        operator = stack.pop()
        result = apply_operator(operator, left, right)
        stack.append(result)


def apply_operator(operator, left, right):
    match operator:
        case "+":
            return left + right
        case "-":
            return left - right
        case "*":
            return left * right
        case "/":
            if right == 0:
                error("Division by zero is not allowed.")
            return left // right
        case _:
            error(f"Unknown operator '{operator}'")


def test_driver(input_file, output_file):
    tokenized_lines = scan_file_to_tokenized_lines(input_file)
    parsed_tokens, ast = parser(
        tokenized_lines, return_parsed_tokens=True, starting_nonterminal="expression"
    )
    result = evaluate_ast(ast)

    with open(output_file, "w") as file_to_write:

        file_to_write.write("Tokens:\n\n")
        write_tokens(parsed_tokens, file_to_write)

        file_to_write.write("AST:\n\n")
        write_ast(ast, file_to_write)

        file_to_write.write("\n\nOutput: ")
        file_to_write.write(f"{result}\n")


def main():
    global output_file
    parser = argparse.ArgumentParser(description="parse based on the type of arguments")
    parser.add_argument("arguments", nargs="+", help="Runtime arguments")
    args = parser.parse_args()
    if len(args.arguments) in [1, 2] and os.path.exists(args.arguments[0]):
        input_file = args.arguments[0]
        if len(args.arguments) == 2:
            output_file = args.arguments[1]
        test_driver(
            input_file,
            output_file,
        )
    elif not os.path.exists(args.arguments[0]):
        if not "." in args.arguments[0]:
            print(
                f'Input file "{args.arguments[0]}" desn\'t incluide the file extension.'
            )
        else:
            print(f'Input file "{args.arguments[0]}" desn\'t exist')
    else:
        print(
            f'{f"{args.arguments}"} ERROR: the input format has to be "python3 evaluator.py <input_file_title> <output_file_title>" or "python3 evaluator.py <input_file_title>" .\n Instead {len(args.arguments)} arguments was passed.'
        )


if __name__ == "__main__":
    main()
