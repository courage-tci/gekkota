from __future__ import annotations
from typing import Sequence

from gekkota.args import StarArg

from .utils import Utils
from .values import Name
from .constants import Config, StrGen
from .core import Renderable, Statement


class ImportSource(Renderable):
    def __init__(self, parts: Sequence[str]):
        self.parts = parts

    def render(self, config: Config) -> StrGen:
        if self.parts:
            yield self.parts[0]
            for i in range(1, len(self.parts)):
                yield "."
                yield self.parts[i]


class ImportDots(ImportSource):
    def __init__(self, length: int = 1):
        self.length = length

    def render(self, config: Config) -> StrGen:
        for _ in range(self.length):
            yield "."


class ImportAlias(Renderable):
    def __init__(self, name: Name, alias: Name | None = None):
        self.name = name
        self.alias = alias

    def render(self, config: Config) -> StrGen:
        yield from self.name.render(config)
        if self.alias:
            yield " "
            yield "as"
            yield " "
            yield from self.alias.render(config)


class ImportStmt(Statement):
    def __init__(self, names: Sequence[ImportAlias | Name | StarArg[None]]):
        self.names = names

    def render(self, config: Config) -> StrGen:
        yield "import"
        yield " "
        yield from Utils.comma_separated(self.names, config)


class FromImportStmt(Statement):
    def __init__(
        self,
        source: ImportSource | Name,
        names: Sequence[ImportAlias | Name | StarArg[None]],
    ):
        self.source = source
        self.names = names

    def render(self, config: Config) -> StrGen:
        yield "from"
        yield " "
        yield from self.source.render(config)
        yield " "
        yield "import"
        yield " "
        yield from Utils.comma_separated(self.names, config)
