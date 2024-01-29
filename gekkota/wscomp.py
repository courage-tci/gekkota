from wordstreamer import Context, Renderable as WSBaseRenderable, Renderer, TokenStream
from wordstreamer.utils import is_marker

from .values import Literal
from .constants import Config, StrGen
from .core import Renderable


class WSRenderable(WSBaseRenderable):
    """Lets you use gekkota.Renderable as wordstreamer.renderable"""

    def __init__(self, renderable: Renderable):
        self.renderable = renderable

    def stream(self, context: Context) -> TokenStream:
        return self.renderable.render(context._renderer.context)


def make_stream(renderable: WSBaseRenderable, config: Config) -> StrGen:
    return adapt_tokenstream(Renderer().stream(renderable, config))


def adapt_tokenstream(ts: TokenStream) -> StrGen:
    for token in ts:
        if not is_marker(token):
            assert isinstance(token, str)
            yield token


class WStoG:
    """

    Base class to help using a wordstreamer.Renderable as gekkota.Renderable. May introduce syntax errors

    Example usage:

    ```python
    from gekkota import WStoG, Literal
    from wordstreamer.startkit import Stringify

    # create a class to define the type of renderable
    class WSLiteral(WStoG, Literal):
        pass

    some_number = Stringify(6)

    print(WSLiteral(some_number) + Literal(8)) # "6 + 8"
    ```
    """

    def __init__(self, renderable: WSBaseRenderable):
        self.renderable = renderable

    def render(self, config: Config) -> StrGen:
        return make_stream(self.renderable, config)


class WSString(Literal):
    """Lets you render a wordstreamer.Renderable inside a Python string"""

    def __init__(self, renderable: WSBaseRenderable):
        self.renderable = renderable

    def render(self, config: Config) -> StrGen:
        stream = make_stream(self.renderable, config)

        yield '"""'
        for token in stream:
            yield token.replace('"', '"')
        yield '"""'
