import sys
from keywords import KEYWORDS

RESERVED_KEYWORDS = set(KEYWORDS.keys())

CMD = {v: k for k, v in KEYWORDS.items()}

def error(msg, line_no):
    raise Exception(f"Clav Error (Line {line_no}): {msg}")


def handle_input(words, indent, line_no):
    if len(words) < 2:
        error("input lene ke liye variable ka naam chahiye bhai, kuch naam to de phle", line_no)
    
    var_name = words[1]
    if var_name in RESERVED_KEYWORDS:
        error(f"'{var_name}' reserved keyword h dost, konse nashe kre h?", line_no)

    return (
        f"{indent}__clav_tmp = input()\n"
        f"{indent}try:\n"
        f"{indent}    {words[1]} = int(__clav_tmp)\n"
        f"{indent}except:\n"
        f"{indent}    try:\n"
        f"{indent}        {words[1]} = float(__clav_tmp)\n"
        f"{indent}    except:\n"
        f"{indent}        {words[1]} = __clav_tmp"
    )

def handle_print(words, indent, line_no):
    if len(words) < 2:
        error("kya print kru? variable ka naam to de", line_no)

    content = " ".join(words[1:])
    return f"{indent}print({content})"

def is_assignment(line):
    in_string = False

    for i, ch in enumerate(line):
        if ch == '"':
            in_string = not in_string

        # detect single '=' but NOT '==' and NOT inside string
        if ch == "=" and not in_string:
            if i + 1 < len(line) and line[i + 1] == "=":
                continue
            return True

    return False

def translate_code(code_lines):
    translated_lines = []

    indent_stack = [0]
    loop_stack = [0]

    last_was_block = False
    last_was_if = False
    for line_no, line in enumerate(code_lines, start=1):
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

        if indent_size > indent_stack[-1]:
            if not last_was_block:
                error("galat indentation hai 🫵 😂", line_no)
            indent_stack.append(indent_size)

        elif indent_size < indent_stack[-1]:
            while indent_stack and indent_size < indent_stack[-1]:
                indent_stack.pop()
            
            while loop_stack and indent_size <= loop_stack[-1]:
                loop_stack.pop()

            if indent_size != indent_stack[-1]:
                error("indentation mismatch hai", line_no)

        last_was_block = False

        # Assignment
        if is_assignment(stripped_line) and not stripped_line.strip().startswith("agar"):
            parts = stripped_line.split("=", 1)

            if len(parts) != 2:
                error("glt baat bro, ese assign krte h kya? check kr shi se", line_no)

            var = parts[0].strip()
            value = parts[1].strip()

            if var in RESERVED_KEYWORDS:
                error(f"'{var}' reserved keyword h dost, konse nashe kre h?", line_no)

            if not var.isidentifier():
                error(f"'{var}' valid variable name nahi hai", line_no)

            translated_lines.append(f"{indent}{var} = {value}")
            continue
        
        # Keyword check
        if command not in KEYWORDS:
            error(f"'{command}' inavalid keyword, check krle yr please🙏", line_no)

        # Input
        if command == CMD["input"]:
            translated_lines.append(handle_input(words, indent, line_no))
            continue

        # Print
        if command == CMD["print"]:
            translated_lines.append(handle_print(words, indent, line_no))
            continue
        
        # Elif
        if KEYWORDS.get(command) == "elif":
            if not stripped_line.endswith(":"):
                error("agarnahi ke baad ':' lagana bhool gaya kya?", line_no)

            if not last_was_if:
                error("agarnahi bina agar ke use nahi hota bhai", line_no)

            condition = stripped_line[len("agarnahi"):].strip()

            for clav_key, py_key in KEYWORDS.items():
                condition = condition.replace(clav_key, py_key)

            translated_lines.append(f"{indent}elif {condition}")

            last_was_block = True
            last_was_if = True
            continue
                
        # If
        if KEYWORDS.get(command) == "if":
            if not stripped_line.endswith(":"):
                error("'agar' ke baad ':' lagana bhool gya, agli bar ni btauga😟",line_no)

            condition = stripped_line[len(command):].strip()

            for clav_key, py_key in KEYWORDS.items():
                condition = condition.replace(clav_key, py_key)

            translated_lines.append(f"{indent}if {condition}")

            last_was_block = True
            last_was_if = True
            continue
        
        # Else
        if KEYWORDS.get(command) == "else":
            if not stripped_line.endswith(":"):
                error("'warna' ke baad ':' lagana bhool gya, agli bar ni btauga😟", line_no)
            
            if stripped_line.strip() != "warna:":
                error("warna ke saath condition nhi ati bro 😒", line_no)
            
            if not last_was_if:
                error("'warna' bina 'agar' ke use ni hota yr🙎", line_no)
            
            translated_lines.append(f"{indent}else:")

            last_was_block = True
            last_was_if = False
            continue
        
        # while
        if KEYWORDS.get(command) == "while":
            if not stripped_line.endswith(":"):
                error("jabtak ke baad ':' lagana bhool gya, agli bar ni btauga😟", line_no)
            
            condition = stripped_line[len(command):].strip()

            for clav_key, py_key in KEYWORDS.items():
                condition = condition.replace(clav_key, py_key)

            translated_lines.append(f"{indent}while {condition}")
            loop_stack.append(indent_size)

            last_was_block = True
            continue
        
        # Break
        if command == CMD["break"]:
            if not loop_stack:
                error("'ruk' sirf loop ke andr use hoga", line_no)

            translated_lines.append(f"{indent}break")
            continue

        # Continue
        if command == CMD["continue"]:
            if not loop_stack:
                error("'chlo' sirf loop ke andr use hoga", line_no)

            translated_lines.append(f"{indent}continue")
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