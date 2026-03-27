import sys
from keywords import KEYWORDS


def translate_code(code_lines):
    translated_lines = []

    for line in code_lines:
        stripped_line = line.rstrip()
        words = stripped_line.split()

        # Handle empty lines
        if not words:
            translated_lines.append("")
            continue

        # Handle input
        if words[0] == "puch":
            if len(words) < 2:
                raise Exception("Syntax Error: variable ka naam miss h bro, Dhyan kidr h")

            var_name = words[1]
            translated_lines.append(f"{var_name} = input()")
            continue

        # Handle print
        if words[0] == "dikha":
            content = " ".join(words[1:])
            translated_lines.append(f"print({content})")
            continue

        if not stripped_line:
            translated_lines.append("")
            continue

        for clav_key, py_key in KEYWORDS.items():
            words = stripped_line.split()
            words = [py_key if word == clav_key else word for word in words]
            stripped_line = " ".join(words)

        translated_lines.append(stripped_line)

    return "\n".join(translated_lines)


def run_file(file_path):
    try:
        with open(file_path, "r") as file:
            code_lines = file.readlines()

        translated_code = translate_code(code_lines)

        print("\n--- Translated Python Code ---\n")
        print(translated_code)
        print("\n--- Output ---\n")

        exec(translated_code)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' nhi milri bro.")
    except Exception as e:
        print(f"Execution Error: {e} bhai")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <file.clav>")
    else:
        run_file(sys.argv[1])