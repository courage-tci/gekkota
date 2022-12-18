from __future__ import annotations
from typing import Sequence, Union

from .small_stmt import PassStmt
from .utils import Utils
from .values import GetAttr, Literal, LiteralValue, Name
from .core import Renderable, Statement
from .constants import Config, StrGen
from .expression import Expression
from .block import Block, BlockStmt


class MatchStmt(BlockStmt):
    def __init__(self, value: Expression, cases: Sequence[CaseStmt]):
        self.body = Block(cases) if cases else PassStmt()
        self.value = value

    def render_head(self, config: Config) -> StrGen:
        yield "match"
        yield " "
        yield from self.value.render(config)


class CaseStmt(BlockStmt):
    def __init__(
        self, pattern: Pattern, body: Statement, guard: Expression | None = None
    ):
        self.pattern = pattern
        self.body = body
        self.guard = guard

    def render_head(self, config: Config) -> StrGen:
        yield "case"
        yield " "
        yield from self.pattern.render(config)
        if self.guard:
            yield " "
            yield "if"
            yield " "
            yield from self.guard.render(config)


class Pattern(Renderable):
    pass


class AsPattern(Pattern):
    def __init__(self, pattern: OrPattern | ClosedPattern, alias: CapturePattern):
        self.pattern = pattern
        self.alias = alias

    def render(self, config: Config) -> StrGen:
        yield from self.pattern.render(config)
        yield " "
        yield "as"
        yield " "
        yield from self.alias.render(config)


class OrPattern(Pattern):
    def __init__(self, alternatives: Sequence[ClosedPattern]):
        self.alternatives = alternatives
        assert alternatives, "OrPattern cannot be empty"

    def render(self, config: Config) -> StrGen:
        yield from Utils.separated(" | ", self.alternatives, config)

    def __or__(self, other: ClosedPattern | OrPattern) -> OrPattern:
        if isinstance(other, OrPattern):
            return OrPattern([*self.alternatives, *other.alternatives])
        return OrPattern([*self.alternatives, other])

    def as_(self, other: CapturePattern) -> AsPattern:
        return AsPattern(self, other)


class ClosedPattern(Pattern):
    def __or__(self, other: ClosedPattern | OrPattern) -> OrPattern:
        if isinstance(other, OrPattern):
            return OrPattern([self, *other.alternatives])
        return OrPattern([self, other])

    def as_(self, other: CapturePattern) -> AsPattern:
        return AsPattern(self, other)


PositionalPattern = Union[AsPattern, OrPattern, ClosedPattern]


class WildcardPattern(ClosedPattern):
    def render(self, config: Config) -> StrGen:
        yield "_"


class CapturePattern(ClosedPattern):
    def __init__(self, name: str):
        self.name = name

    def render(self, config: Config) -> StrGen:
        yield self.name

    def getattr(self, attr: str) -> ValuePattern:
        return ValuePattern(Name(self.name).getattr(attr))


class ValuePattern(ClosedPattern):
    def __init__(self, name: GetAttr[Name]):
        self.name = name

    def render(self, config: Config) -> StrGen:
        yield from self.name.render(config)

    def getattr(self, attr: str) -> ValuePattern:
        return ValuePattern(self.name.getattr(attr))


class LiteralPattern(ClosedPattern):
    def __init__(self, value: LiteralValue):
        self.value = value

    def render(self, config: Config) -> StrGen:
        return Literal(self.value).render(config)


class StarPattern(Renderable):
    def __init__(self, pattern: CapturePattern | WildcardPattern):
        self.pattern = pattern

    def render(self, config: Config) -> StrGen:
        yield "*"
        yield from self.pattern.render_str(config)


class OpenSequencePattern(Pattern):
    def __init__(self, elements: Sequence[StarPattern | PositionalPattern]):
        self.elements = elements
        assert elements, "OpenSequencePattern cannot be empty"

    def render(self, config: Config) -> StrGen:
        yield from Utils.comma_separated(self.elements, config)
        yield ","


class SequencePattern(ClosedPattern):
    def __init__(self, elements: Sequence[StarPattern | PositionalPattern]):
        self.pattern = OpenSequencePattern(elements)

    def render(self, config: Config) -> StrGen:
        yield from Utils.wrap("[]", self.pattern.render(config))


class KeywordPattern(Renderable):
    def __init__(self, name: str, pattern: PositionalPattern):
        self.name = name
        self.pattern = pattern

    def render(self, config: Config) -> StrGen:
        yield self.name
        yield "="
        yield from self.pattern.render(config)


class ClassPattern(ClosedPattern):
    def __init__(
        self,
        classname: Name | GetAttr[Name],
        positional_args: Sequence[PositionalPattern] = (),
        keyword_args: Sequence[KeywordPattern] = (),
    ):
        self.classname = classname
        self.positional_args = positional_args
        self.keyword_args = keyword_args

    def render(self, config: Config) -> StrGen:
        yield from self.classname.render(config)
        yield "("

        if self.positional_args:
            yield from Utils.comma_separated(self.positional_args, config)
            if self.keyword_args:
                yield ","
                yield " "
        if self.keyword_args:
            yield from Utils.comma_separated(self.keyword_args, config)

        yield ")"


class DoubleStarPattern(Renderable):
    def __init__(self, pattern: CapturePattern):
        self.pattern = pattern

    def render(self, config: Config) -> StrGen:
        yield "**"
        yield from self.pattern.render_str(config)


class KeyValuePattern(Renderable):
    def __init__(self, key: LiteralPattern | ValuePattern, value: PositionalPattern):
        self.key = key
        self.value = value

    def render(self, config: Config) -> StrGen:
        yield from self.key.render(config)
        yield ":"
        yield " "
        yield from self.value.render(config)


class MappingPattern(ClosedPattern):
    def __init__(self, items: Sequence[KeyValuePattern | DoubleStarPattern]):
        self.items = items

    def render(self, config: Config) -> StrGen:
        return Utils.wrap("{}", Utils.comma_separated(self.items, config))


class GroupPattern(ClosedPattern):
    def __init__(self, pattern: PositionalPattern):
        self.pattern = pattern

    def render(self, config: Config) -> StrGen:
        yield from Utils.wrap("()", self.pattern.render(config))
