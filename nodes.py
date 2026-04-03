class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"


class StringNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringNode({self.value})"


class IdentifierNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"IdentifierNode({self.name})"


class AssignNode:
    def __init__(self, name, value):
        self.name  = name     # variable name (string)
        self.value = value    # any node (NumberNode, StringNode etc.)

    def __repr__(self):
        return f"AssignNode({self.name} = {self.value})"


class BinaryOpNode:
    def __init__(self, left, operator, right):
        self.left     = left      # left side node
        self.operator = operator  # +, -, *, /, >, <, ==, !=, >=, <=
        self.right    = right     # right side node

    def __repr__(self):
        return f"BinaryOpNode({self.left} {self.operator} {self.right})"


class PrintNode:
    def __init__(self, value):
        self.value = value    # any node

    def __repr__(self):
        return f"PrintNode({self.value})"


class InputNode:
    def __init__(self, var_name):
        self.var_name = var_name   # variable name to store input in

    def __repr__(self):
        return f"InputNode({self.var_name})"


class IfNode:
    def __init__(self, condition, body, elif_cases, else_body):
        self.condition   = condition    # BinaryOpNode or IdentifierNode
        self.body        = body         # list of nodes
        self.elif_cases  = elif_cases   # list of (condition, body) tuples
        self.else_body   = else_body    # list of nodes or None

    def __repr__(self):
        return f"IfNode({self.condition})"


class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition    # BinaryOpNode
        self.body      = body         # list of nodes

    def __repr__(self):
        return f"WhileNode({self.condition})"


class BreakNode:
    def __repr__(self):
        return "BreakNode"


class ContinueNode:
    def __repr__(self):
        return "ContinueNode"


class ProgramNode:
    def __init__(self, statements):
        self.statements = statements   # list of all nodes

    def __repr__(self):
        return f"ProgramNode({self.statements})"