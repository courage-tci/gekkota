from gekkota import Name
from gekkota import (
    MatchStmt,
    CaseStmt,
    AsPattern,
    OrPattern,
    WildcardPattern,
    CapturePattern,
    ValuePattern,
    LiteralPattern,
    StarPattern,
    OpenSequencePattern,
    SequencePattern,
    KeywordPattern,
    ClassPattern,
    DoubleStarPattern,
    KeyValuePattern,
    MappingPattern,
    GroupPattern,
)
from gekkota import Literal


a = Name("a")
b = Name("b")
c = Name("c")

a_pattern = CapturePattern("a")
b_pattern = CapturePattern("b")
c_pattern = CapturePattern("c")

or_pattern = OrPattern([a_pattern, b_pattern])
simple_case = CaseStmt(a_pattern, b)
guard_case = CaseStmt(a_pattern, b, c)


class TestClass:
    def test_match(self):
        assert str(MatchStmt(c, [simple_case])) == "match c: \n    case a: b"
        assert str(MatchStmt(c, [])) == "match c: pass"

    def test_case(self):
        assert str(simple_case) == "case a: b"
        assert str(guard_case) == "case a if c: b"

    def test_as_pattern(self):
        assert str(AsPattern(a_pattern, b_pattern)) == "a as b"

    def test_or_pattern(self):
        assert str(OrPattern([a_pattern, b_pattern])) == "a | b"

    def test_wildcard_pattern(self):
        assert str(WildcardPattern()) == "_"

    def test_capture_pattern(self):
        assert str(a_pattern) == "a"

    def test_value_pattern(self):
        assert str(ValuePattern(a.getattr("b"))) == "a.b"
        assert str(ValuePattern(a.getattr("b")).getattr("c")) == "a.b.c"

    def test_literal_pattern(self):
        assert str(LiteralPattern(6)) == str(Literal(6))
        assert str(LiteralPattern("6")) == str(Literal("6"))

    def test_star_pattern(self):
        assert str(StarPattern(a_pattern)) == "*a"

    def test_double_star_pattern(self):
        assert str(DoubleStarPattern(a_pattern)) == "**a"

    def test_open_sequence_pattern(self):
        assert str(OpenSequencePattern([a_pattern, b_pattern])) == "a, b,"

    def test_sequence_pattern(self):

        assert str(SequencePattern([a_pattern, b_pattern])) == "[a, b,]"

    def test_keyword_pattern(self):
        assert str(KeywordPattern("b", a_pattern)) == "b=a"

    def test_class_pattern(self):
        assert str(ClassPattern(a)) == "a()"
        assert str(ClassPattern(a, [b_pattern])) == "a(b)"
        assert (
            str(ClassPattern(a, [b_pattern], [KeywordPattern("d", c_pattern)]))
            == "a(b, d=c)"
        )
        assert str(ClassPattern(a, [], [KeywordPattern("d", c_pattern)])) == "a(d=c)"

    def test_key_value_pattern(self):
        assert str(KeyValuePattern(a_pattern.getattr("b"), c_pattern)) == "a.b: c"

    def test_mapping_pattern(self):
        kv = KeyValuePattern(a_pattern.getattr("b"), c_pattern)

        assert str(MappingPattern([])) == "{}"
        assert (
            str(
                MappingPattern(
                    [
                        kv,
                    ]
                )
            )
            == "{a.b: c}"
        )

    def test_group_pattern(self):
        assert str(GroupPattern(a_pattern)) == "(a)"

    def test_or(self):
        assert str(or_pattern | or_pattern) == "a | b | a | b"
        assert str(or_pattern | c_pattern) == "a | b | c"
        assert str(c_pattern | or_pattern) == "c | a | b"
        assert str(a_pattern | b_pattern) == "a | b"

    def test_as(self):
        assert str(or_pattern.as_(c_pattern)) == "a | b as c"
        assert str(a_pattern.as_(c_pattern)) == "a as c"
