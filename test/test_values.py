from gekkota import Literal, Name



class TestClass:
    def test_numbers(self):
        assert Literal(0).render_str() == "0"
        assert Literal(5).render_str() == "5"
        assert Literal(-5).render_str() == "-5"
        assert Literal(5.0).render_str() == "5.0"
        assert Literal(5+5j).render_str() == "(5+5j)"

    def test_boolean(self):
        assert Literal(True).render_str() == "True"
        assert Literal(False).render_str() == "False"

    def test_none(self):
        assert Literal(None).render_str() == "None"

    def test_string(self):
        assert Literal("Hello, \"World\"").render_str() == "'Hello, \"World\"'"

    def test_bytes(self):
        assert Literal(b'test').render_str() == "b'test'"

    def test_name(self):
        assert Name("a").render_str() == "a"
        assert Name("a", Name("b")).render_str() == "a: b"

