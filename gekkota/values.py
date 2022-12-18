from __future__ import annotations
from collections.abc import Iterable

from typing import Generic, Optional, Sequence, Union
from typing_extensions import TypeVar

from gekkota.core import Renderable

from .args import CallArg, FuncArg
from .constants import Config, StrGen, op_priorities
from .expression import Expression
from .utils import Utils


class Name(Expression, FuncArg):
    def __init__(self, name: str, annotation: Optional[Expression] = None):
        self.name = name
        self.annotation = annotation

    def render(self, config: Config) -> StrGen:
        yield self.name
        if self.annotation:
            yield ":"
            yield " "
            yield from self.annotation.render(config)


LiteralValue = Union[int, float, complex, str, bytes, bool, None]


class Literal(Expression):
    priority = 15

    def __init__(self, value: LiteralValue):
        self.value = value
        if isinstance(value, (str, bytes)):
            self.priority = 100

    def render(self, config: Config) -> StrGen:
        yield repr(self.value)


class FormatSpec(Expression):
    def __init__(self, expression: Expression, spec: str | Sequence[FStringPart]):
        self.expression = expression
        self.spec = spec

    def render(self, config: Config) -> StrGen:
        return self.expression.render(config)


class FString(Expression):
    def __init__(self, parts: Sequence[FStringPart] = ()):
        self.expression = make_fstring(parts)

    def render(self, config: Config) -> StrGen:
        return self.expression.render(config)


FStringPart = Union[str, Expression, FormatSpec]


def get_expressions(parts: Sequence[FStringPart]) -> Iterable[Expression]:
    for part in parts:
        if isinstance(part, Expression):
            yield part
        if isinstance(part, FormatSpec):
            spec = part.spec
            if not isinstance(spec, str):
                yield from get_expressions(spec)


def make_fstring(
    parts: Sequence[FStringPart] = (),
) -> Literal | CallExpr[GetAttr[Literal]]:
    if not parts:
        return Literal("")

    expression_parts: list[Expression | FormatSpec] = list(get_expressions(parts))
    nonexpression_parts: list[str] = []

    for part in parts:
        if isinstance(part, str):
            nonexpression_parts.append(part)

    if not expression_parts:
        return Literal("".join(nonexpression_parts))

    def render_part(part: FStringPart) -> StrGen:
        if isinstance(part, str):
            yield repr(part)[1:-1].replace("{", "{{").replace("}", "}}")
            return

        yield "{"

        if isinstance(part, FormatSpec):
            yield ":"

            if isinstance(part.spec, str):
                yield part.spec

            else:
                for subpart in part.spec:
                    yield from render_part(subpart)

        yield "}"

    def render_parts() -> StrGen:
        for part in parts:
            yield from render_part(part)

    return Literal("".join(render_parts())).getattr("format")(*expression_parts)


T = TypeVar("T", default=Expression, bound=Expression)


class Indexing(Expression, Generic[T]):
    priority = op_priorities["getitem"]

    def __init__(self, expression: T, index: Expression | SliceExpr):
        self.expression = expression.respect_priority(self, side="left")
        self.index_ = index

    def render(self, config: Config) -> StrGen:
        yield from self.expression.render(config)
        yield "["
        yield from self.index_.render(config)
        yield "]"


class SliceExpr(Renderable):
    def __init__(
        self,
        start: Optional[Expression] = None,
        stop: Optional[Expression] = None,
        step: Optional[Expression] = None,
    ):
        self.start = start
        self.stop = stop
        self.step = step

    def render(self, config: Config) -> StrGen:
        if self.start:
            yield from self.start.render(config)

        yield ":"

        if self.stop:
            yield from self.stop.render(config)

        if self.step:
            yield ":"
            yield from self.step.render(config)


class CallExpr(Expression, Generic[T]):
    priority = op_priorities["call"]

    def __init__(self, callee: T, args: Sequence[CallArg | Expression]):
        self.callee = callee.respect_priority(self, side="left")
        self.args = args

    def render(self, config: Config) -> StrGen:
        yield from self.callee.render(config)
        yield "("
        yield from Utils.comma_separated(self.args, config)
        yield ")"


class GetAttr(Expression, Generic[T]):
    priority = op_priorities["."]

    def __init__(self, value: T, *attributes: str):
        self.value = value.respect_priority(self, side="left")
        self.attributes = attributes

    def render(self, config: Config) -> StrGen:
        yield from self.value.render(config)
        yield "."
        yield from Utils.separated_str(".", self.attributes, config)

    def getattr(self, other: str) -> GetAttr[T]:
        return GetAttr(self.value, *self.attributes, other)
