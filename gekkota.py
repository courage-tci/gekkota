from typing import Generator, Union, Sequence, Optional, Callable

StrGen = Generator[str, None, None]


op_priorities = {
    ":=": 0,
    "lambda": 1,
    "ternary": 2,
    "or": 3,
    "and": 4,
    "unot ": 5,
    ">": 6,
    "<": 6,
    "==": 6,
    "!=": 6,
    ">=": 6,
    "<=": 6,
    "in": 6,
    "not in": 6,
    "is": 6,
    "is not": 6,
    "|": 7,
    "^": 8,
    "&": 9,
    ">>": 10,
    "<<": 11,
    "+": 11,
    "-": 11,
    "*": 12,
    "/": 12,
    "//": 12,
    "%": 12,
    "@": 12,
    "u-": 13,
    "u+": 13,
    "u~": 13,
    "**": 14,
    "await": 15,
    "call": 16,
    "getitem": 16,
    ".": 16,
}



class Renderable:
    def render(self, tab_size: int) -> StrGen:
        return NotImplemented

    def render_str(self, tab_size: int = 4) -> str:
        return "".join([*self.render(tab_size)])


class Utils:
    @staticmethod
    def add_tab(generator: StrGen, tab_size: int) -> StrGen:
        tab = tab_size * " "
        yield tab
        for part in generator:
            yield part
            if part == "\n":
                yield tab
    
    @staticmethod
    def separated(separator: str, renderables: Sequence[Renderable], tab_size: int) -> StrGen:
        if not len(renderables):
            yield ""
            return
        yield from renderables[0].render(tab_size)
        for renderable in renderables[1:]:
            yield separator
            yield from renderable.render(tab_size)

    @staticmethod
    def comma_separated(renderables: Sequence[Renderable], tab_size: int) -> StrGen:
        yield from Utils.separated(", ", renderables, tab_size)


class Statement(Renderable):
    """statement, biggest separate part of code"""
    spacing = 0
    get_spacing: Callable[["Statement"], int] = lambda x: x.spacing

    @staticmethod
    def get_max_spacing(statements: Sequence["Statement"]) -> int:
        return max(
            map(
                Statement.get_spacing, 
                statements
            )
        )
    

class Expression(Statement):
    priority = 100
    """expression, a type of statement with a return value"""

    def make_binary_op(left, right: "Expression", op_str: str) -> "BinaryExpr":
        op_priority = op_priorities[op_str]

        if left.priority < op_priority:
            left = Parens(left)
        if right.priority < op_priority:
            if op_str != "**" or not isinstance(right, UnaryExpr):
                right = Parens(right)

        return BinaryExpr(left, right, op_str)

    def make_unary_op(expression, op_str: str) -> "UnaryExpr":
        op_priority = op_priorities[f"u{op_str}"]

        if expression.priority < op_priority:
            expression = Parens(expression)

        return UnaryExpr(expression, op_str, op_priority)

    def __or__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "|")

    def __and__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "&")

    def __xor__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "^")

    def __add__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "+")

    def __sub__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "-")

    def __mul__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "*")

    def __truediv__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "/")

    def __matmul__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "@")

    def __floordiv__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "//")

    def __mod__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "%")

    def __pow__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "**")

    def __rshift__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, ">>")

    def __lshift__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "<<")

    def eq(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "==")

    def neq(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "!=")

    def __gt__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, ">")

    def __ge__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, ">=")

    def __lt__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "<")

    def __le__(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "<=")

    def __call__(self, *args, **kwargs):
        if self.priority < op_priorities["call"]:
            self = Parens(self)

        args = list(args)
        for k in kwargs:
            args.append(CallArg(k, kwargs[k]))
        return CallExpr(self, args)

    def getattr(self, other: str) -> "GetAttr":
        if self.priority < op_priorities["."]:
            self = Parens(self)
        return GetAttr(self, other)

    def __getitem__(self, item):
        return self.index(item)

    def index(self, index: Union["Expression", "SliceExpr", Sequence["SliceExpr"]]) -> "Indexing":
        if self.priority < op_priorities["getitem"]:
            self = Parens(self)

        if isinstance(index, Sequence):
            index = SequenceExpr([
                x 
                if isinstance(x, SliceExpr) 
                else SliceExpr(x.start, x.stop, x.step) # check explanation right below
                for x in index
            ])

        # Case of getting a slice instance is impossible with static typing (since `slice` is not in available types of index)
        # Omitting slice from index typing comes from the fact that slice can be generic only starting from Py3.9 and this is not a good reason to bump minimal supported version
        # Nevertheless, using real slices in Indexing is incredibly convenient so I'd rather support that for folks who don't use type-checking

        if isinstance(index, slice): # type: ignore
            index = SliceExpr(index.start, index.stop, index.step) # type: ignore

        return Indexing(self, index)

    def and_(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "and")

    def or_(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "or")

    def not_(self) -> "UnaryExpr":
        return self.make_unary_op("not ")

    def in_(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "in")

    def not_in(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "not in")

    def is_(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "is")

    def is_not(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, "is not")

    def assign(self, other: "Expression") -> "BinaryExpr":
        return self.make_binary_op(other, ":=")

    def await_(self) -> "AwaitExpr":
        return AwaitExpr(self)

    def __neg__(self) -> "UnaryExpr":
        return self.make_unary_op("-")

    def __pos__(self) -> "UnaryExpr":
        return self.make_unary_op("+")

    def __invert__(self) -> "UnaryExpr":
        return self.make_unary_op("~")


class Parens(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression

    def render(self, tab_size: int) -> StrGen:
        yield "("
        yield from self.expression.render(tab_size)
        yield ")"


class SequenceExpr(Expression):
    parens = "", ""
    def __init__(self, values: Sequence[Expression]):
        self.values = values

    def render(self, tab_size: int) -> StrGen:
        if len(self.values) == 0 and isinstance(self, SetExpr):
            yield "set()"
            return
        yield self.parens[0]
        yield from Utils.comma_separated(self.values, tab_size)
        if len(self.values) == 1 and isinstance(self, TupleExpr):
            yield ", "
        yield self.parens[1]


class ListExpr(SequenceExpr):
    parens = "[", "]"


class TupleExpr(SequenceExpr):
    parens = "(", ")"


class SetExpr(SequenceExpr):
    parens = "{", "}"


class DictExpr(SequenceExpr):
    parens = "{", "}"


class GeneratorPart(Renderable):
    pass

class GeneratorIf(GeneratorPart):
    def __init__(self, condition: Expression):
        self.condition = condition

    def render(self, tab_size: int) -> StrGen:
        yield "if "
        yield from self.condition.render(tab_size)


class GeneratorFor(GeneratorPart):
    def __init__(self, target: Expression, iterator: Expression):
        self.target = target
        self.iterator = iterator

    def render(self, tab_size: int) -> StrGen:
        yield "for "
        yield from self.target.render(tab_size)
        yield " in "
        yield from self.iterator.render(tab_size)


class GeneratorExpr(Expression):
    def __init__(self, expression: Expression, parts: Sequence[GeneratorPart]):
        self.expression = expression
        self.parts = parts

    def render(self, tab_size: int) -> StrGen:
        yield from Utils.separated(" ", [self.expression, *self.parts], tab_size)


class KeyValue(Expression):
    def __init__(self, key: Expression, value: Expression):
        self.key = key
        self.value = value

    def render(self, tab_size: int) -> StrGen:
        yield from self.key.render(tab_size)
        yield ": "
        yield from self.value.render(tab_size)


class SliceExpr(Expression):
    def __init__(self, start: Optional[Expression] = None, stop: Optional[Expression] = None, step: Optional[Expression] = None):
        self.start = start
        self.stop = stop
        self.step = step

    def render(self, tab_size: int) -> StrGen:
        if self.start:
            yield from self.start.render(tab_size)
        
        yield ":"
        
        if self.stop:
            yield from self.stop.render(tab_size)

        if self.step:
            yield ":"
            yield from self.step.render(tab_size)


class Indexing(Expression):
    priority = op_priorities["getitem"]

    def __init__(self, expression: Expression, index: Expression):
        self.expression = expression
        self.index_ = index

    def render(self, tab_size: int) -> StrGen:
        yield from self.expression.render(tab_size)
        yield "["
        yield from self.index_.render(tab_size)
        yield "]"


class CallExpr(Expression):
    def __init__(self, callee: Expression, args: Sequence["AnyCallArg"]):
        self.callee = callee
        self.args = args

    def render(self, tab_size: int) -> StrGen:
        yield from self.callee.render(tab_size)
        yield "("
        yield from Utils.comma_separated(self.args, tab_size)
        yield ")"


class UnaryExpr(Expression):
    def __init__(self, expression: Expression, op: str, priority: int):
        self.expression = expression
        self.op = op
        self.priority = priority

    def render(self, tab_size: int) -> StrGen:
        yield self.op
        yield from self.expression.render(tab_size)


class BinaryExpr(Expression):
    def __init__(self, left: Expression, right: Expression, op: str):
        self.left = left
        self.right = right
        self.op = op
        self.priority = op_priorities[op]

    def render(self, tab_size: int) -> StrGen:
        yield from self.left.render(tab_size)
        yield " "
        yield self.op
        yield " "
        yield from self.right.render(tab_size)


class GetAttr(Expression):
    def __init__(self, value: Expression, attr: str):
        self.value = value
        self.attr = attr

    def render(self, tab_size: int) -> StrGen:
        yield from self.value.render(tab_size)
        yield "."
        yield self.attr


class AwaitExpr(Expression):
    priority = op_priorities["await"]

    def __init__(self, awaitable: Expression):
        self.awaitable = awaitable

    def render(self, tab_size: int) -> StrGen:
        yield "await "
        yield from self.awaitable.render(tab_size)


class Name(Expression):
    def __init__(self, name: str, annotation: Optional[Expression] = None):
        self.name = name
        self.annotation = annotation

    def render(self, tab_size: int) -> StrGen:
        yield self.name
        if self.annotation:
            yield ": "
            yield from self.annotation.render(tab_size)


class Literal(Expression):
    priority = 15
    def __init__(self, value: Union[int, float, complex, str, bytes, bool, None]):
        self.value = value

    def render(self, tab_size: int) -> StrGen:
        yield repr(self.value)


class Block(Statement):
    """block, a type of statement that consists of other statements"""
    def __init__(self, statements: Sequence[Statement]):
        self.statements: Sequence[Statement] = statements

    def render(self, tab_size: int) -> StrGen:
        yield "\n"
        yield from Utils.add_tab(
            self.spaced_render(tab_size), 
            tab_size
        )

    def spaced_render(self, tab_size: int) -> StrGen:
        if not self.statements:
            yield from PassStmt().render(tab_size)
            return

        yield from self.statements[0].render(tab_size)

        for i in range(1, len(self.statements)):
            spacing = Statement.get_max_spacing(self.statements[i - 1: i + 2])
            
            for _ in range(1 + spacing):
                yield "\n"
            yield from self.statements[i].render(tab_size)


class FuncArg(Renderable):
    def __init__(
        self, 
        name: str, 
        annotation: Optional[Expression] = None, 
        default_value: Optional[Expression] = None
    ):
        self.name = name
        self.annotation = annotation
        self.default_value = default_value

    def render(self, tab_size: int) -> StrGen:
        yield self.name
        if self.annotation:
            yield ": "
            yield from self.annotation.render(tab_size)
        if self.default_value:
            if self.annotation:
                yield " = "
            else:
                yield "="
            yield from self.default_value.render(tab_size)


class CallArg(Renderable):
    def __init__(self, name: str, value: Optional[Expression] = None):
        self.name = name
        self.value = value

    def render(self, tab_size: int) -> StrGen:
        yield self.name
        if self.value:
            yield "="
            yield from self.value.render(tab_size)


class StarArg(FuncArg, CallArg, Expression):
    def __init__(self, value: Optional[Expression] = None):
        self.value: Optional[Expression] = value

    def render(self, tab_size: int) -> StrGen:
        yield "*"
        if self.value:
            value = self.value
            if value.priority < self.priority:
                value = Parens(value)
            yield from value.render(tab_size)


class DoubleStarArg(StarArg):
    def render(self, tab_size: int) -> StrGen:
        yield "**"
        if self.value:
            value = self.value
            if value.priority < self.priority:
                value = Parens(value)
            yield from value.render(tab_size)


class Slash(FuncArg):
    def __init__(self):
        pass
    
    def render(self, tab_size: int) -> StrGen:
        yield "/"


AnyFuncArg = Union[FuncArg, Name]
AnyCallArg = Union[CallArg, Expression]


class BlockStmt(Statement):
    body: Statement

    def render_head(self, tab_size: int) -> StrGen:
        return NotImplemented

    def render(self, tab_size: int) -> StrGen:
        yield from self.render_head(tab_size)
        yield ": "
        yield from self.body.render(tab_size)


class LambDef(Expression):
    def __init__(self, args: Sequence[AnyFuncArg], body: Expression):
        self.args = args
        self.body = body

    def render(self, tab_size: int) -> StrGen:
        yield "lambda"
        if self.args:
            yield " "
            yield from Utils.comma_separated(self.args, tab_size)
        yield ": "
        yield from self.body.render(tab_size)


class Decorated(Statement):
    def __init__(self, decorator: Expression, statement: Statement):
        self.decorator = decorator
        self.statement = statement

    def render(self, tab_size: int) -> StrGen:
        yield "@"
        yield from self.decorator.render(tab_size)
        yield "\n"
        yield from self.statement.render(tab_size)


class FuncDef(BlockStmt):
    spacing = 1

    def __init__(self, name: str, args: Sequence[AnyFuncArg], body: Statement, *, rtype: Optional[Expression] = None):
        self.name = name
        self.body = body
        self.args = args
        self.rtype = rtype

    def render_head(self, tab_size: int) -> StrGen:
        yield "def "
        yield self.name
        yield "("
        yield from Utils.comma_separated(self.args, tab_size)
        yield ")"
        if self.rtype:
            yield " -> "
            yield from self.rtype.render(tab_size)


class ClassDef(BlockStmt):
    spacing = 1
    def __init__(self, name: str, args: Sequence[AnyCallArg], body: Statement):
        self.name = name
        self.body = body
        self.args = args

    def render_head(self, tab_size: int) -> StrGen:
        yield "class "
        yield self.name
        if self.args:
            yield "("
            yield from Utils.comma_separated(self.args, tab_size)
            yield ")"


class IfStmt(BlockStmt):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body

    def render_head(self, tab_size: int) -> StrGen:
        yield "if "
        yield from self.condition.render(tab_size)


class ElifStmt(IfStmt):
    def render_head(self, tab_size: int) -> StrGen:
        yield "elif "
        yield from self.condition.render(tab_size)


class ElseStmt(BlockStmt):
    def __init__(self, body: Statement):
        self.body = body

    def render_head(self, tab_size: int) -> StrGen:
        yield "else"


class WhileStmt(IfStmt):
    def render_head(self, tab_size: int):
        yield "while "
        yield from self.condition.render(tab_size)


class ForStmt(BlockStmt):
    def __init__(self, target: Expression, iterator: Expression, body: Statement):
        self.target = target
        self.iterator = iterator
        self.body = body

    def render_head(self, tab_size: int) -> StrGen:
        yield "for "
        yield from self.target.render(tab_size)
        yield " in "
        yield from self.iterator.render(tab_size)


class TryStmt(BlockStmt):
    def __init__(self, body: Statement):
        self.body = body

    def render_head(self, tab_size: int):
        yield "try"


class ExceptStmt(BlockStmt):
    def __init__(self, exceptions: Sequence[Name], alias: Optional[Name], body: Statement):
        self.exceptions = exceptions
        self.alias = alias
        self.body = body

    def render_head(self, tab_size: int) -> StrGen:
        yield "except"
        if self.exceptions:
            yield " "
            if len(self.exceptions) > 1:
                yield from TupleExpr(self.exceptions).render(tab_size)
            else:
                yield from self.exceptions[0].render(tab_size)
            if self.alias:
                yield " as "
                yield from self.alias.render(tab_size)


class FinallyStmt(BlockStmt):
    def __init__(self, body: Statement):
        self.body = body

    def render_head(self, tab_size: int) -> StrGen:
        yield "finally"


class RaiseStmt(Statement):
    def __init__(self, exception: Optional[Expression] = None, scope: Optional[Expression] = None):
        self.exception = exception
        self.scope = scope

    def render(self, tab_size: int) -> StrGen:
        yield "raise"
        if self.exception:
            yield " "
            yield from self.exception.render(tab_size)
            if self.scope:
                yield " from "
                yield from self.scope.render(tab_size)


class WithTarget(Expression):
    def __init__(self, expression: Expression, alias: Optional[str] = None):
        self.expression = expression
        self.alias = alias

    def render(self, tab_size: int) -> StrGen:
        yield from self.expression.render(tab_size)
        if self.alias:
            yield " as "
            yield self.alias


class WithStmt(BlockStmt):
    def __init__(self, targets: Sequence[Union[WithTarget, Expression]], body: Statement):
        self.targets = targets
        self.body = body

    def render_head(self, tab_size: int) -> StrGen:
        yield "with "
        yield from Utils.comma_separated(self.targets, tab_size)


class SmallStmt(Statement):
    prefix: str
    has_contents: bool = True

    def __init__(self, expression: Optional[Expression] = None):
        self.expression = expression

    def render(self, tab_size: int) -> StrGen:
        yield self.prefix
        if self.expression and self.has_contents:
            yield " "
            yield from self.expression.render(tab_size)


class ReturnStmt(SmallStmt):
    prefix = "return"


class BreakStmt(SmallStmt):
    prefix = "break"
    has_contents = False


class ContinueStmt(SmallStmt):
    prefix = "continue"
    has_contents = False


class YieldStmt(SmallStmt, Expression):
    priority = -1
    prefix = "yield"


class YieldFromStmt(YieldStmt):
    prefix = "yield from"


class PassStmt(SmallStmt):
    prefix = "pass"
    has_contents = False


class GlobalStmt(Statement):
    def __init__(self, names: Sequence[Name]):
        self.names = names

    def render(self, tab_size: int) -> StrGen:
        yield "global "
        yield from Utils.comma_separated(self.names, tab_size)


class NonLocalStmt(GlobalStmt):
    def render(self, tab_size: int) -> StrGen:
        yield "nonlocal "
        yield from Utils.comma_separated(self.names, tab_size)


class DelStmt(Statement):
    def __init__(self, target: Expression):
        self.target = target

    def render(self, tab_size: int) -> StrGen:
        yield "del "
        yield from self.target.render(tab_size)


class AssertStmt(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def render(self, tab_size: int) -> StrGen:
        yield "assert "
        yield from self.expression.render(tab_size)


class AsyncStmt(Statement):
    def __init__(self, statement: Union[Statement, GeneratorFor]):
        self.statement = statement

    def render(self, tab_size: int) -> StrGen:
        yield "async "
        yield from self.statement.render(tab_size)


Target = Union[SequenceExpr, GetAttr, Indexing, StarArg, SequenceExpr]


class Assignment(Statement):
    def __init__(self, targets: Sequence[Expression], value: Expression):
        self.targets = targets
        self.value = value

    def render(self, tab_size: int) -> StrGen:
        yield from Utils.separated(" = ", [*self.targets, self.value], tab_size)


AugTarget = Union[Name, GetAttr, Indexing]



class AugmentedAssignment(Statement):
    def __init__(self, target: AugTarget, op: str, expression: Expression):
        self.target = target
        self.op = op
        self.expression = expression

    def render(self, tab_size: int) -> StrGen:
        yield from self.target.render(tab_size)
        yield " "
        yield self.op
        yield " "
        yield from self.expression.render(tab_size)


class ImportSource(Renderable):
    def __init__(self, parts: Sequence[str]):
        self.parts = parts

    def render(self, tab_size: int) -> StrGen:
        if self.parts:
            yield self.parts[0]
            for i in range(1, len(self.parts)):
                yield "."
                yield self.parts[i]


class ImportDots(ImportSource):
    def __init__(self, length: int = 1):
        self.length = length

    def render(self, tab_size: int) -> StrGen:
        for _ in range(self.length):
            yield "."


class ImportAlias(Renderable):
    def __init__(self, name: Name, alias: Optional[Name] = None):
        self.name = name
        self.alias = alias

    def render(self, tab_size: int) -> StrGen:
        yield from self.name.render(tab_size)
        if self.alias:
            yield " as "
            yield from self.alias.render(tab_size)


AnyImportAlias = Union[ImportAlias, Name]
AnyImportSource = Union[ImportSource, Name]


class ImportStmt(Statement):
    def __init__(self, names: Sequence[AnyImportAlias]):
        self.names = names

    def render(self, tab_size: int) -> StrGen:
        yield "import "
        yield from Utils.comma_separated(self.names, tab_size)


class FromImportStmt(Statement):
    def __init__(self, source: AnyImportSource, names: Sequence[AnyImportAlias]):
        self.source = source
        self.names = names

    def render(self, tab_size: int) -> StrGen:
        yield "from "
        yield from self.source.render(tab_size)
        yield " import "
        yield from Utils.comma_separated(self.names, tab_size)


class Code(Renderable):
    """whole code as it is"""
    def __init__(self, statements: Sequence[Statement]):
        self.statements = statements

    def render(self, tab_size: int) -> StrGen:
        if not self.statements:
            yield ""
            return

        yield from self.statements[0].render(tab_size)

        for i in range(1, len(self.statements)):
            spacing = Statement.get_max_spacing(self.statements[i - 1: i + 2]) * 2

            for _ in range(1 + spacing):
                yield "\n"
            yield from self.statements[i].render(tab_size)