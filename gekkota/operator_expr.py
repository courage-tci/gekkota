from gekkota.constants import Config, StrGen, op_priorities, op_associativities
from gekkota.expression import Expression


class BinaryExpr(Expression):
    def __init__(self, left: Expression, right: Expression, op: str):
        self.op = op
        self.priority = op_priorities[op]
        self.associativity = op_associativities.get(op, "both")
        self.left = left.respect_priority(self, side="left")
        self.right = right.respect_priority(self, side="right")

    def render(self, config: Config) -> StrGen:
        yield from self.left.render(config)
        yield " "
        yield self.op
        yield " "
        yield from self.right.render(config)


class UnaryExpr(Expression):
    def __init__(self, expression: Expression, op: str):
        self.op = op
        self.priority = op_priorities[f"u{op}"]
        self.expression = expression.respect_priority(self)

    def render(self, config: Config) -> StrGen:
        yield self.op
        yield from self.expression.render(config)


class AwaitExpr(Expression):
    priority = op_priorities["await"]

    def __init__(self, awaitable: Expression):
        self.awaitable = awaitable.respect_priority(self, side="right")

    def render(self, config: Config) -> StrGen:
        yield "await"
        yield " "
        yield from self.awaitable.render(config)
