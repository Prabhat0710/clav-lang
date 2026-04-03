class TokenType:
    # Literals
    NUMBER      = "NUMBER"
    STRING      = "STRING"
    IDENTIFIER  = "IDENTIFIER"

    # Keywords
    KEYWORD     = "KEYWORD"

    # Operators
    OPERATOR    = "OPERATOR"
    ASSIGN      = "ASSIGN"        # =

    # Symbols
    COLON       = "COLON"         # :
    COMMA       = "COMMA"         # ,
    LPAREN      = "LPAREN"        # (
    RPAREN      = "RPAREN"        # )

    # Structure
    NEWLINE     = "NEWLINE"
    INDENT      = "INDENT"
    DEDENT      = "DEDENT"
    EOF         = "EOF"


class Token:
    def __init__(self, type, value, line_no):
        self.type    = type
        self.value   = value
        self.line_no = line_no

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line_no})"