import sys
from keywords import KEYWORDS


def error(msg):
    raise Exception(f"Clav Error: {msg}")


def handle_input(words):
    if len(words) < 2:
        error("input lene ke liye variable ka naam chahiye bhai, kuch naam to de phle")

    var_name = words[1]
    return f"{var_name} = input()"


def handle_print(words):
    if len(words) < 2:
        error("kya print kru? variable ka naam to de")

    content = " ".join(words[1:])
    return f"print({content})"


def replace_keywords(line):
    for clav_key, py_key in KEYWORDS.items():
        if line.startswith(clav_key):
            return line.replace(clav_key, py_key, 1)
    return line


def translate_code(code_lines):
    translated_lines = []

    for line in code_lines:
        stripped_line = line.rstrip()
        words = stripped_line.split()

        # Empty line safe
        if not words:
            translated_lines.append("")
            continue

        command = words[0]
        valid_commands = ["dikha", "puch"] + list(KEYWORDS.keys())

        if command not in valid_commands:
            error(f"'{command}' arey kehna kya chahte ho? syntax check kr")

        # Input
        if command == "puch":
            translated_lines.append(handle_input(words))
            continue

        # Print
        if command == "dikha":
            translated_lines.append(handle_print(words))
            continue

        # Keyword replacement (if, while etc.)
        new_line = replace_keywords(stripped_line)

        # Unknown command detection
        if new_line == stripped_line and command not in KEYWORDS:
            error(f"'{command}' koi valid command nahi hai")

        translated_lines.append(new_line)

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
        print(f"Error: File '{file_path}' nahi milri bro.")
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <file.clav>")
    else:
        run_file(sys.argv[1])