from __future__ import annotations
from typing import Sequence
from typing_extensions import Self

from .constants import StrGen, Config
from .core import Statement


class Expression(Statement):
    """expression, a type of statement with a return value"""

    priority = 100
    associativity = "both"

    def __or__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "|")

    def __and__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "&")

    def __xor__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "^")

    def __add__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "+")

    def __sub__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "-")

    def __mul__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "*")

    def __truediv__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "/")

    def __matmul__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "@")

    def __floordiv__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "//")

    def __mod__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "%")

    def __pow__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "**")

    def __rshift__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, ">>")

    def __lshift__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "<<")

    def eq(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "==")

    def neq(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "!=")

    def __gt__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, ">")

    def __ge__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, ">=")

    def __lt__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "<")

    def __le__(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "<=")

    def and_(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "and")

    def or_(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "or")

    def in_(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "in")

    def not_in(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "not in")

    def is_(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "is")

    def is_not(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, "is not")

    def assign(self, other: Expression) -> BinaryExpr:
        return BinaryExpr(self, other, ":=")

    def not_(self) -> UnaryExpr:
        return UnaryExpr(self, "not ")

    def __neg__(self) -> UnaryExpr:
        return UnaryExpr(self, "-")

    def __pos__(self) -> UnaryExpr:
        return UnaryExpr(self, "+")

    def __invert__(self) -> UnaryExpr:
        return UnaryExpr(self, "~")

    def __call__(
        self, *args: CallArg | Expression, **kwargs: Expression
    ) -> CallExpr[Self]:
        return CallExpr(self, [*args, *(CallArg(k, kwargs[k]) for k in kwargs)])

    def getattr(self, other: str) -> GetAttr[Self]:
        return GetAttr(self, other)

    def __getitem__(self, item):
        return self.index(item)

    def index(
        self, index: Expression | SliceExpr | Sequence[SliceExpr]
    ) -> Indexing[Self]:
        if isinstance(index, Sequence):
            index = SequenceExpr(
                [
                    x
                    if isinstance(x, SliceExpr)
                    else SliceExpr(
                        x.start, x.stop, x.step
                    )  # check explanation right below
                    for x in index
                ]
            )

        # Case of getting a slice instance is impossible with static typing (since `slice` is not in available types of index)
        # Omitting slice from index typing comes from the fact that slice can't be generic: https://github.com/python/typeshed/issues/8647
        # Nevertheless, using real slices in Indexing is incredibly convenient so I'd rather support that for folks who don't use type checking

        if isinstance(index, slice):  # type: ignore
            index = SliceExpr(index.start, index.stop, index.step)  # type: ignore

        return Indexing(self, index)

    def await_(self) -> AwaitExpr:
        return AwaitExpr(self)

    def if_(self, condition: Expression, else_branch: Expression) -> IfExpr:
        return IfExpr(true_branch=self, condition=condition, false_branch=else_branch)

    def respect_priority(self, op: Expression, side: str = "none") -> Expression:
        if self.priority < op.priority:
            return Parens(self)

        if self.priority == op.priority:
            if side == "none" or self.associativity == "both":
                return self
            if self.associativity != side:  # e.g "left" != "right" and vice versa
                return Parens(self)

        return self


class Parens(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression

    def render(self, config: Config) -> StrGen:
        yield "("
        yield from self.expression.render(config)
        yield ")"


from .operator_expr import AwaitExpr, BinaryExpr, UnaryExpr
from .control_flow import IfExpr
from .values import CallExpr, GetAttr, Indexing, SliceExpr
from .sequences import SequenceExpr
from .args import CallArg
