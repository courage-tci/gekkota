from gekkota import Name, SequenceExpr
from gekkota import (
    ReturnStmt,
    DelStmt,
    AssertStmt,
    BreakStmt,
    ContinueStmt,
    YieldStmt,
    YieldFromStmt,
    NonLocalStmt,
    GlobalStmt,
    PassStmt,
    RaiseStmt,
)

a = Name("a")
b = Name("b")


class TestClass:
    def test_return(self):
        assert str(ReturnStmt(a)) == "return a"

    def test_yield(self):
        assert str(YieldStmt()) == "yield"
        assert str(YieldStmt(a)) == "yield a"
        assert str(YieldFromStmt(b)) == "yield from b"

    def test_del(self):
        assert str(DelStmt(SequenceExpr([a, b]))) == "del a, b"

    def test_assert(self):
        assert str(AssertStmt(a)) == "assert a"

    def test_break(self):
        assert str(BreakStmt()) == "break"

    def test_continue(self):
        assert str(ContinueStmt()) == "continue"

    def test_global(self):
        assert str(GlobalStmt(a, b)) == "global a, b"

    def test_nonlocal(self):
        assert str(NonLocalStmt(a, b)) == "nonlocal a, b"

    def test_pass(self):
        assert str(PassStmt()) == "pass"

    def test_raise(self):
        assert str(RaiseStmt()) == "raise"
        assert str(RaiseStmt(a)) == "raise a"
        assert str(RaiseStmt(a, b)) == "raise a from b"
