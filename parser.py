import os
import argparse
from scaner import scan_file_to_tokenized_lines, TokenType


initNode = lambda nodeValue, children, nodeType="non-terminal": {
    "value": nodeValue,
    "nodeType": nodeType,
    "children": children,
}


def parse_expression(tokens, pos):
    """Parse an expression: term { + term }"""
    node, pos = parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos]["token"] == "+":
        op = tokens[pos]
        right, pos = parse_term(tokens, pos + 1)
        node = initNode(op, [node, right])
    return node, pos


def parse_term(tokens, pos):
    """Parse a term: factor { - factor }"""
    node, pos = parse_factor(tokens, pos)
    while pos < len(tokens) and tokens[pos]["token"] == "-":
        op = tokens[pos]["token"]
        right, pos = parse_factor(tokens, pos + 1)
        node = initNode(op, [node, right])
    return node, pos


def parse_factor(tokens, pos):
    """Parse a factor: piece { / piece }"""
    node, pos = parse_piece(tokens, pos)
    while pos < len(tokens) and tokens[pos]["token"] == "/":
        op = tokens[pos]["token"]
        right, pos = parse_piece(tokens, pos + 1)
        node = initNode(op, [node, right])
    return node, pos


def parse_piece(tokens, pos):
    """Parse a piece: element { * element }"""
    node, pos = parse_element(tokens, pos)
    while pos < len(tokens) and tokens[pos]["token"] == "*":
        op = tokens[pos]["token"]
        right, pos = parse_element(tokens, pos + 1)
        node = initNode(op, [node, right])
    return node, pos


def parse_element(tokens, pos):
    """Parse an element: ( expression ) | NUMBER | IDENTIFIER"""
    if tokens[pos]["token"] == "(":
        node, pos = parse_expression(tokens, pos + 1)
        if tokens[pos]["token"] == ")":
            return node, pos + 1
        else:
            raise SyntaxError(f"Expected ')', found {tokens[pos]['token']}")
    elif tokens[pos]["tokenType"] == TokenType.NUM.value:
        node = initNode(tokens[pos], [], "terminal")
        return node, pos + 1
    elif tokens[pos]["tokenType"] == TokenType.ID.value:
        node = initNode(tokens[pos], [], "terminal")
        return node, pos + 1
    else:
        raise SyntaxError(f"Unexpected token: {tokens[pos]}")


def test_driver(a, b):
    AST = scan_file_to_tokenized_lines("input_file.txt")
    for line_num, node in enumerate(AST, start=1):
        tokens = node["tokens"]
        ast, _ = parse_expression(tokens, 0)
        print(f"Line {line_num}:")
        print(ast)


def main():
    parser = argparse.ArgumentParser(description="parse based on the type of arguments")
    parser.add_argument("arguments", nargs="+", help="Runtime arguments")
    args = parser.parse_args()
    if len(args.arguments) in [1, 2] and os.path.exists(args.arguments[0]):
        test_driver(
            args.arguments[0],
            args.arguments[1] if len(args.arguments) == 2 else "test_output.txt",
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
            f'{print(f"{args.arguments}")} ERROR: the input format has to be "python3 parser.py <input_file_title> <output_file_title>" or "python3 parser.py <input_file_title>" .\n Instead {len(args.arguments)} arguments was passed.'
        )


if __name__ == "__main__":
    main()
