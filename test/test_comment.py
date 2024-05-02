from gekkota import Comment


class TestClass:
    def test_hashed(self):
        assert str(Comment("test")) == "# test\n"
        assert str(Comment("test\notherline")) == "# test\n# otherline\n"

    def test_string(self):
        assert str(Comment("test", use_string=True)) == '"""test"""\n'
        assert (
            str(Comment("test\ntest2", use_string=True))
            == '"""\n    test\n    test2\n"""\n'
        )
