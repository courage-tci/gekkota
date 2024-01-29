from __future__ import annotations
from typing import Sequence, Union


from .core import Renderable
from .expression import Expression
from .utils import Utils
from .constants import Config, StrGen
from .small_stmt import SmallStmt
from .values import Identifier, Name


class TypeStmt(SmallStmt):
    def __init__(
        self,
        name: Identifier,
        type_params: Sequence[TypeParam],
        value: Expression,
    ):
        self.name = name
        self.type_params = type_params
        self.value = value

    def render(self, config: Config) -> StrGen:
        yield "type"
        yield " "
        yield from self.name.render(config)

        if self.type_params:
            yield "["
            yield from Utils.comma_separated(self.type_params, config)
            yield "]"

        yield " "
        yield "="
        yield " "

        yield from self.value.render(config)


class TypeParamConcrete(Renderable):
    pass


class TypeVarParam(TypeParamConcrete):
    def __init__(
        self,
        name: Identifier,
        value: Expression | None = None,
        default: Expression | None = None,
    ):
        self.name = name
        self.value = value
        self.default = default

    def render(self, config: Config) -> StrGen:
        yield from self.name.render(config)

        if self.value:
            yield from (":", " ")
            yield from self.value.render(config)

        if self.default:
            yield from (" ", "=", " ")
            yield from self.default.render(config)


class TypeVarTupleParam(TypeParamConcrete):
    def __init__(
        self,
        name: Identifier,
        default: Expression | None = None,
    ):
        self.name = name
        self.default = default

    def render(self, config: Config) -> StrGen:
        yield "*"
        yield from self.name.render(config)

        if self.default:
            yield from (" ", "=", " ")
            yield from self.default.render(config)


class ParamSpecParam(TypeParamConcrete):
    def __init__(
        self,
        name: Identifier,
        default: Expression | None = None,
    ):
        self.name = name
        self.default = default

    def render(self, config: Config) -> StrGen:
        yield "**"
        yield from self.name.render(config)

        if self.default:
            yield from (" ", "=", " ")
            yield from self.default.render(config)


TypeParam = Union[Name, TypeParamConcrete]
