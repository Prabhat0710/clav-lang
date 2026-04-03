from tokens import Token, TokenType
from keywords import KEYWORDS

class Lexer:
    def __init__(self, source):
        self.source  = source        # entire source code as string
        self.pos     = 0             # current character position
        self.line_no = 1             # current line number
        self.tokens  = []            # final list of tokens

    def current_char(self):
        if self.pos < len(self.source):
            return self.source[self.pos]
        return None                  # means we reached end of file

    def advance(self):
        if self.current_char() == "\n":
            self.line_no += 1
        self.pos += 1

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.source):
            return self.source[peek_pos]
        return None

    def read_number(self):
        result = ""
        is_float = False

        while self.current_char() is not None and (self.current_char().isdigit() or self.current_char() == "."):
            if self.current_char() == ".":
                is_float = True
            result += self.current_char()
            self.advance()

        value = float(result) if is_float else int(result)
        return Token(TokenType.NUMBER, value, self.line_no)

    def read_string(self):
        self.advance()               # skip opening "
        result = ""

        while self.current_char() is not None and self.current_char() != '"':
            result += self.current_char()
            self.advance()

        self.advance()               # skip closing "
        return Token(TokenType.STRING, result, self.line_no)

    def read_word(self):
        result = ""

        while self.current_char() is not None and (self.current_char().isalnum() or self.current_char() == "_"):
            result += self.current_char()
            self.advance()

        # is it a keyword or a variable name?
        if result in KEYWORDS:
            return Token(TokenType.KEYWORD, result, self.line_no)
        else:
            return Token(TokenType.IDENTIFIER, result, self.line_no)

    def read_operator(self):
        ch = self.current_char()

        # two character operators: ==, !=, >=, <=
        if self.peek() == "=":
            if ch in "=!<>":
                op = ch + "="
                self.advance()
                self.advance()
                return Token(TokenType.OPERATOR, op, self.line_no)

        # single = is assignment not operator
        if ch == "=":
            self.advance()
            return Token(TokenType.ASSIGN, "=", self.line_no)

        # single character operators: +, -, *, /, >, 
        self.advance()
        return Token(TokenType.OPERATOR, ch, self.line_no)

    def read_indent(self):
        result = ""
        while self.current_char() == " ":
            result += " "
            self.advance()
        return Token(TokenType.INDENT, result, self.line_no)

    def tokenize(self):
        while self.current_char() is not None:
            ch = self.current_char()

            # indentation — only at start of line
            if ch == " " and (len(self.tokens) == 0 or self.tokens[-1].type == TokenType.NEWLINE):
                self.tokens.append(self.read_indent())

            # skip other spaces
            elif ch == " ":
                self.advance()

            # newline
            elif ch == "\n":
                self.tokens.append(Token(TokenType.NEWLINE, "\n", self.line_no))
                self.advance()

            # number
            elif ch.isdigit():
                self.tokens.append(self.read_number())

            # string
            elif ch == '"':
                self.tokens.append(self.read_string())

            # keyword or identifier
            elif ch.isalpha() or ch == "_":
                self.tokens.append(self.read_word())

            # colon
            elif ch == ":":
                self.tokens.append(Token(TokenType.COLON, ":", self.line_no))
                self.advance()

            # comma
            elif ch == ",":
                self.tokens.append(Token(TokenType.COMMA, ",", self.line_no))
                self.advance()

            # parentheses
            elif ch == "(":
                self.tokens.append(Token(TokenType.LPAREN, "(", self.line_no))
                self.advance()

            elif ch == ")":
                self.tokens.append(Token(TokenType.RPAREN, ")", self.line_no))
                self.advance()

            # operators and assignment
            elif ch in "=+-*/<>!":
                self.tokens.append(self.read_operator())

            # unknown character
            else:
                raise Exception(f"Clav Error (Line {self.line_no}): '{ch}' samajh nahi aaya bhai")

        self.tokens.append(Token(TokenType.EOF, None, self.line_no))
        return self.tokens
    
if __name__ == "__main__":
    code = """agar x > 5:
    dikha "yes"
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)