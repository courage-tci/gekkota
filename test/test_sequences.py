from gekkota import Name
from gekkota import SetExpr, ListExpr, TupleExpr, DictExpr, KeyValue
from gekkota import GeneratorExpr, GeneratorFor, GeneratorIf


a = Name("a")
b = Name("b")


class TestClass:
    def test_list(self):
        assert ListExpr([a, b]).render_str() == "[a, b]"
        assert ListExpr([a]).render_str() == "[a]"

    def test_dict(self):
        assert DictExpr([KeyValue(a, b)]).render_str() == "{a: b}"

    def test_tuple(self):
        assert TupleExpr([a, b]).render_str() == "(a, b)"
        assert TupleExpr([a]).render_str() == "(a, )"

    def test_set(self):
        assert SetExpr([a, b]).render_str() == "{a, b}"
        assert SetExpr([]).render_str() == "set()"

    def test_generator(self):
        assert GeneratorExpr(
            a,
            [
                GeneratorFor(a, b),
                GeneratorIf(a)
            ]
        ).render_str() == "a for a in b if a"