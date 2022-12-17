from gekkota import Name
from gekkota import SetExpr, ListExpr, TupleExpr, DictExpr, KeyValue
from gekkota import GeneratorExpr, GeneratorFor, GeneratorIf
from gekkota import (
    SetComprehension,
    ListComprehension,
    DictComprehension,
)


a, b, c, d = map(Name, "abcd")


class TestClass:
    def test_list(self):
        assert str(ListExpr([a, b])) == "[a, b]"
        assert str(ListExpr([a])) == "[a]"
        assert str(ListExpr([])) == "[]"
        assert str(ListComprehension(a, [GeneratorFor(b, c)])) == "[a for b in c]"

    def test_dict(self):
        assert str(DictExpr([KeyValue(a, b)])) == "{a: b}"
        assert (
            str(DictComprehension(KeyValue(a, b), [GeneratorFor(c, d)]))
            == "{a: b for c in d}"
        )

    def test_tuple(self):
        assert str(TupleExpr([a, b])) == "(a, b)"
        assert str(TupleExpr([a])) == "(a, )"

    def test_set(self):
        assert str(SetExpr([a, b])) == "{a, b}"
        assert str(SetExpr([])) == "set()"
        assert str(SetComprehension(a, [GeneratorFor(b, c)])) == "{a for b in c}"

    def test_generator(self):
        assert (
            str(GeneratorExpr(a, [GeneratorFor(b, c), GeneratorIf(d)]))
            == "(a for b in c if d)"
        )

    def test_async_generator(self):
        assert (
            str(GeneratorExpr(a, [GeneratorFor(b, c, is_async=True), GeneratorIf(d)]))
            == "(a async for b in c if d)"
        )
