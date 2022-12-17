from typing import Union, overload

from .values import Literal, LiteralValue
from .sequences import DictExpr, KeyValue, ListExpr, SequenceExpr, SetExpr, TupleExpr
from .expression import Expression


SequenceLiteral = Union[
    "dict[ValueOrExpression, ValueOrExpression]",
    "list[ValueOrExpression]",
    "set[ValueOrExpression]",
    "tuple[ValueOrExpression, ...]",
]

ValueOrExpression = Union[LiteralValue, Expression, SequenceLiteral]


@overload
def to_expression(convertable: LiteralValue) -> Literal:
    ...


@overload
def to_expression(convertable: SequenceLiteral) -> SequenceExpr:
    ...


@overload
def to_expression(convertable: ValueOrExpression) -> Expression:
    ...


def to_expression(
    convertable: ValueOrExpression,
) -> Expression:
    """Converts a value into an Expression instance. If Expression instance passed, returns it unchanged"""
    if isinstance(convertable, Expression):
        return convertable

    if isinstance(convertable, (list, set, tuple)):
        seq_converted = list(map(to_expression, convertable))

        if isinstance(convertable, list):
            return ListExpr(seq_converted)

        if isinstance(convertable, tuple):
            return TupleExpr(seq_converted)

        return SetExpr(seq_converted)

    if isinstance(convertable, dict):
        return DictExpr(
            [
                KeyValue(to_expression(key), to_expression(value))
                for key, value in convertable.items()
            ]
        )

    return Literal(convertable)
