from typing import Generic
from typing_extensions import Never, TypeVar
from .constants import Config, StrGen
from .core import Renderable, Statement
from .expression import Expression
from .utils import Utils
from .values import Name

T = TypeVar("T", default=Expression, bound=Renderable)


class SmallStmt(Statement, Generic[T]):
    prefix: str

    def __init__(self, *contents: T):
        self.contents = contents

    def render(self, config: Config) -> StrGen:
        yield self.prefix

        if not self.contents:
            return

        yield " "
        yield from Utils.comma_separated(self.contents, config)


class ReturnStmt(SmallStmt):
    prefix = "return"


class BreakStmt(SmallStmt[Never]):
    prefix = "break"


class ContinueStmt(SmallStmt[Never]):
    prefix = "continue"


class YieldStmt(SmallStmt, Expression):
    priority = -1
    prefix = "yield"


class YieldFromStmt(SmallStmt, Expression):
    prefix = "yield from"
    priority = -1


class PassStmt(SmallStmt[Never]):
    prefix = "pass"


class GlobalStmt(SmallStmt[Name]):
    prefix = "global"


class NonLocalStmt(GlobalStmt):
    prefix = "nonlocal"


class DelStmt(SmallStmt):
    prefix = "del"


class AssertStmt(SmallStmt):
    prefix = "assert"
