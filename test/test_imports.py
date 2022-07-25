from gekkota import Name
from gekkota import ImportStmt, FromImportStmt, ImportAlias, ImportSource, ImportDots


a = Name("a")
b = Name("b")
c = Name("c")


class TestClass:
    def test_import(self):
        assert ImportStmt([a, b]).render_str() == "import a, b"
        assert ImportStmt([ImportAlias(a, b), ImportAlias(b, a)]).render_str() == "import a as b, b as a"

    def test_from_import(self):
        assert FromImportStmt(a, [b, c]).render_str() == "from a import b, c"
        assert FromImportStmt(a, [ImportAlias(b, c), ImportAlias(c, b)]).render_str() == "from a import b as c, c as b"

    def test_import_source(self):
        assert ImportSource(["a", "b"]).render_str() == "a.b"
        assert ImportSource(["", "b"]).render_str() == ".b"
        assert ImportSource(["", "", ""]).render_str() == ".."
        assert ImportDots(2).render_str() == ".."


