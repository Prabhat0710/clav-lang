from tokens import TokenType
from nodes import (
    NumberNode, StringNode, IdentifierNode,
    AssignNode, BinaryOpNode, PrintNode, InputNode,
    IfNode, WhileNode, BreakNode, ContinueNode, ProgramNode
)
from keywords import KEYWORDS

CMD = {v: k for k, v in KEYWORDS.items()}

class Parser:
    def __init__(self, tokens):
        self.tokens  = tokens
        self.pos     = 0

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def peek(self):
        next_pos = self.pos + 1
        if next_pos < len(self.tokens):
            return self.tokens[next_pos]
        return None

    def expect(self, token_type):
        token = self.current()
        if token.type != token_type:
            raise Exception(
                f"Clav Error (Line {token.line_no}): "
                f"expected {token_type} but mila {token.type} ({token.value})"
            )
        return self.advance()

    def skip_newlines(self):
        while self.current().type == TokenType.NEWLINE:
            self.advance()

    def get_indent_level(self):
        if self.current().type == TokenType.INDENT:
            return len(self.current().value)
        return 0

    def parse_primary(self):
        token = self.current()

        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)

        if token.type == TokenType.STRING:
            self.advance()
            return StringNode(token.value)

        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return IdentifierNode(token.value)

        raise Exception(
            f"Clav Error (Line {token.line_no}): "
            f"'{token.value}' samajh nahi aaya bhai"
        )

    def parse_expression(self):
        left = self.parse_primary()

        # check if next token is an operator
        if self.current().type == TokenType.OPERATOR:
            operator = self.advance().value
            right    = self.parse_primary()
            return BinaryOpNode(left, operator, right)

        return left

    def parse_print(self):
        line_no = self.current().line_no
        self.advance()  # skip dikha

        # dikha can take multiple comma separated values
        values = []
        values.append(self.parse_expression())

        while self.current().type == TokenType.COMMA:
            self.advance()  # skip comma
            values.append(self.parse_expression())

        return PrintNode(values)

    def parse_input(self):
        self.advance()  # skip puch
        token = self.expect(TokenType.IDENTIFIER)
        return InputNode(token.value)

    def parse_assignment(self, identifier_token):
        self.advance()  # skip =
        value = self.parse_expression()
        return AssignNode(identifier_token.value, value)

    def parse_block(self, parent_indent):
        statements = []
        expected_indent = parent_indent + 4

        while self.current().type != TokenType.EOF:
            self.skip_newlines()

            if self.current().type == TokenType.EOF:
                break

            current_indent = self.get_indent_level()

            # block ended
            if current_indent <= parent_indent:
                break

            if current_indent != expected_indent:
                raise Exception(
                    f"Clav Error (Line {self.current().line_no}): "
                    f"indentation galat hai bhai"
                )

            if self.current().type == TokenType.INDENT:
                self.advance()  # skip indent token

            stmt = self.parse_statement(expected_indent)
            if stmt:
                statements.append(stmt)

        return statements

    def parse_if(self, indent_level):
        self.advance()  # skip agar
        condition = self.parse_expression()
        self.expect(TokenType.COLON)

        body       = self.parse_block(indent_level)
        elif_cases = []
        else_body  = None

        # check for agarnahi
        while True:
            self.skip_newlines()
            current_indent = self.get_indent_level()

            if current_indent != indent_level:
                break

            if self.current().type == TokenType.INDENT:
                self.advance()

            if (self.current().type == TokenType.KEYWORD and
                    self.current().value == CMD["elif"]):
                self.advance()  # skip agarnahi
                elif_condition = self.parse_expression()
                self.expect(TokenType.COLON)
                elif_body = self.parse_block(indent_level)
                elif_cases.append((elif_condition, elif_body))

            elif (self.current().type == TokenType.KEYWORD and
                    self.current().value == CMD["else"]):
                self.advance()  # skip warna
                self.expect(TokenType.COLON)
                else_body = self.parse_block(indent_level)
                break

            else:
                break

        return IfNode(condition, body, elif_cases, else_body)

    def parse_while(self, indent_level):
        self.advance()  # skip jabtak
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        body = self.parse_block(indent_level)
        return WhileNode(condition, body)

    def parse_statement(self, indent_level=0):
        self.skip_newlines()
        token = self.current()

        if token.type == TokenType.EOF:
            return None

        # keyword statements
        if token.type == TokenType.KEYWORD:
            if token.value == CMD["print"]:
                return self.parse_print()

            if token.value == CMD["input"]:
                return self.parse_input()

            if token.value == CMD["if"]:
                return self.parse_if(indent_level)

            if token.value == CMD["while"]:
                return self.parse_while(indent_level)

            if token.value == CMD["break"]:
                self.advance()
                return BreakNode()

            if token.value == CMD["continue"]:
                self.advance()
                return ContinueNode()

        # assignment: x = 5
        if token.type == TokenType.IDENTIFIER:
            if self.peek() and self.peek().type == TokenType.ASSIGN:
                identifier_token = self.advance()  # grab identifier
                return self.parse_assignment(identifier_token)

            # standalone identifier expression
            return IdentifierNode(self.advance().value)

        raise Exception(
            f"Clav Error (Line {token.line_no}): "
            f"'{token.value}' yahan expect nahi tha bhai"
        )

    def parse(self):
        statements = []
        self.skip_newlines()

        while self.current().type != TokenType.EOF:
            if self.current().type == TokenType.INDENT:
                self.advance()

            stmt = self.parse_statement(0)
            if stmt:
                statements.append(stmt)

            self.skip_newlines()

        return ProgramNode(statements)