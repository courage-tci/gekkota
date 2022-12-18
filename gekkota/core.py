from __future__ import annotations

from typing import Callable, Sequence
from .constants import Config, StrGen, default_config


class Renderable:
    def render(self, config: Config) -> StrGen:
        return NotImplemented

    def render_str(self, config: Config | None = None) -> str:
        """The main way to render the code"""
        empty_config: Config = {}
        config = {**default_config, **(config or empty_config)}

        generator = self.render(config)
        if config.get("compact", False):
            generator = Utils.make_compact(generator, config)
        return "".join([*generator])

    def __str__(self) -> str:
        return self.render_str()


class Statement(Renderable):
    """statement, biggest separate part of code"""

    spacing = 0
    get_spacing: Callable[["Statement"], int] = lambda x: x.spacing

    @staticmethod
    def get_max_spacing(statements: Sequence["Statement"]) -> int:
        return max(map(Statement.get_spacing, statements))


from .utils import Utils
