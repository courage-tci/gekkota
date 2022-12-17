from gekkota import Name
from gekkota import FuncDef, ClassDef, LambDef, FuncArg, Decorated


a = Name("a")
b = Name("b")
c = Name("c")


class TestClass:
    def test_funcarg(self):
        assert str(FuncArg("a")) == "a"
        assert str(FuncArg("a", b)) == "a: b"
        assert str(FuncArg("a", b, c)) == "a: b = c"
        assert str(FuncArg("a", None, c)) == "a=c"

    def test_funcdef(self):
        assert str(FuncDef("a", (), b)) == "def a(): b"
        assert str(FuncDef("a", (), b, rtype=c)) == "def a() -> c: b"
        assert str(FuncDef("a", (a, b, c), b, rtype=a)) == "def a(a, b, c) -> a: b"

    def test_classdef(self):
        assert str(ClassDef("A", (), b)) == "class A: b"
        assert str(ClassDef("A", (a, b), c)) == "class A(a, b): c"

    def test_lambdef(self):
        assert str(LambDef([], a)) == "lambda: a"
        assert str(LambDef([a], b)) == "lambda a: b"
        assert str(LambDef([a, b], c)) == "lambda a, b: c"

    def test_decorated(self):
        minfunc = FuncDef("b", (), c)
        assert str(Decorated(a, minfunc)) == "@a\ndef b(): c"

    def test_async(self):
        minfunc = FuncDef("b", (), c, is_async=True)
        assert str(minfunc) == "async def b(): c"
