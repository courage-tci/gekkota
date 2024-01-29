from gekkota import Name, TypeStmt, TypeVarParam, TypeVarTupleParam, ParamSpecParam
from gekkota.args import FuncArg
from gekkota.classes import ClassDef
from gekkota.functions import FuncDef


a, b, c, d = map(Name, "abcd")


class TestClass:
    def test_typevar(self):
        assert str(TypeVarParam(a)) == "a"
        assert str(TypeVarParam(a, b)) == "a: b"
        assert str(TypeVarParam(a, b, c)) == "a: b = c"
        assert str(TypeVarParam(a, default=c)) == "a = c"

    def test_typevartuple(self):
        assert str(TypeVarTupleParam(a)) == "*a"
        assert str(TypeVarTupleParam(a, c)) == "*a = c"

    def test_paramspec(self):
        assert str(ParamSpecParam(a)) == "**a"
        assert str(ParamSpecParam(a, c)) == "**a = c"

    def test_type_stmt(self):
        assert str(TypeStmt(a, [], b)) == "type a = b"
        assert str(TypeStmt(a, [b, c], d)) == "type a[b, c] = d"

    def test_genericfunc(self):
        assert (
            str(FuncDef("f", [FuncArg("arg", a)], b, rtype=a, type_params=[a]))
            == "def f[a](arg: a) -> a: b"
        )

    def test_genericclass(self):
        assert (
            str(
                ClassDef(
                    "c",
                    [],
                    a,
                    type_params=[b],
                )
            )
            == "class c[b]: a"
        )
