from gekkota import to_expression
from gekkota import Literal, ListExpr, TupleExpr, DictExpr, SetExpr
from gekkota.sequences import KeyValue


class TestClass:
    def test_literals(self):
        assert str(to_expression(6)) == str(Literal(6))
        assert str(to_expression("1")) == str(Literal("1"))
        assert str(to_expression(b"123")) == str(Literal(b"123"))
        assert str(to_expression(True)) == str(Literal(True))
        assert str(to_expression(None)) == str(Literal(None))

    def test_sequences(self):
        assert str(to_expression([])) == str(ListExpr([]))
        assert str(to_expression([1, 2])) == str(ListExpr([Literal(1), Literal(2)]))

        assert str(to_expression(())) == str(TupleExpr([]))
        assert str(to_expression((1, 2))) == str(TupleExpr([Literal(1), Literal(2)]))

        assert str(to_expression(set())) == str(SetExpr([]))
        assert str(to_expression({1, 2})) == str(SetExpr([Literal(1), Literal(2)]))

        assert str(to_expression({})) == str(DictExpr([]))
        assert str(to_expression({1: 2})) == str(
            DictExpr([KeyValue(Literal(1), Literal(2))])
        )

    def test_expression(self):
        t = Literal(10)
        assert to_expression(t) is t
