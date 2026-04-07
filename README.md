# Clav Lang 🇮🇳

Clav is a Hindi-flavored programming language built from scratch in Python — with its own **Lexer**, **Parser**, and **Tree-walking Interpreter**. No `exec()`, no translation tricks. Real execution.

Error messages are in Hindi. With trolling. And emojis. 😂

---

## 🧱 Architecture

```
source.clav
     ↓
   Lexer        →  breaks code into tokens
     ↓
  Parser        →  builds an AST (Abstract Syntax Tree)
     ↓
Interpreter     →  walks the tree and executes it
```

---

## 📁 Project Structure

```
clav-lang/
├── main.py           → entry point
├── lexer.py          → tokenizer
├── parser.py         → builds AST from tokens
├── interpreter.py    → executes the AST
├── nodes.py          → AST node definitions
├── tokens.py         → token type definitions
├── keywords.py       → clav → python keyword mapping
└── examples/         → example .clav programs
```

---

## 🔑 Keywords

| Clav | Meaning |
|------|---------|
| `dikha` | print |
| `puch` | input |
| `agar` | if |
| `agarnahi` | elif |
| `warna` | else |
| `jabtak` | while |
| `ruk` | break |
| `chlo` | continue |
| `sach` | True |
| `jhoot` | False |

---

## ✍️ Syntax Examples

**Variables & Print**
```
x = 10
dikha x
dikha "hello"
```

**Input**
```
puch naam
dikha naam
```

**If / Elif / Else**
```
agar x > 10:
    dikha "bada hai"
agarnahi x == 10:
    dikha "barabar hai"
warna:
    dikha "chhota hai"
```

**While Loop**
```
x = 1
jabtak x < 6:
    dikha x
    x = x + 1
```

**Break & Continue**
```
x = 1
jabtak x < 10:
    agar x == 5:
        ruk
    dikha x
    x = x + 1
```

**Arithmetic**
```
a = 10
b = 3
dikha a + b
dikha a - b
dikha a * b
dikha a / b
```

---

## 🚀 How to Run

```bash
python main.py examples/yourfile.clav
```

---

## ❌ Error Messages

Errors are in Hindi with trolling because why not 😂

```
Clav Error (Line 2): 'much' kaunsa keyword hai bhai? 🤔 spelling check kr
Clav Error (Line 4): 'agar' ke baad ':' lagana bhool gaya? 😂
Clav Error: 'x' ko pehle banaya to hota bhai 😭
Clav Error: zero se divide?? 💀 maths ki class mein so raha tha kya?
```

---

## 🎓 Learning Outcomes

Building Clav from scratch taught the following concepts hands-on:

- **Lexical analysis** — how raw source text is scanned character by character and broken into meaningful tokens
- **Tokenization** — how to classify characters into types like keywords, identifiers, operators, strings, and numbers
- **Recursive descent parsing** — how to consume a flat list of tokens and build a structured AST using recursive function calls
- **AST design** — how every language construct (if, while, assignment, expression) maps to a specific node type in a tree
- **Tree-walking interpretation** — how to traverse an AST and execute each node without any code translation or `exec()`
- **Environment & scope** — how variables are stored, looked up, and managed during execution using a simple dictionary
- **Control flow** — how `if/elif/else`, `while`, `break`, and `continue` are implemented at the interpreter level using signals and recursion
- **Error handling** — how to produce meaningful, line-specific error messages at each stage of the pipeline

---

## ⚠️ Limitations

Clav is a learning project, not a production language. Current known limitations:

- **No functions** — cannot define or call functions
- **No for loops** — only `jabtak` (while) is supported
- **No lists or arrays** — only single values can be stored in variables
- **No string operations** — no concatenation, slicing, or string methods
- **No nested expressions** — only simple `left operator right` form works, so `(a + b) * c` will not work
- **No negative number literals** — write `0 - 5` instead of `-5`
- **Indentation must be exactly 4 spaces** — tabs or other spacing will cause errors
- **No multi-line expressions** — every expression must fit on one line
- **No type system** — variables have no declared types, everything is dynamic
- **Single file execution only** — no imports or multi-file programs

---

## 🧠 Why This Project?

Most people use programming languages without ever thinking about what happens inside. This project is about understanding that — how raw text becomes tokens, how tokens become a tree, and how that tree actually executes.

Built incrementally, committed cleanly, no shortcuts.