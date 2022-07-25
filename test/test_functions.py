from gekkota import Name
from gekkota import FuncDef, ClassDef, LambDef, FuncArg, Decorated


a = Name("a")
b = Name("b")
c = Name("c")


class TestClass:
    def test_funcarg(self):
        assert FuncArg("a").render_str() == "a"
        assert FuncArg("a", b).render_str() == "a: b"
        assert FuncArg("a", b, c).render_str() == "a: b = c"
        assert FuncArg("a", None, c).render_str() == "a=c"

    def test_funcdef(self):
        assert FuncDef("a", (), b).render_str() == "def a(): b"
        assert FuncDef("a", (), b, rtype=c).render_str() == "def a() -> c: b"
        assert FuncDef("a", (a, b, c), b, rtype=a).render_str() == "def a(a, b, c) -> a: b"

    def test_classdef(self):
        assert ClassDef("A", (), b).render_str() == "class A: b"
        assert ClassDef("A", (a, b), c).render_str() == "class A(a, b): c"

    def test_lambdef(self):
        assert LambDef([], a).render_str() == "lambda: a"
        assert LambDef([a], b).render_str() == "lambda a: b"
        assert LambDef([a, b], c).render_str() == "lambda a, b: c"

    def test_decorated(self):
        assert Decorated(a, b).render_str() == "@a\nb"