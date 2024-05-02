from __future__ import annotations

from typing import Sequence, Iterable


class Utils:
    @staticmethod
    def add_tab(generator: StrGen, config: Config) -> StrGen:
        tab_size: int = config.get("tab_size", 4)
        tab_char: str = config.get("tab_char", " ")

        tab = tab_size * tab_char
        yield tab
        for part in generator:
            yield part
            if part == "\n":
                yield tab

    @staticmethod
    def separated(
        separator: Iterable[str], renderables: Iterable[Renderable], config: Config
    ) -> StrGen:
        counter = 0

        for renderable in renderables:
            if counter:
                yield from separator

            yield from renderable.render(config)

            counter += 1

        if not counter:
            yield ""

    @staticmethod
    def separated_str(separator: Iterable[str], strings: Iterable[str], config: Config):
        counter = 0

        for renderable in strings:
            if counter:
                yield from separator

            yield renderable

            counter += 1

        if not counter:
            yield ""

    @staticmethod
    def comma_separated(renderables: Iterable[Renderable], config: Config) -> StrGen:
        yield from Utils.separated(", ", renderables, config)

    @staticmethod
    def make_compact(generator: StrGen, config: Config) -> StrGen:
        is_tab = False
        last_token_isalpha = False
        for token in generator:
            if token == "\n":
                is_tab = True
            elif token != " ":
                is_tab = False

            if token == " " and not is_tab:
                continue

            if token.startswith("0."):
                token = token[1:]

            if (token[0] == "_" or token[0].isalnum()) and last_token_isalpha:
                yield " "

            last_token_isalpha = token[-1] == "_" or token[-1].isalpha()
            yield token

    @staticmethod
    def wrap(parens: Sequence[str], generator: StrGen) -> StrGen:
        yield parens[0]
        yield from generator
        yield parens[1]


from .core import Renderable
from .constants import Config, StrGen
