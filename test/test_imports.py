from gekkota import Name
from gekkota import ImportStmt, FromImportStmt, ImportAlias, ImportSource, ImportDots


a = Name("a")
b = Name("b")
c = Name("c")


class TestClass:
    def test_import(self):
        assert str(ImportStmt([a, b])) == "import a, b"
        assert (
            str(ImportStmt([ImportAlias(a, b), ImportAlias(b, a)]))
            == "import a as b, b as a"
        )

    def test_from_import(self):
        assert str(FromImportStmt(a, [b, c])) == "from a import b, c"
        assert (
            str(FromImportStmt(a, [ImportAlias(b, c), ImportAlias(c, b)]))
            == "from a import b as c, c as b"
        )

    def test_import_source(self):
        assert str(ImportSource(["a", "b"])) == "a.b"
        assert str(ImportSource(["", "b"])) == ".b"
        assert str(ImportSource(["", "", ""])) == ".."
        assert str(ImportDots(2)) == ".."
