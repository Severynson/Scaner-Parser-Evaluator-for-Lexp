import re
from enum import Enum
import os
import argparse

identifierRegex = r"[a-zA-Z][a-zA-Z0-9]*"
numberRegex = r"[0-9]+"
symbolRegex = r"\+|\-|\*|/|\(|\)"


class TokenType(Enum):
    ID = "identifier"
    NUM = "number"
    SYM = "symbol"
    ERR = "error"
    SPACE = "space"


def get_token_type(token):
    if re.fullmatch(identifierRegex, token):
        return TokenType.ID.value
    elif re.fullmatch(numberRegex, token):
        return TokenType.NUM.value
    elif re.fullmatch(symbolRegex, token):
        return TokenType.SYM.value
    elif re.fullmatch(" ", token):
        return TokenType.SPACE.value
    else:
        return TokenType.ERR.value


initTokenDict = lambda char: {"token": f"{char}", "tokenType": get_token_type(char)}

initTokenizedLineDict = lambda title, tokens: {
    "line": title,
    "tokens": tokens,
}


def scan_line(inputString=""):
    if inputString == "":
        return
    tokens = [initTokenDict(inputString[0].strip())]
    index = 1
    while index < len(inputString):
        previous_char = inputString[index - 1]
        if get_token_type(previous_char) == TokenType.ERR.value:
            break

        current_type = tokens[-1]["tokenType"]

        char = inputString[index]
        char_type = get_token_type(char)

        potential_update = f"{tokens[-1]["token"]}{char}"
        potential_update_type = get_token_type(potential_update)

        if current_type == potential_update_type:
            tokens[-1]["token"] = potential_update
        elif char_type != TokenType.SPACE.value:
            tokens.append(initTokenDict(inputString[index]))

        index += 1

    return tokens


def scaner(string_to_tokenize):
    lines_to_tokenize = string_to_tokenize.split("\n")
    tokenized_lines = []
    for line in lines_to_tokenize:
        line = line.lstrip()
        tokens = scan_line(line)
        tokenized_lines.append(initTokenizedLineDict(line, tokens))
    return tokenized_lines


def input_and_output(input_file, output_file):
    with open(input_file, "r") as file:
        file_content = file.read()
    tokenized_file_lines = scaner(file_content)

    with open(output_file, "w") as file_to_write:
        for line in tokenized_file_lines:
            if line["tokens"] != None:
                file_to_write.write(f"Line: {line["line"]}\n")
                for token in line["tokens"]:
                    if token["tokenType"] == TokenType.ERR.value:
                        file_to_write.write(f'ERROR READING "{token["token"]}"\n')
                    else:
                        file_to_write.write(
                            f"{token["token"]} : {f"{token["tokenType"]}".upper()}\n"
                        )
            file_to_write.write("\n")


def main():
    parser = argparse.ArgumentParser(description="parse based on the type of arguments")
    parser.add_argument("arguments", nargs="+", help="Runtime arguments")
    args = parser.parse_args()

    if len(args.arguments) == 2 and os.path.exists(args.arguments[0]):
        input_and_output(args.arguments[0], args.arguments[1])
    else:
        string_to_tokenize = " ".join(args.arguments)
        tokenized_lines = scaner(string_to_tokenize)
        for line in tokenized_lines:
            print(f"Line: {line["line"]}")
            for token in line["tokens"]:
                if token["tokenType"] == TokenType.ERR.value:
                    print(f'ERROR READING "{token["token"]}"')
                else:
                    print(f"{token["token"]} : {f"{token["tokenType"]}".upper()}")
            print("")


if __name__ == "__main__":
    main()
