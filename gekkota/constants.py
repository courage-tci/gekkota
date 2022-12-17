from typing import Any, Iterable, Dict


op_priorities = {
    ":=": 0,
    "lambda": 1,
    "ternary": 2,
    "or": 3,
    "and": 4,
    "unot ": 5,
    ">": 6,
    "<": 6,
    "==": 6,
    "!=": 6,
    ">=": 6,
    "<=": 6,
    "in": 6,
    "not in": 6,
    "is": 6,
    "is not": 6,
    "|": 7,
    "^": 8,
    "&": 9,
    ">>": 10,
    "<<": 11,
    "+": 11,
    "-": 11,
    "*": 12,
    "/": 12,
    "//": 12,
    "%": 12,
    "@": 12,
    "u-": 13,
    "u+": 13,
    "u~": 13,
    "**": 14,
    "await": 15,
    "call": 16,
    "getitem": 16,
    ".": 16,
}

op_associativities = {
    "**": "right",
    "<<": "left",
    ">>": "left",
    "//": "none",
    "await": "left",
}

Config = Dict[str, Any]

default_config: Config = {
    "tab_size": 4,  # how much chars to use in indentation
    "compact": False,  # if True, renders without redundant whitespace (e.g "for [i, e] in enumerate(a)" renders as "for[i,e]in enumerate(a)")
    "tab_char": " ",  # character used for indentation
    "place_semicolons": False,  # if True, semicolons are placed after one-line statements
    "inline_small_stmts": False,  # if True, one-line statements are inlined. Overrides "place_semicolons".
}

StrGen = Iterable[str]
