import re
from enum import Enum
import os
import argparse

state_line_of_the_error = True

identifierRegex = r"[a-zA-Z][a-zA-Z0-9]*"
numberRegex = r"[0-9]+"
symbolRegex = r"\+|\-|\*|/|\(|\)|:=|;"
keywordRegex = r"if|then|else|endif|while|do|endwhile|skip"


class TokenType(Enum):
    ID = "identifier"
    NUM = "number"
    SYM = "symbol"
    KEYWORD = "keyword"
    ERR = "error"
    SPACE = "space"


def get_token_type(token):
    if re.fullmatch(keywordRegex, token):
        return TokenType.KEYWORD.value
    elif re.fullmatch(numberRegex, token):
        return TokenType.NUM.value
    elif re.fullmatch(symbolRegex, token):
        return TokenType.SYM.value
    elif re.fullmatch(identifierRegex, token):
        return TokenType.ID.value
    elif re.fullmatch(" ", token):
        return TokenType.SPACE.value
    else:
        return TokenType.ERR.value


initTokenDict = lambda char: {"token": f"{char}", "tokenType": get_token_type(char)}

initTokenizedLineDict = lambda line_number, title, tokens: {
    "line_number": line_number,
    "line": title,
    "tokens": tokens,
}


# Do not call this method itself even for a single string, use scaner instead
def scan_line(inputString=""):
    tokens = [initTokenDict(inputString[0])]
    index = 1
    if tokens[-1]["tokenType"] != TokenType.ERR.value:
        while index < len(inputString):
            current_token = tokens[-1]["token"]
            current_token_type = tokens[-1]["tokenType"]

            char = inputString[index]
            char_type = get_token_type(char)

            potential_updated_token = f"{current_token}{char}"
            potential_updated_token_type = get_token_type(potential_updated_token)

            if char_type == TokenType.SPACE.value:
                while inputString[index] == TokenType.SPACE.value:
                    index += 1
                tokens.append(initTokenDict(char))
                index += 1

            elif potential_updated_token_type == TokenType.ERR.value:
                # Check if continue reading won't start to make sense
                # For example, while ":" is an error, ":=" is a symbol
                look_ahead_index = index + 1
                found_valid = False

                while look_ahead_index <= len(inputString):
                    potential_token = inputString[index:look_ahead_index]
                    if get_token_type(potential_token) != TokenType.ERR.value:
                        if char_type != TokenType.SPACE.value:
                            tokens.append(initTokenDict(potential_token))
                        index = look_ahead_index
                        found_valid = True
                        break
                    look_ahead_index += 1

                if not found_valid:
                    tokens.append(initTokenDict(char))
                    tokens[-1]["tokenType"] = TokenType.ERR.value
                    break

            elif (
                current_token_type == potential_updated_token_type
                or (
                    current_token_type == TokenType.ID.value
                    and potential_updated_token_type == TokenType.KEYWORD.value
                )
                or (
                    current_token_type == TokenType.KEYWORD.value
                    and potential_updated_token_type == TokenType.ID.value
                )
            ):
                tokens[-1] = initTokenDict(potential_updated_token)
                index += 1

    return [token for token in tokens if token["tokenType"] != TokenType.SPACE.value]


def scaner(string_to_tokenize):
    lines_to_tokenize = string_to_tokenize.split("\n")
    tokenized_lines = []
    for line_number, line in enumerate(lines_to_tokenize, start=1):
        if line and not line.isspace():
            tokens = scan_line(line.lstrip())
            tokenized_lines.append(initTokenizedLineDict(line_number, line, tokens))
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
                        file_to_write.write(
                            f'ERROR READING "{token["token"]}" {"(line " + str(line["line_number"]) + ")" if state_line_of_the_error else ""}\n'
                        )
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
        tokenized_lines = scaner(string_to_tokenize.lstrip())
        for line in tokenized_lines:
            print(f"Line: {line["line"]}")
            for token in line["tokens"]:
                if token["tokenType"] == TokenType.ERR.value:
                    print(
                        f'ERROR READING "{token["token"]}" {"(line " + str(line["line_number"]) + ")" if state_line_of_the_error else ""}\n'
                    )
                else:
                    print(f"{token["token"]} : {f"{token["tokenType"]}".upper()}")
            print("")


if __name__ == "__main__":
    main()
