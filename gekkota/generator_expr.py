from __future__ import annotations
from typing import Sequence

from .core import Renderable
from .constants import Config, StrGen
from .expression import Expression


class GeneratorPart(Renderable):
    pass


class GeneratorIf(GeneratorPart):
    def __init__(self, condition: Expression):
        self.condition = condition

    def render(self, config: Config) -> StrGen:
        yield "if"
        yield " "
        yield from self.condition.render(config)


class GeneratorFor(GeneratorPart):
    def __init__(
        self,
        target: AssignmentTarget,
        iterator: Expression,
        *,
        is_async: bool = False,
    ):
        self.target = target
        self.iterator = iterator
        self.is_async = is_async

    def render(self, config: Config) -> StrGen:
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


class GeneratorBase(Renderable):
    def __init__(
        self, expression: Expression | KeyValue, parts: Sequence[GeneratorPart]
    ):
        self.expression = expression
        self.parts = parts

    def render(self, config: Config) -> StrGen:
        yield from Utils.separated(" ", [self.expression, *self.parts], config)


class GeneratorExpr(Expression):
    def __init__(self, expression: Expression, parts: Sequence[GeneratorPart]):
        self.base = GeneratorBase(expression, parts)

    def render(self, config: Config) -> StrGen:
        yield "("
        yield from self.base.render(config)
        yield ")"


from .assignment import AssignmentTarget
from .sequences import KeyValue
from .utils import Utils
