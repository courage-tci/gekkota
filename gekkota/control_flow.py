from __future__ import annotations
from typing import Sequence

from gekkota.utils import Utils

from .expression import Expression
from .constants import Config, StrGen, op_priorities
from .core import Statement
from .block import BlockStmt


class IfExpr(Expression):
    priority = op_priorities["ternary"]

    def __init__(
        self, true_branch: Expression, condition: Expression, false_branch: Expression
    ):
        self.true_branch = true_branch
        self.condition = condition
        self.false_branch = false_branch

    def render(self, config: Config) -> StrGen:
        yield from self.true_branch.render(config)
        yield " "
        yield "if"
        yield " "
        yield from self.condition.render(config)
        yield " "
        yield "else"
        yield " "
        yield from self.false_branch.render(config)


class IfStmt(BlockStmt):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body

    def render_head(self, config: Config) -> StrGen:
        yield "if"
        yield " "
        yield from self.condition.render(config)


class ElifStmt(IfStmt):
    def render_head(self, config: Config) -> StrGen:
        yield "elif"
        yield " "
        yield from self.condition.render(config)


class ElseStmt(BlockStmt):
    def __init__(self, body: Statement):
        self.body = body

    def render_head(self, config: Config) -> StrGen:
        yield "else"


class WhileStmt(IfStmt):
    def render_head(self, config: Config):
        yield "while"
        yield " "
        yield from self.condition.render(config)


class ForStmt(BlockStmt):
    def __init__(
        self,
        target: Expression,
        iterator: Expression,
        body: Statement,
        *,
        is_async: bool = False,
    ):
        self.target = target
        self.iterator = iterator
        self.body = body
        self.is_async = is_async

    def render_head(self, config: Config) -> StrGen:
        if self.is_async:
            yield "async"
            yield " "
        yield "for"
        yield " "
        yield from self.target.render(config)
        yield " "
        yield "in"
        yield " "
        yield from self.iterator.render(config)


class WithTarget(Expression):
    def __init__(self, expression: Expression, alias: str | None = None):
        self.expression = expression
        self.alias = alias

    def render(self, config: Config) -> StrGen:
        yield from self.expression.render(config)
        if self.alias:
            yield " "
            yield "as"
            yield " "
            yield self.alias


class WithStmt(BlockStmt):
    def __init__(
        self,
        targets: Sequence[WithTarget | Expression],
        body: Statement,
        *,
        is_async: bool = False,
    ):
        self.targets = targets
        self.body = body
        self.is_async = is_async

    def render_head(self, config: Config) -> StrGen:
        if self.is_async:
            yield "async"
            yield " "
        yield "with"
        yield " "
        yield from Utils.comma_separated(self.targets, config)
