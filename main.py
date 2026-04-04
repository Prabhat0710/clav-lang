import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def run_file(file_path):
    try:
        with open(file_path, "r") as file:
            source = file.read()

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        tree = parser.parse()

        interpreter = Interpreter()
        interpreter.run(tree)

    except FileNotFoundError:
        print(f"Clav Error: file '{file_path}' nahi mili bhai")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <file.clav>")
    else:
        run_file(sys.argv[1])