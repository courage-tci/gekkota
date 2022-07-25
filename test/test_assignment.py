from gekkota import Name
from gekkota import Assignment, AugmentedAssignment


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
        assert Assignment([a], b).render_str() == "a = b"
        assert Assignment([a, b], c).render_str() == "a = b = c"

    def test_augassign(self):
        for op in aug_ops:
            assert AugmentedAssignment(a, op, b).render_str() == f"a {op} b"