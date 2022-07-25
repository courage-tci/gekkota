from gekkota import Name, SequenceExpr
from gekkota import ReturnStmt, DelStmt, AssertStmt, BreakStmt, ContinueStmt, YieldStmt, YieldFromStmt, NonLocalStmt, GlobalStmt, PassStmt, RaiseStmt, AsyncStmt

a = Name("a")
b = Name("b")


class TestClass:
    def test_return(self):
        assert ReturnStmt(a).render_str() == "return a"

    def test_yield(self):
        assert YieldStmt(a).render_str() == "yield a"
        assert YieldFromStmt(b).render_str() == "yield from b"

    def test_del(self):
        assert DelStmt(SequenceExpr([a, b])).render_str() == "del a, b"

    def test_assert(self):
        assert AssertStmt(a).render_str() == "assert a"

    def test_break(self):
        assert BreakStmt().render_str() == "break"

    def test_continue(self):
        assert ContinueStmt().render_str() == "continue"

    def test_global(self):
        assert GlobalStmt([a, b]).render_str() == "global a, b"

    def test_nonlocal(self):
        assert NonLocalStmt([a, b]).render_str() == "nonlocal a, b"

    def test_pass(self):
        assert PassStmt().render_str() == "pass"

    def test_raise(self):
        assert RaiseStmt().render_str() == "raise" 
        assert RaiseStmt(a).render_str() == "raise a"
        assert RaiseStmt(a, b).render_str() == "raise a from b"

    def test_async(self):
        assert AsyncStmt(a).render_str() == "async a"