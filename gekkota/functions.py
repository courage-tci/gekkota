from __future__ import annotations

from typing import Optional, Sequence
from .args import FuncArg
from .block import BlockStmt
from .constants import Config, StrGen
from .core import Statement
from .utils import Utils
from .expression import Expression


class LambDef(Expression):
    def __init__(self, args: Sequence[FuncArg], body: Expression):
        self.args = args
        self.body = body

    def render(self, config: Config) -> StrGen:
        yield "lambda"
        if self.args:
            yield " "
            yield from Utils.comma_separated(self.args, config)
        yield ":"
        yield " "
        yield from self.body.render(config)


class FuncDef(BlockStmt):
    spacing = 1

    def __init__(
        self,
        name: str,
        args: Sequence[FuncArg],
        body: Statement,
        *,
        rtype: Optional[Expression] = None,
        is_async: bool = False,
    ):
        self.name = name
        self.body = body
        self.args = args
        self.rtype = rtype
        self.is_async = is_async

    def render_head(self, config: Config) -> StrGen:
        if self.is_async:
            yield "async"
            yield " "
        yield "def"
        yield " "
        yield self.name
        yield "("
        yield from Utils.comma_separated(self.args, config)
        yield ")"

        if self.rtype:
            yield " "
            yield "->"
            yield " "
            yield from self.rtype.render(config)


class Decorated(Statement):
    def __init__(self, decorator: Expression, statement: ClassDef | FuncDef):
        self.decorator = decorator
        self.statement = statement

    def render(self, config: Config) -> StrGen:
        yield "@"
        yield from self.decorator.render(config)
        yield "\n"
        yield from self.statement.render(config)


from gekkota.classes import ClassDef
