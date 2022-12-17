from __future__ import annotations

from typing import Optional
from .constants import Config, StrGen
from .core import Renderable


class CallArg(Renderable):
    def __init__(self, name: str, value: Optional[Expression] = None):
        self.name = name
        self.value = value

    def render(self, config: Config) -> StrGen:
        yield self.name
        if self.value:
            yield "="
            yield from self.value.render(config)


class FuncArg(Renderable):
    def __init__(
        self,
        name: str,
        annotation: Optional[Expression] = None,
        default_value: Optional[Expression] = None,
    ):
        self.name = name
        self.annotation = annotation
        self.default_value = default_value

    def render(self, config: Config) -> StrGen:
        yield self.name
        if self.annotation:
            yield ":"
            yield " "
            yield from self.annotation.render(config)
        if self.default_value:
            if self.annotation:
                yield " "
                yield "="
                yield " "
            else:
                yield "="
            yield from self.default_value.render(config)


from .expression import Expression, Parens

from typing import Generic
from typing_extensions import TypeVar

T = TypeVar("T", default=Optional[Expression], bound=Optional[Expression])


class StarArg(FuncArg, Expression, Generic[T]):
    def __init__(self, value: T = None):
        self.value = value

    def render(self, config: Config) -> StrGen:
        yield "*"
        if self.value is not None:
            value = self.value
            if value.priority < self.priority:
                value = Parens(value)
            yield from value.render(config)


class DoubleStarArg(StarArg[Expression]):
    def render(self, config: Config) -> StrGen:
        yield "*"
        yield from super().render(config)


class Slash(FuncArg):
    def __init__(self):
        pass

    def render(self, config: Config) -> StrGen:
        yield "/"
