from gekkota import Name
from gekkota import Block, IfStmt, ElifStmt, ElseStmt, WhileStmt, ForStmt, TryStmt, ExceptStmt, FinallyStmt, WithStmt, WithTarget


a = Name("a")
b = Name("b")
c = Name("c")


class TestClass:
    def test_block(self):
        assert Block([a]).render_str(tab_size=4) == "\n    a"

    def test_if(self):
        assert IfStmt(a, b).render_str() == "if a: b"
        assert ElifStmt(a, b).render_str() == "elif a: b"
        assert ElseStmt(b).render_str() == "else: b"

    def test_while(self):
        assert WhileStmt(a, b).render_str() == "while a: b"

    def test_for(self):
        assert ForStmt(a, b, c).render_str() == "for a in b: c"

    def test_try(self):
        assert TryStmt(a).render_str() == "try: a"
        assert ExceptStmt([a], b, c).render_str() == "except a as b: c"
        assert ExceptStmt(None, None, a).render_str() == "except: a"
        assert ExceptStmt([a], None, b).render_str() == "except a: b"
        assert FinallyStmt(a).render_str() == "finally: a"

    def test_with(self):
        assert WithStmt([a], b).render_str() == "with a: b"
        assert WithStmt([WithTarget(a, "b")], c).render_str() == "with a as b: c"
        assert WithStmt(
            [WithTarget(a, "b"), WithTarget(a, "b")],
            c
        ).render_str() == "with a as b, a as b: c" 