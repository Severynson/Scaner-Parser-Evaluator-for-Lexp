import os
import argparse
from scaner import scan_file_to_tokenized_lines, TokenType


initNode = lambda nodeValue, children, nodeType="non-terminal": {
    "value": nodeValue,
    "nodeType": nodeType,
    "children": children,
}


def parse_expression(tokens, position):
    """Parse an expression: term { + term }"""
    node, position = parse_term(tokens, position)
    while position < len(tokens) and tokens[position]["token"] == "+":
        operator = tokens[position]
        right, position = parse_term(tokens, position + 1)
        node = initNode(operator, [node, right])
    return node, position


def parse_term(tokens, position):
    """Parse a term: factor { - factor }"""
    node, position = parse_factor(tokens, position)
    while position < len(tokens) and tokens[position]["token"] == "-":
        operator = tokens[position]
        right, position = parse_factor(tokens, position + 1)
        node = initNode(operator, [node, right])
    return node, position


def parse_factor(tokens, position):
    """Parse a factor: piece { / piece }"""
    node, position = parse_piece(tokens, position)
    while position < len(tokens) and tokens[position]["token"] == "/":
        operator = tokens[position]
        right, position = parse_piece(tokens, position + 1)
        node = initNode(operator, [node, right])
    return node, position


def parse_piece(tokens, position):
    """Parse a piece: element { * element }"""
    node, position = parse_element(tokens, position)
    while position < len(tokens) and tokens[position]["token"] == "*":
        operator = tokens[position]
        right, position = parse_element(tokens, position + 1)
        node = initNode(operator, [node, right])
    return node, position


def parse_element(tokens, position):
    """Parse an element: ( expression ) | NUMBER | IDENTIFIER"""
    if tokens[position]["token"] == "(":
        node, position = parse_expression(tokens, position + 1)
        if tokens[position]["token"] == ")":
            return node, position + 1
        else:
            raise SyntaxError(f"Expected ')', found {tokens[position]['token']}")
    elif tokens[position]["tokenType"] == TokenType.NUM.value:
        node = initNode(tokens[position], [], "terminal")
        return node, position + 1
    elif tokens[position]["tokenType"] == TokenType.ID.value:
        node = initNode(tokens[position], [], "terminal")
        return node, position + 1
    else:
        raise SyntaxError(f"Unexpected token: {tokens[position]}")


def write_ast(node, file_to_write, indentation=0):
    if node:

        indentations = "\t" * indentation
        file_to_write.write(
            f"{indentations}{(node['value'])['token']} : {(node['value'])['tokenType']}\n"
        )

        for child in node["children"]:
            write_ast(child, file_to_write, indentation + 1)
    else:
        file_to_write.write("")


def test_driver(input_file, output_file="test_output.txt"):
    tokenized_lines = scan_file_to_tokenized_lines(input_file)
    with open(output_file, "w") as file_to_write:
        for tokenized_line in tokenized_lines:
            ast, _ = parse_expression(tokenized_line["tokens"], 0)
            file_to_write.write(
                f'Line {tokenized_line["line_number"]} "{tokenized_line["line"]}":\n'
            )
            write_ast(ast, file_to_write)


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
