from __future__ import annotations

from typing import Sequence

from gekkota.expression import Expression
from .block import BlockStmt
from .constants import Config, StrGen
from .core import Statement
from .args import CallArg
from .utils import Utils


class ClassDef(BlockStmt):
    spacing = 1

    def __init__(
        self, name: str, args: Sequence[CallArg | Expression], body: Statement
    ):
        self.name = name
        self.body = body
        self.args = args

    def render_head(self, config: Config) -> StrGen:
        yield "class"
        yield " "
        yield self.name
        if self.args:
            yield "("
            yield from Utils.comma_separated(self.args, config)
            yield ")"
