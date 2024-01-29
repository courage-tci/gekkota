from wordstreamer import Renderable as WSBaseRenderable
from gekkota import WStoG, WSRenderable, WSString, Name, to_expression
from wordstreamer.startkit import Stringify

a, b, c, d = map(Name, "abcd")


class TestClass:
    def test_ws_renderable(self):
        ws_compatible = WSRenderable(a)

        assert isinstance(ws_compatible, WSBaseRenderable)
        assert ws_compatible.render_string() == "a"

        ws_compatible_list = WSRenderable(to_expression([a, b, c]))

        assert isinstance(ws_compatible_list, WSBaseRenderable)
        assert ws_compatible_list.render_string() == "[a, b, c]"

    def test_ws_to_g(self):
        ws_literal = Stringify("a")

        class WSName(WStoG, Name):
            def __init__(self, renderable: WSBaseRenderable):
                self.annotation = None
                super().__init__(renderable)

            @property
            def name(self):
                return self.render_str()

        ws_a = WSName(ws_literal)

        assert str(ws_a) == "a"

    def test_ws_string(self):
        ws_a_string = Stringify("a")

        assert str(WSString(ws_a_string)) == '"""a"""'
