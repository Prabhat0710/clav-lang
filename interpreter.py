from nodes import (
    NumberNode, StringNode, IdentifierNode,
    AssignNode, BinaryOpNode, PrintNode, InputNode,
    IfNode, WhileNode, BreakNode, ContinueNode, ProgramNode
)

# signals to handle break and continue
class BreakSignal(Exception):
    pass

class ContinueSignal(Exception):
    pass


class Interpreter:
    def __init__(self):
        self.env = {}   # stores all variables

    # ─── entry point 

    def run(self, tree):
        return self.execute_block(tree.statements)

    # ─── block execution 

    def execute_block(self, statements):
        for stmt in statements:
            self.execute(stmt)

    # ─── node dispatcher

    def execute(self, node):
        if isinstance(node, AssignNode):
            return self.execute_assign(node)

        if isinstance(node, PrintNode):
            return self.execute_print(node)

        if isinstance(node, InputNode):
            return self.execute_input(node)

        if isinstance(node, IfNode):
            return self.execute_if(node)

        if isinstance(node, WhileNode):
            return self.execute_while(node)

        if isinstance(node, BreakNode):
            raise BreakSignal()

        if isinstance(node, ContinueNode):
            raise ContinueSignal()

        raise Exception(f"Clav Error: bhai ye '{type(node)}' node kahan se uthake le aaya? 😂")
    
    # ─── expression evaluator

    def evaluate(self, node):
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, StringNode):
            return node.value

        if isinstance(node, IdentifierNode):
            if node.name not in self.env:
                raise Exception(
                    f"Clav Error: '{node.name}' ko pehle banaya to hota bhai 😭 seedha use karne chala aaya, ghar mein ghusne se pehle darwaza khatkhatate hain 🚪"
                )
            return self.env[node.name]

        if isinstance(node, BinaryOpNode):
            left  = self.evaluate(node.left)
            right = self.evaluate(node.right)
            op    = node.operator

            if op == "+":  return left + right
            if op == "-":  return left - right
            if op == "*":  return left * right
            if op == "/":
                if right == 0:
                    raise Exception("Clav Error: zero se divide?? 💀 maths ki class mein sora tha kya? 😴 ye possible hi ni hai bhai 🤦")
                return left / right
            if op == ">":  return left > right
            if op == "<":  return left < right
            if op == "==": return left == right
            if op == "!=": return left != right
            if op == ">=": return left >= right
            if op == "<=": return left <= right

            raise Exception(f"Clav Error: '{op}' kaunsa operator hai bhai? 🧐 khud se operator banane laga hai kya? 😂 jo hai unhi se kaam chala")

        raise Exception(f"Clav Error: '{type(node)}' expression ka toh naam bhi nahi suna tha bhai 🤯 kahan se copy kiya ye? 😭")

    # ─── statement executors 

    def execute_assign(self, node):
        value = self.evaluate(node.value)
        self.env[node.name] = value

    def execute_print(self, node):
        values = [str(self.evaluate(v)) for v in node.value]
        print(" ".join(values))

    def execute_input(self, node):
        raw = input()
        try:
            self.env[node.var_name] = int(raw)
        except:
            try:
                self.env[node.var_name] = float(raw)
            except:
                self.env[node.var_name] = raw

    def execute_if(self, node):
        if self.evaluate(node.condition):
            self.execute_block(node.body)
            return

        for elif_condition, elif_body in node.elif_cases:
            if self.evaluate(elif_condition):
                self.execute_block(elif_body)
                return

        if node.else_body:
            self.execute_block(node.else_body)

    def execute_while(self, node):
        while self.evaluate(node.condition):
            try:
                self.execute_block(node.body)
            except BreakSignal:
                break
            except ContinueSignal:
                continue