from __future__ import annotations

from typing import Sequence, Union

from .utils import Utils
from .constants import Config, StrGen
from .core import Renderable, Statement
from .values import GetAttr, Indexing, Name


AugAssignmentTarget = Union[
    Name, GetAttr["AugAssignmentTarget"], Indexing["AugAssignmentTarget"]
]

AssignmentTarget = Union[
    Name,
    "SequenceExpr[AssignmentTarget]",
    "StarArg[AssignmentTarget]",
    Indexing["AssignmentTarget"],
    GetAttr["AssignmentTarget"],
]


class Assignment(Statement):
    def __init__(
        self, targets: Sequence[AssignmentTarget] | AnnotatedTarget, value: Expression
    ):
        self.targets = targets
        self.value = value

    def render(self, config: Config) -> StrGen:
        if isinstance(self.targets, AnnotatedTarget):
            yield from self.targets.render(config)
        else:
            yield from Utils.separated(" = ", self.targets, config)
        yield " "
        yield "="
        yield " "
        yield from self.value.render(config)


class AnnotatedTarget(Statement):
    def __init__(self, target: AssignmentTarget, annotation: Expression):
        self.target = target
        self.annotation = annotation

    def render(self, config: Config) -> StrGen:
        yield from self.target.render(config)
        yield ": "
        yield from self.annotation.render(config)


class AugmentedAssignment(Statement):
    def __init__(self, target: AugAssignmentTarget, op: str, expression: Expression):
        self.target = target
        self.op = op
        self.expression = expression

    def render(self, config: Config) -> StrGen:
        yield from self.target.render(config)
        yield " "
        yield self.op
        yield " "
        yield from self.expression.render(config)


from .sequences import SequenceExpr
from .args import StarArg
from .expression import Expression
