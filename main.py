import sys
from keywords import KEYWORDS


def error(msg):
    raise Exception(f"Clav Error: {msg}")


def handle_input(words, indent):
    if len(words) < 2:
        error("input lene ke liye variable ka naam chahiye bhai, kuch naam to de phle")

    return (
    f"{indent}val = input()\n"
    f"{indent}try:\n"
    f"{indent}    {words[1]} = int(val)\n"
    f"{indent}except:\n"
    f"{indent}    {words[1]} = val"
    )


def handle_print(words, indent):
    if len(words) < 2:
        error("kya print kru? variable ka naam to de")

    content = " ".join(words[1:])
    return f"{indent}print({content})"

def translate_code(code_lines):
    translated_lines = []

    prev_indent = 0
    last_was_block = False
    last_was_if = False
    for line in code_lines:
        # Preserve indentation
        indent_size = len(line) - len(line.lstrip())
        indent = line[:indent_size]

        stripped_line = line.strip()
        words = stripped_line.split()

        # Empty line
        if not words:
            translated_lines.append("")
            continue

        command = words[0].replace(":", "")
        if indent_size > prev_indent and not last_was_block:
            error("galat indentation hai 🫵  😂")

        prev_indent = indent_size
        last_was_block = False


        if "=" in stripped_line:
            parts = stripped_line.split("=", 1)

            if len(parts) != 2:
                error("assignment galat hai bhai")

            var = parts[0].strip()
            value = parts[1].strip()

            if not var.isidentifier():
                error(f"'{var}' valid variable name nahi hai")

            translated_lines.append(f"{indent}{var} = {value}")
            continue

        if command not in KEYWORDS:
            error(f"'{command}' inavalid keyword, check krle yr please🙏")

        # Input
        if command == "puch":
            translated_lines.append(handle_input(words, indent))
            continue

        # Print
        if command == "dikha":
            translated_lines.append(handle_print(words, indent))
            continue
        
        # If
        if KEYWORDS.get(command) == "if":
            if not stripped_line.endswith(":"):
                error("'agar' ke baad ':' lagana bhool gya, agli bar ni btauga😟")

            condition = stripped_line[len(command):].strip()
            translated_lines.append(f"{indent}if {condition}")

            last_was_block = True
            last_was_if = True
            continue
        
        # Else
        if KEYWORDS.get(command) == "else":
            if not stripped_line.endswith(":"):
                error("'warna' ke baad ':' lagana bhool gya, agli bar ni btauga😟")
            
            if not last_was_if:
                error("'warna' bina 'agar' ke use ni hota yr🙎")
            
            translated_lines.append(f"{indent}else:")

            last_was_block = True
            last_was_if = False
            continue
        
        # while
        if KEYWORDS.get(command) == "while":
            if not stripped_line.endswith(":"):
                error("jabtak ke baad ':' lagana bhool gya, agli bar ni btauga😟")
            
            condition = stripped_line[len(command):].strip()
            translated_lines.append(f"{indent}while {condition}")

            last_was_block = True
            continue

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