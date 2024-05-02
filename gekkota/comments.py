from gekkota.constants import Config, StrGen
from gekkota.utils import Utils
from .core import Statement


class Comment(Statement):
    """
    text (str): comment text

    use_string (bool): render a string (triple-quote) instead of #-based comment
    """

    def __init__(self, text: str, use_string: bool = False):
        self.lines = text.split("\n")
        self.use_string = use_string

    def render_hashed(self, config: Config) -> StrGen:
        for line in self.lines:
            yield "#"
            yield " "
            yield line
            yield "\n"

    def escape_string(self, s: str):
        return repr(s)[1:-1].replace('"""', '\\"\\"\\"')

    def render_string_contents(self, config: Config) -> StrGen:
        return Utils.separated_str(
            ["\n"],
            (self.escape_string(s) for s in self.lines),
            config,
        )

    def render_string(self, config: Config) -> StrGen:
        yield '"""'

        if len(self.lines) > 1:
            yield "\n"
            yield from Utils.add_tab(self.render_string_contents(config), config)
            yield "\n"

        elif self.lines:
            yield self.escape_string(self.lines[0])

        yield '"""'
        yield "\n"

    def render(self, config: Config) -> StrGen:
        if self.use_string:
            return self.render_string(config)
        return self.render_hashed(config)
