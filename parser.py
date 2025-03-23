# Student: Severyn Kurach
# Project Phase: 2.1

import os, sys, argparse
from scaner import scan_file_to_tokenized_lines, TokenType

line_currently_parsed, line_num_currently_parsed = None, None
output_file = "test_output.txt"


init_node = lambda nodeValue, children, nodeType="non-terminal": {
    "value": nodeValue,
    "nodeType": nodeType,
    "children": children,
}


# def parse_statement(tokens, position):
#     """Parse a statement: basestatement { ; basestatement }"""
#     if position >= len(tokens):
#         error("Unexpected end of input, expected a basestatement after statement")
#     node, position = parse_basestatement(tokens, position)
#     while position < len(tokens) and tokens[position]["token"] == ";":
#         operator = tokens[position]
#         right, position = parse_basestatement(tokens, position + 1)
#         node = init_node(operator, [node, right])
#     return node, position


# def parse_basestatement(tokens, position):
#     """Parse a basestatement: assignment | ifstatement | whilestatement | skip"""
#     if position >= len(tokens):
#         error("Unexpected end of input, expected a basestatement")
#     current_token = tokens[position]
#     if current_token["tokenType"] == TokenType.ID.value:
#         return parse_assignment(tokens, position)
#     elif current_token["token"] == "if":
#         return parse_ifstatement(tokens, position)
#     elif current_token["token"] == "while":
#         return parse_whilestatement(tokens, position)
#     elif current_token["token"] == "skip":
#         return parse_skip(tokens, position)
#     else:
#         error(
#             "Unexpected end of input, an ssignment, ifstatement, whilestatement or skip was expected after basestatement"
#         )


# def parse_assignment(tokens, position):
#     """Parse an assignment: IDENTIFIER := expression"""
#     if position >= len(tokens):
#         error(
#             "Unexpected end of input, expected DENTIFIER, := and expression after assignment"
#         )

#     identifier = tokens[position]
#     if identifier["tokenType"] != TokenType.ID.value:
#         error(f'Expected IDENTIFIER, got "{identifier["token"]}".')
#     identifier = init_node(identifier, [], "terminal")
#     position += 1

#     if position >= len(tokens) or tokens[position]["token"] != ":=":
#         error("Expected ':=' after identifier in assignment")
#     operator = tokens[position]
#     position += 1
#     expression, position = parse_expression(tokens, position)

#     node = init_node(operator, [identifier, expression])
#     return node, position


# def parse_ifstatement(tokens, position):
#     """Parse an ifstatement: if expression then statement else statement endif"""
#     if_token = tokens[position]
#     position += 1

#     condition, position = parse_expression(tokens, position)

#     if position >= len(tokens) or tokens[position]["token"] != "then":
#         error("Expected 'then' after if condition")
#     position += 1

#     then_statement, position = parse_statement(tokens, position)

#     if position >= len(tokens) or tokens[position]["token"] != "else":
#         error("Expected 'else' in if statement")
#     position += 1

#     else_statement, position = parse_statement(tokens, position)

#     if position >= len(tokens) or tokens[position]["token"] != "endif":
#         error("Expected 'endif' at end of if statement")
#     position += 1

#     node = init_node(if_token, [condition, then_statement, else_statement])
#     return node, position


# def parse_whilestatement(tokens, position):
#     """Parse a whilestatement: while expression do statement endwhile"""
#     pass


# def parse_skip(tokens, position):
#     """Parse a skip statement"""
#     return init_node(tokens[position], [], "terminal")


def parse_expression(tokens, position):
    """Parse an expression: term { + term }"""
    if position >= len(tokens):
        error("Unexpected end of input, expected a term after expression")
    node, position = parse_term(tokens, position)
    while position < len(tokens) and tokens[position]["token"] == "+":
        operator = tokens[position]
        right, position = parse_term(tokens, position + 1)
        node = init_node(operator, [node, right])
    return node, position


def parse_term(tokens, position):
    """Parse a term: factor { - factor }"""
    if position >= len(tokens):
        error("Unexpected end of input, expected a factor after term")
    node, position = parse_factor(tokens, position)
    while position < len(tokens) and tokens[position]["token"] == "-":
        operator = tokens[position]
        right, position = parse_factor(tokens, position + 1)
        node = init_node(operator, [node, right])
    return node, position


def parse_factor(tokens, position):
    """Parse a factor: piece { / piece }"""
    if position >= len(tokens):
        error("Unexpected end of input, expected a piece after factor")
    node, position = parse_piece(tokens, position)
    while position < len(tokens) and tokens[position]["token"] == "/":
        operator = tokens[position]
        right, position = parse_piece(tokens, position + 1)
        node = init_node(operator, [node, right])
    return node, position


def parse_piece(tokens, position):
    """Parse a piece: element { * element }"""
    if position >= len(tokens):
        error("Unexpected end of input, expected an element after piece")
    node, position = parse_element(tokens, position)
    while position < len(tokens) and tokens[position]["token"] == "*":
        operator = tokens[position]
        right, position = parse_element(tokens, position + 1)
        node = init_node(operator, [node, right])
    return node, position


def parse_element(tokens, position):
    """Parse an element: ( expression ) | NUMBER | IDENTIFIER"""
    if position >= len(tokens):
        error("Unexpected end of input, expected a NUMBER, IDENTIFIER, or '('")

    if tokens[position]["token"] == "(":
        node, position = parse_expression(tokens, position + 1)
        if position >= len(tokens):
            error("Unexpected end of input, missing closing parenthesis")
        elif tokens[position]["token"] == ")":
            return node, position + 1
    elif tokens[position]["tokenType"] == TokenType.NUM.value:
        node = init_node(tokens[position], [], "terminal")
        return node, position + 1
    elif tokens[position]["tokenType"] == TokenType.ID.value:
        node = init_node(tokens[position], [], "terminal")
        return node, position + 1
    else:
        error(
            f'Unexpected token "{tokens[position]["token"]}", while expected a NUMBER, IDENTIFIER, or "("'
        )


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


def test_driver(input_file, output_file):
    global line_currently_parsed
    global line_num_currently_parsed
    tokenized_lines = scan_file_to_tokenized_lines(input_file)
    with open(output_file, "w") as file_to_write:
        for tokenized_line in tokenized_lines:
            line_currently_parsed = tokenized_line["line"]
            line_num_currently_parsed = tokenized_line["line_number"]
            ast, position = parse_expression(tokenized_line["tokens"], 0)

            if position < len(tokenized_line["tokens"]):
                unexpected_token = tokenized_line["tokens"][position]["token"]
                error(f'Unexpected token "{unexpected_token}" at the end of expression')

            file_to_write.write(
                f'Line {line_num_currently_parsed} "{line_currently_parsed}":\n'
            )
            write_ast(ast, file_to_write)

    # all_tokens = []
    # for line in tokenized_lines:
    #     all_tokens.extend(line["tokens"])

    # print(all_tokens)

    # with open(output_file, "w") as file_to_write:
    #     ast, position = parse_statement(all_tokens, 0)

    #     if position < len(all_tokens):
    #         unexpected_token = all_tokens[position]["token"]
    #         error(f'Unexpected token "{unexpected_token}" at the end of input')

    #     write_ast(ast, file_to_write)


def error(message):
    with open(output_file, "w") as file_to_write:
        file_to_write.write(f"Parsing Error: {message}\n")
        file_to_write.write(
            f'in the line #{line_num_currently_parsed}: "{line_currently_parsed}"\n'
        )
    sys.exit(1)


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
            f'{print(f"{args.arguments}")} ERROR: the input format has to be "python3 parser.py <input_file_title> <output_file_title>" or "python3 parser.py <input_file_title>" .\n Instead {len(args.arguments)} arguments was passed.'
        )


if __name__ == "__main__":
    main()
