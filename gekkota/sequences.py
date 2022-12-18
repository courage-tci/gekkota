from __future__ import annotations

from typing import Any, Generic, Sequence
from typing_extensions import Type, TypeVar


from .values import Name
from .core import Renderable
from .constants import Config, StrGen
from .expression import Expression
from .utils import Utils

T = TypeVar("T", default=Expression, bound=Renderable)


class SequenceExpr(Expression, Generic[T]):
    parens: tuple[str, str] = ("", "")

    def __init__(self, values: Sequence[T]):
        self.values = values

    def render_empty(self, config: Config) -> StrGen:
        yield from self.parens

    def render_one(self, config: Config) -> StrGen:
        yield from Utils.wrap(self.parens, self.values[0].render(config))

    def render(self, config: Config) -> StrGen:
        if not self.values:
            yield from self.render_empty(config)
            return
        if len(self.values) == 1:
            yield from self.render_one(config)
            return

        yield from Utils.wrap(self.parens, Utils.comma_separated(self.values, config))


class ListExpr(SequenceExpr):
    parens = ("[", "]")


class TupleExpr(SequenceExpr):
    parens = ("(", ")")

    def render_one(self, config: Config) -> StrGen:
        yield self.parens[0]
        yield from self.values[0].render(config)
        yield ","
        yield " "
        yield self.parens[1]


class SetExpr(SequenceExpr):
    parens = ("{", "}")

    def render_empty(self, config: Config) -> StrGen:
        yield from Name("set")().render(config)


class KeyValue(Expression):
    def __init__(self, key: Expression, value: Expression):
        self.key = key
        self.value = value

    def render(self, config: Config) -> StrGen:
        yield from self.key.render(config)
        yield ":"
        yield " "
        yield from self.value.render(config)


class DictExpr(SequenceExpr[KeyValue]):
    parens = ("{", "}")


S = TypeVar("S", bound=Type[SequenceExpr[Any]])


class Comprehension(Expression, Generic[S]):
    def __init__(self, comprehension_type: S, generator: GeneratorBase):
        self.ctype = comprehension_type
        self.generator = generator

    def render(self, config: Config) -> StrGen:
        yield from Utils.wrap(self.ctype.parens, self.generator.render(config))


class ListComprehension(Comprehension[Type[ListExpr]]):
    """

    If used as `ListComprehension(generator_or_expr: GeneratorBase)`:
        A shorthand for `Comprehension(ListExpr, generator_or_expr)`

    If used as `ListComprehension(generator_or_expr: Expression, parts: Sequence[GeneratorPart])`:
        A shorthand for `Comprehension(ListExpr, GeneratorBase(generator_or_expr, parts))`

    """

    def __init__(
        self,
        generator_or_expr: GeneratorBase | Expression,
        parts: Sequence[GeneratorPart] = (),
    ):

        if not isinstance(generator_or_expr, GeneratorBase):
            generator_or_expr = GeneratorBase(generator_or_expr, parts)

        super().__init__(ListExpr, generator_or_expr)


class SetComprehension(Comprehension[Type[SetExpr]]):
    """

    If used as `SetComprehension(generator_or_expr: GeneratorBase)`:
        A shorthand for `Comprehension(SetExpr, generator_or_expr)`

    If used as `SetComprehension(generator_or_expr: Expression, parts: Sequence[GeneratorPart])`:
        A shorthand for `Comprehension(SetExpr, GeneratorBase(generator_or_expr, parts))`

    """

    def __init__(
        self,
        generator_or_expr: GeneratorBase | Expression,
        parts: Sequence[GeneratorPart] = (),
    ):

        if not isinstance(generator_or_expr, GeneratorBase):
            generator_or_expr = GeneratorBase(generator_or_expr, parts)

        super().__init__(SetExpr, generator_or_expr)


class DictComprehension(Comprehension[Type[DictExpr]]):
    """

    If used as `DictComprehension(generator_or_expr: GeneratorBase)`:
        A shorthand for `Comprehension(DictExpr, generator_or_expr)`

    If used as `DictComprehension(generator_or_expr: KeyValue, parts: Sequence[GeneratorPart])`:
        A shorthand for `Comprehension(DictExpr, GeneratorBase(generator_or_expr, parts))`

    """

    def __init__(
        self,
        generator_or_expr: GeneratorBase | KeyValue,
        parts: Sequence[GeneratorPart] = (),
    ):
        if not isinstance(generator_or_expr, GeneratorBase):
            generator_or_expr = GeneratorBase(generator_or_expr, parts)

        super().__init__(DictExpr, generator_or_expr)


from .generator_expr import GeneratorBase, GeneratorPart
