from gekkota import Name
from gekkota import Assignment, AugmentedAssignment, AnnotatedTarget


a = Name("a")
b = Name("b")
c = Name("c")


aug_ops = [
    "+=",
    "-=",
    "*=",
    "@=",
    "/=",
    "//=",
    "%=",
    "**=",
    ">>=",
    "<<=",
    "&=",
    "^=",
    "|=",
]


class TestClass:
    def test_assignment(self):
        assert str(Assignment([a], b)) == "a = b"
        assert str(Assignment([a, b], c)) == "a = b = c"

    def test_augassign(self):
        for op in aug_ops:
            assert str(AugmentedAssignment(a, op, b)) == f"a {op} b"

    def test_annasign(self):
        ab = AnnotatedTarget(a, b)
        assert str(ab) == "a: b"

        assert str(Assignment(ab, c)) == "a: b = c"
