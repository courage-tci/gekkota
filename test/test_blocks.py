from gekkota import Name
from gekkota import (
    Block,
    Code,
    IfStmt,
    ElifStmt,
    ElseStmt,
    WhileStmt,
    ForStmt,
    TryStmt,
    ExceptStmt,
    FinallyStmt,
    WithStmt,
    WithTarget,
)


a = Name("a")
b = Name("b")
c = Name("c")


class TestClass:
    def test_block(self):
        assert Block([]).render_str({"tab_size": 4}) == "\n    pass"
        assert Block([]).render_str({"tab_size": 4, "compact": True}) == "\n    pass"
        assert Block([a]).render_str({"tab_size": 4}) == "\n    a"
        assert Block([a, b]).render_str({"tab_size": 4}) == "\n    a\n    b"
        assert Block([a, b]).render_str({"tab_size": 2}) == "\n  a\n  b"
        assert (
            Block([a, b]).render_str({"tab_char": "\t", "tab_size": 1}) == "\n\ta\n\tb"
        )

    def test_code(self):
        assert str(Code([])) == ""
        assert str(Code([a, b])) == "a\nb"

    def test_if(self):
        assert str(IfStmt(a, b)) == "if a: b"
        assert str(ElifStmt(a, b)) == "elif a: b"
        assert str(ElseStmt(b)) == "else: b"

    def test_while(self):
        assert str(WhileStmt(a, b)) == "while a: b"

    def test_for(self):
        assert str(ForStmt(a, b, c)) == "for a in b: c"
        assert str(ForStmt(a, b, c, is_async=True)) == "async for a in b: c"

    def test_try(self):
        assert str(TryStmt(a)) == "try: a"
        assert str(ExceptStmt([a], b, c)) == "except a as b: c"
        assert str(ExceptStmt(None, None, a)) == "except: a"
        assert str(ExceptStmt([a], None, b)) == "except a: b"
        assert str(ExceptStmt([a, b], None, c)) == "except (a, b): c"
        assert str(FinallyStmt(a)) == "finally: a"

    def test_with(self):
        assert str(WithStmt([a], b)) == "with a: b"
        assert str(WithStmt([a], b, is_async=True)) == "async with a: b"
        assert str(WithStmt([WithTarget(a, "b")], c)) == "with a as b: c"
        assert (
            str(WithStmt([WithTarget(a, "b"), WithTarget(a, "b")], c))
            == "with a as b, a as b: c"
        )

    def test_inline(self):
        block = Block([a, b])

        assert block.render_str({"tab_size": 1}) == "\n a\n b"
        assert (
            block.render_str({"tab_size": 1, "place_semicolons": True}) == "\n a;\n b"
        )
        assert (
            block.render_str({"tab_size": 1, "inline_small_stmts": True}) == "\n a; b"
        )

        assert (
            block.render_str(
                {"tab_size": 1, "inline_small_stmts": True, "compact": True}
            )
            == "\n a;b"
        )

        assert (
            Block([block, c, c]).render_str({"tab_size": 1, "inline_small_stmts": True})
            == "\n \n  a; b\n c; c"
        )

        assert (
            Block([c, block, c]).render_str({"tab_size": 1, "inline_small_stmts": True})
            == "\n c; \n \n  a; b\n c"
        )
