from __future__ import annotations
from typing import Sequence

from .expression import Expression
from .constants import Config, StrGen
from .values import Name
from .block import BlockStmt
from .core import Statement
from .sequences import TupleExpr


class TryStmt(BlockStmt):
    def __init__(self, body: Statement):
        self.body = body

    def render_head(self, config: Config):
        yield "try"


class ExceptStmt(BlockStmt):
    def __init__(
        self,
        exceptions: Sequence[Expression] | None,
        alias: Name | None,
        body: Statement,
    ):
        self.exceptions = exceptions
        self.alias = alias
        self.body = body

    def render_head(self, config: Config) -> StrGen:
        yield "except"
        if self.exceptions:
            yield " "

            if len(self.exceptions) > 1:
                yield from TupleExpr(self.exceptions).render(config)
            else:
                yield from self.exceptions[0].render(config)

            if self.alias:
                yield " "
                yield "as"
                yield " "
                yield from self.alias.render(config)


class FinallyStmt(BlockStmt):
    def __init__(self, body: Statement):
        self.body = body

    def render_head(self, config: Config) -> StrGen:
        yield "finally"


class RaiseStmt(Statement):
    def __init__(
        self, exception: Expression | None = None, scope: Expression | None = None
    ):
        self.exception = exception
        self.scope = scope

    def render(self, config: Config) -> StrGen:
        yield "raise"
        if self.exception:
            yield " "
            yield from self.exception.render(config)
            if self.scope:
                yield " "
                yield "from"
                yield " "
                yield from self.scope.render(config)
