from gekkota import Statement, Utils, Renderable, Slash, BlockStmt


class TestClass:
    def test_add_tab(self):
        generator = (x for x in ["a", "\n", "\n", "b"])
        assert "".join(Utils.add_tab(generator, 4)) == "    a\n    \n    b"

    def test_spacer(self):
        s1 = Statement()
        s2 = Statement()
        
        s1.spacing = 30
        s2.spacing = 15

        assert Statement.get_max_spacing([s1, s2]) == 30
        assert Statement.get_max_spacing([s2, s1]) == 30

    def test_renderable(self):
        assert Renderable().render(tab_size=4) == NotImplemented

    def test_blockstmt(self):
        assert BlockStmt().render_head(tab_size=4) == NotImplemented

    def test_slash(self):
        assert Slash().render_str() == "/"