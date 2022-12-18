from gekkota import Statement, Utils, Renderable, Slash
from gekkota.block import BlockStmt


class TestClass:
    def test_add_tab(self):
        tokens = ["a", "\n", "\n", "b"]
        assert "".join(Utils.add_tab(tokens, {"tab_size": 4})) == "    a\n    \n    b"

    def test_spacer(self):
        s1 = Statement()
        s2 = Statement()

        s1.spacing = 30
        s2.spacing = 15

        assert Statement.get_max_spacing([s1, s2]) == 30
        assert Statement.get_max_spacing([s2, s1]) == 30

    def test_renderable(self):
        assert Renderable().render({"tab_size": 4}) == NotImplemented

    def test_blockstmt(self):
        assert BlockStmt().render_head({"tab_size": 4}) == NotImplemented

    def test_slash(self):
        assert str(Slash()) == "/"

    def test_separated_str(self):
        assert "".join(Utils.separated_str(["|"], [], {})) == ""
        assert "".join(Utils.separated_str(["|"], ["1"], {})) == "1"
        assert "".join(Utils.separated_str(["|"], ["1", "2"], {})) == "1|2"
