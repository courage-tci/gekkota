from typing import Sequence
from .constants import Config, StrGen
from .core import Renderable, Statement
from .small_stmt import PassStmt
from .utils import Utils


class Code(Renderable):
    """whole code as it is"""

    def __init__(self, statements: Sequence[Statement]):
        self.statements = statements

    def render(self, config: Config) -> StrGen:
        if not self.statements:
            yield ""
            return

        yield from self.spaced_render(config)

    def spaced_render(self, config: Config) -> StrGen:
        last_one_line = True

        inline_small = config.get("inline_small_stmts", False)
        place_semicolons = config.get("place_semicolons", False) or inline_small

        generator = self.statements[0].render(config)

        if place_semicolons:
            for token in generator:
                if token == "\n":
                    last_one_line = False
                yield token
        else:
            yield from generator

        for i in range(1, len(self.statements)):
            spacing = Statement.get_max_spacing(self.statements[i - 1 : i + 2])

            if place_semicolons and last_one_line:
                yield ";"

            if inline_small and last_one_line:
                yield " "

            else:
                for _ in range(1 + spacing):
                    yield "\n"

            last_one_line = True

            generator = self.statements[i].render(config)

            if place_semicolons:
                tokens = [*generator]

                for token in tokens:
                    if token == "\n":
                        last_one_line = False

                if not last_one_line:
                    yield "\n"

                yield from tokens

            else:
                yield from generator


class Block(Statement, Code):
    """block, a type of statement that consists of other statements"""

    def render(self, config: Config) -> StrGen:
        generator = (
            PassStmt().render(config)
            if not self.statements
            else self.spaced_render(config)
        )
        yield "\n"
        yield from Utils.add_tab(generator, config)


class BlockStmt(Statement):
    body: Statement

    def render_head(self, config: Config) -> StrGen:
        return NotImplemented

    def render(self, config: Config) -> StrGen:
        yield from self.render_head(config)
        yield ":"
        yield " "
        yield from self.body.render(config)
