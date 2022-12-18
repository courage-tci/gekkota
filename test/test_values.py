from gekkota import Literal, Name, FormatSpec, FString


class TestClass:
    def test_numbers(self):
        assert str(Literal(0)) == "0"
        assert str(Literal(5)) == "5"
        assert str(Literal(-5)) == "-5"
        assert str(Literal(5.0)) == "5.0"
        assert str(Literal(5 + 5j)) == "(5+5j)"

    def test_boolean(self):
        assert str(Literal(True)) == "True"
        assert str(Literal(False)) == "False"

    def test_none(self):
        assert str(Literal(None)) == "None"

    def test_string(self):
        assert str(Literal('Hello, "World"')) == "'Hello, \"World\"'"

    def test_bytes(self):
        assert str(Literal(b"test")) == "b'test'"

    def test_name(self):
        assert str(Name("a")) == "a"
        assert str(Name("a", Name("b"))) == "a: b"

    def test_format_spec(self):
        assert str(FormatSpec(Name("a"), spec=".2f")) == "a"

    def test_fstring(self):
        assert str(FString()) == "''"
        assert str(FString(["a"])) == "'a'"
        assert str(FString(["a", "b"])) == "'ab'"

        simple_fstring = FString(["a", Name("b"), "c", FormatSpec(Name("d"), ".2f")])

        assert str(simple_fstring) == "'a{}c{:.2f}'.format(b, d)"

        nested_formatspec = FString(
            [
                "a",
                Name("b"),
                "c",
                FormatSpec(Name("d"), [".", Literal(2), "f"]),
                Name("e"),
                Name("f"),
            ]
        )

        assert str(nested_formatspec) == "'a{}c{:.{}f}{}{}'.format(b, d, 2, e, f)"
