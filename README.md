[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/courage-tci/gekkota/build.yml?branch=pub)](https://github.com/courage-tci/gekkota/actions/workflows/build.yml)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/courage-tci/gekkota/test.yml?branch=pub&label=tests)](https://github.com/courage-tci/gekkota/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/gekkota)](https://pypi.org/project/gekkota/)
![PyPI - Downloads](https://pepy.tech/badge/gekkota)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gekkota)
[![Coveralls](https://img.shields.io/coverallsCoverage/github/courage-tci/gekkota?label=test%20coverage)](https://coveralls.io/github/courage-tci/gekkota?branch=pub)
![License](https://img.shields.io/github/license/courage-tci/gekkota)
![Badge Count](https://img.shields.io/badge/badges-8-important)

This is a Python code-generation module.    

- Generates any Python statement/expression
- Places parens to ensure expression priorities are unchanged
- Places extra newlines before/after class/function definitions to conform with PEP 8
- 100% coverage of type hints, passing MyPy with `--disallow-any-expr`
- Meaningful type hierarchy inspired by Python grammar
- Covered with ~~diamonds~~ tests completely 

## Installation

Just install `gekkota` package, e.g. with `python -m pip install gekkota` (or any other package manager of your choice)

## Rendering and configuration

To render any `Renderable` into a string, you could use a few approaches:

- `str(renderable)`: renders a Renderable with default configuration (check below)
- `renderable.render_str()`: also default configuration
- `renderable.render_str(config)`: overrides default config options with provided in `config` mapping. Unspecified keys remain at default values

Here is current default config:
```python
default_config: Config = {
    "tab_size": 4,  # how much chars to use in indentation
    "compact": False,  # if True, renders without redundant whitespace (e.g "for [i, e] in enumerate(a)" renders as "for[i,e]in enumerate(a)")
    "tab_char": " ",  # character used for indentation
    # "place_semicolons" and "inline_small_stmts" options have some performance impact, since those require checking for newlines in token stream before re-streaming tokens.
    # this impact is probably negligible, but be aware of it
    "place_semicolons": False,  # if True, semicolons are placed after one-line statements
    "inline_small_stmts": False,  # if True, one-line statements are inlined. Overrides "place_semicolons" if True.
}
```


## Expressions

### Basic expressions

Your starting points would be `to_expression` and `Name`:

```python
from gekkota import Name, to_expression

# Name(name: str, annotation: Optional[Expression] = None)
# to_expression(value: int | float | complex | str | bytes | bool | None)

a = Name("a")
b = Name("b")
six = to_expression(6)

# prints 'a + b * 6'
print(
    (a + b * six)
)

```

`Name`, as many other classes in the module, is an `Expression` instance

Expressions support most operations to combine with other expressions.    
Exceptions are:

- Attribute reference: for that you should use `Expression.getattr(other: str)`
- Indexing: `Expression.index(index: Expression)`
- Slicing: `Expression.index(index: Union[SliceExpr, Sequence[SliceExpr]])`
- Equality / Inequality: `Expression.eq(right_hand_side)` and `Expression.neq(right_hand_side)` respectively
- `is`: `Expression.is_(right_hand_side)`,
- `is not`: `Expression.is_not(right_hand_side)`
- `in`: `Expression.in_(right_hand_side)`
- `not in`: `Expression.not_in(right_hand_side)`
- `and`: `Expression.and_(right_hand_side)`
- `or`: `Expression.or_(right_hand_side)`
- `await`: `Expression.await_()`
- `:=` assignment: `Expression.assign(value)`
- Ternary operator: `Expression.if_(condition, alternative)`

For example:

```python
from gekkota import Name

a = Name("a")
b = Name("b")

expression = a.await_().in_(b)

print(expression) # await a in b

```

For any other operation on expressions you can just use familiar Python syntax:

```python
from gekkota import Name

a = Name("a")
b = Name("b")
c = Name("c")

print(
    (a + b * c / a(b, c)) # 'a + b * c / a(b, c)'
)

```

### Sequences

Most convenient way to create sequence literals is, again, `to_expression`:

```python
from gekkota import to_expression, Name

a = Name("a")
b = Name("b")

print(
    to_expression( (a, b, 6) ), # '(a, b, 6)' (notice that to_expression is recursive)
    to_expression( (a, ) ),     # '(a, )'
    to_expression([a, b]),      # '[a, b]'
    to_expression([]),          # '[]'
    to_expression({a: b}),      # '{a: b}'
    to_expression(set()),       # 'set()'
    to_expression([a, [a, b]]), # '[a, [a, b]]'
)
```

If you want to have more precise control, you can use `TupleExpr`, `ListExpr`, `SetExpr` and `DictExpr` for this.
All have same constructor signature: `(values: Sequence[Expression])` (except `DictExpr`, which has `KeyValue` values)

To create comprehensions:

```python
from gekkota import Name, GeneratorFor, GeneratorIf
from gekkota import (
    ListComprehension,
    DictComprehension,
    KeyValue,
    SetComprehension, # same usage as ListComprehension
)

a, b, c, d = map(Name, "abcd")

# ListComprehension(generator_or_expr: GeneratorBase | Expression, parts: Sequence[GeneratorPart] = ())
print(
    ListComprehension(
        a, 
        [
            # GeneratorFor(target: AssignmentTarget, iterator: Expression, *, is_async: bool = False)
            GeneratorFor(b, c), 
            
            # GeneratorIf(condition: Expression)
            GeneratorIf(b.eq(d))
        ]
    )
) # [a for b in c if b == d]

# DictComprehension(generator_or_expr: GeneratorBase | KeyValue, parts: Sequence[GeneratorPart] = ())
# GeneratorPart == GeneratorFor | GeneratorIf
print(
    DictComprehension(KeyValue(a, b), [GeneratorFor(c, d), GeneratorIf(b.eq(d))])
) # {a: b for c in d if b == d}

```

### Keyword call args

Use `CallArg` to provide keyword call args:

```python
from gekkota import Name, to_expression

print_ = Name("print")

# CallArg(name: str, value: Optional[Expression] = None)
print(
    print_(
        Name("a"),
        CallArg("b"),
        CallArg("sep", to_expression(", "))
    )
) # print(a, b, sep=', ')

```

### Type hints

To annotate a name, just pass an additional parameter to `Name`:

```python
from gekkota import Name

a = Name("a", Name("int"))

print(a) # a: int

```

Be aware that this usage is not restricted to valid places at the moment. For example:

```python
from gekkota import Name

a = Name("a", Name("int"))

# doesn't produce any typecheck errors
print(a + a) # a: int + a: int
print(Name("b", Name("a", Name("int")))) # b: a: int
```

This would probably be fixed in the future in some way.
Annotations for other code (namely function args and return types) is described in relevant sections.

## Statements

To render program code (with multiple statements), use `Code`:

```python
from gekkota import Code, Assignment, Name

a = Name("a")

six = Literal(6)

create_variable = Assignment(
    [Name("a")], 
    six + six
)

print_variable = Name("print")(a)

print(
    Code([
        create_variable,
        print_variable,
    ])
)
# prints:
# a = 6 + 6
# print(a)

```

To render a block of code, use `Block`:

```python
from gekkota import Block, IfStmt, Assignment, Name

a = Name("a")
b = Name("b")

six = Literal(6)

create_variable = Assignment(
    [Name("a")], 
    six + six
)

print_variable = Name("print")(a)

print(
    IfStmt(
        b, 
        Block([
            create_variable,
            print_variable,
        ])
    )
)
# prints:
# if b:
#     a = 6 + 6
#     print(a)

```

If the difference between two is not obvious: `Code` just renders statements on separate lines, while block also adds a newline before the first statement and indentation to every line.
Moreover, `Code([])` renders into `""`, while `Block([])` — into `"\n    pass"`


### Small statements

Here is an example of a few small statements:

```python
from gekkota import Name, SequenceExpr
from gekkota import (
    ReturnStmt, 
    DelStmt, 
    AssertStmt, 
    BreakStmt, 
    ContinueStmt, 
    YieldStmt, 
    YieldFromStmt, 
    NonLocalStmt, 
    GlobalStmt, 
    PassStmt, 
    RaiseStmt, 
    AsyncStmt
)

a, b, c = map(Name, "abc")

print(ReturnStmt(a)) # 'return a'

print(YieldStmt(a)) # 'yield a'
print(YieldFromStmt(b)) # 'yield from b'

print(DelStmt(a, b)) # 'del a, b'

print(AssertStmt(a)) # 'assert a'

print(BreakStmt()) # 'break'

print(ContinueStmt()) # 'continue'

print(GlobalStmt(a, b)) # 'global a, b'
print(NonLocalStmt(a, b)) # 'nonlocal a, b'

print(PassStmt()) # 'pass'

print(RaiseStmt()) # 'raise' 
print(RaiseStmt(a)) # 'raise a'
print(RaiseStmt(a, b)) # 'raise a from b'
```

### Assignment

For common assigment use `Assignment`:

```python
from gekkota import Assignment, Name

a, b, c = map(Name, "abc")

# Assignment(targets: Sequence[AssignmentTarget] | AnnotatedTarget, value: Expression)

print(
    Assignment([a], b), # a = b
    Assignment([a.index(b)], c) # a[b] = c
    Assignment([a, b], c), # a = b = c
)

```

To annotate assignment (or just annotate a variable), use `AnnotatedTarget`:

```python

from gekkota import Assignment, AnnotatedTarget, Name

a, b, c = map(Name, "abc")
D = Name("D")

# AnnotatedTarget(target: AssignmentTarget, annotation: Expression)
print(
    Assignment(AnnotatedTarget(a, D), b), # a: D = b
    Assignment(AnnotatedTarget(a.index(b), D), c) # a[b]: D = c
    Assignment([a, b], c), # a = b = c
)

```

For augmented assignment (e.g. `+=`) use `AugmentedAssignment`:

```python
from gekkota import Assignment, Name

a, b, c = map(Name, "abc")

# AugmentedAssignment(target: AugAssignmentTarget, op: str, expression: Expression)

print(
    AugmentedAssignment(a, "+=", b), # a += b
    AugmentedAssignment(a.index(b), "*=", c) # a *= c
)

```

### Control flow

For control flow you can use `IfStmt`, `ElifStmt` and `ElseStmt`:

```python
from gekkota import Name, IfStmt, ElifStmt, ElseStmt, Code

a, b, c = map(Name, "abc")

# IfStmt(condition: Expression, body: Statement)
# ElifStmt(condition: Expression, body: Statement)
# ElseStmt(body: Statement)
code = Code([
    IfStmt(a, b),
    ElifStmt(b, a),
    ElseStmt(c)
])

print(code)
"""
if a: b
elif b: a
else: c
"""
```

### Loops

Use `ForStmt` and `WhileStmt` for loops:

```python
from gekkota import ForStmt, WhileStmt, Name

a, b, c = map(Name, "abc")

# ForStmt(target: Expression, iterator: Expression, body: Statement, *, is_async: bool = False)
print(
    ForStmt(a, b, c)
) # for a in b: c

# WhileStmt(condition: Expression, body: Statement)
print(
    WhileStmt(a, b)
) # while a: b
```

### Functions

To render a function definition, you will need a `FuncDef`:

```python
from gekkota import Name, FuncDef

a, b, c = map(Name, "abc")

# FuncDef(name: str, args: Sequence[FuncArg], body: Statement, *, rtype: Optional[Expression] = None, is_async: bool = False)
print(
    FuncDef(
        "cool_func",
        [a],
        b,
        rtype=c,
    )
) # def cool_func(a) -> c: b
```

To provide a default value and/or annotations to arguments, use `FuncArg`:

```python

from gekkota import Name, FuncDef, FuncArg, to_expression

a, b, c = map(Name, "abc")

# FuncDef(name: str, args: Sequence[FuncArg], body: Statement, *, rtype: Optional[Expression] = None, is_async: bool = False)
# FuncArg(name: str, annotation: Optional[Expression] = None, default_value: Optional[Expression] = None)
print(
    FuncDef(
        "cool_func",
        [
            FuncArg(
                "a", 
                Name("int"), 
                to_expression(0)
            )
        ],
        b,
        rtype=c,
    )
) # def cool_func(a: int = 0) -> c: b

```

Other argument types are:

- `StarArg(value: T = None)`: generates `*value`, `*` by default
- `DoubleStarArg(value)`: same as `StarArg`, but with `**`
- `Slash()` is `/` (a mark of positional-only arguments in Python 3.8+)

Lambda functions are generated using `LambDef`:

```python
from gekkota import Name, LambDef

a, b, c = map(Name, "abc")

# LambDef(args: Sequence[FuncArg], body: Expression)
print(
    LambDef(
        [a],
        b,
    )
) # lambda a: b
```

To decorate a function/class, use `Decorated`:

```python
from gekkota import Name, FuncDef, Decorated

decorator = Name("decorator")
a, b, c = map(Name, "abc")

# Decorated(decorator: Expression, statement: ClassDef | FuncDef)
# FuncDef(name: str, args: Sequence[FuncArg], body: Statement, *, rtype: Optional[Expression] = None, is_async: bool = False)
print(
    Decorated(
        decorator,
        FuncDef(
            "cool_func",
            [a],
            b,
            rtype=c,
        )
    )
)
# @decorator
# def cool_func(a) -> c: b
```

### Classes

To define a class, use `ClassDef`:

```python
from gekkota import Name, ClassDef

a, b, c = map(Name, "abc")

# ClassDef(name: str, args: Sequence[CallArg | Expression], body: Statement)
print(
    ClassDef("MyClass1", [], a)
) # class MyClass1: a

print(
    ClassDef("MyClass2", [b], c)
) # class MyClass2(b): c

```

### Imports

To render imports, use `ImportStmt` and `FromImportStmt`:

```python
from gekkota import Name, StarArg, ImportDots, ImportSource, ImportStmt, FromImportStmt, ImportAlias


# ImportStmt(names: Sequence[ImportAlias | Name | StarArg[None]])
print(
    ImportStmt([Name("a")])
) # import a

print(
    ImportStmt([Name("a"), Name("b")])
) # import a, b

# FromImportStmt(source: ImportSource | Name, names: Sequence[ImportAlias | Name | StarArg[None]])
# ImportAlias(name: Name, alias: Name | None = None)
print(
    FromImportStmt(
        Name("math"), 
        [
            Name("cos"), 
            ImportAlias(Name("sin"), Name("tan")) # we do a little trolling
        ]
    )
) # from math import cos, sin as tan

print(
    FromImportStmt(
        Name("gekkota"),
        [StarArg()]
    )
) # from gekkota import *

# ImportDots(length: int = 1)
print(
    FromImportStmt(
        ImportDots(),
        [StarArg()]
    )
) # from . import *

# ImportSource(parts: Sequence[str])
print(
    FromImportStmt(
        ImportSource(["", "values"]),
        [Name("Name")]
    )
) # from .values import Name

```

### Exceptions

```python
from gekkota import Name, TryStmt, ExceptStmt, FinallyStmt, Block

a, b, e = map(Name, "abe")

# TryStmt(body: Statement)
print(
    TryStmt(a)
) # try: a

# ExceptStmt(exceptions: Sequence[Expression] | None, alias: Name | None, body: Statement)
print(
    ExceptStmt(None, None, a)
) # except: a

print(
    ExceptStmt(None, None, Block([]))
) 
# except:
#     pass

print(
    ExceptStmt([a], None, b)
) # except a: b

print(
    ExceptStmt([a], e, b)
) # except a as e: b

# FinallyStmt(body: Statement)
print(
    FinallyStmt(a)
) # finally: a

```

### Context Managers

```python
from gekkota import Name, WithStmt, WithTarget

a, b, e = map(Name, "abe")

# WithStmt(targets: Sequence[WithTarget | Expression], body: Statement, *, is_async: bool = False,)
print(
    WithStmt([a], b)
) # with a: b

# WithTarget(expression: Expression, alias: str | None = None)
print(
    WithStmt([WithTarget(a, "aaaa")], b)
) # with a as aaaa: b

print(
    WithStmt([a], b, is_async=True)
) # async with a: b

```

### Pattern matching

This section is currently unfinished, check [pattern_matching.py](https://github.com/courage-tci/gekkota/blob/pub/gekkota/pattern_matching.py)

## Custom rendering

If your custom element can be meaningfully represented as a combination of existing elements, you can use a function instead of a class:

```python
from gekkota import Expression

def Square(e: Expression) -> Expression:
    return e * e

```

This is a pretty obvious approach, but often it works best.

---

While being aimed at Python code generation, `gekkota` is pretty extensible, and can be used to render different things.    
You can build custom renderables, statements, expressions, and so on.    

The simplest example of a custom renderable would be:

```python
from gekkota import Renderable, StrGen, Config


class RenderString(Renderable):
    """It renders whatever is passed to it"""

    def __init__(self, value: str):
        self.value = value

    def render(self, config: Config) -> StrGen:
        yield self.value
```

Let's suppose you want to render a custom expression: a custom sequence literal (obviously isn't valid in Python, but you need it for some reason).    
Suppose your custom literal would be in form of `<|value1, value2, ...|>`.

You can extend `SequenceExpr` for that:

```python
from gekkota import SequenceExpr, Name

class MyCoolSequence(SequenceExpr):
    parens = "<|", "|>"


seq = MyCoolSequence([Name("a"), Name("b")])

print(seq) # <|a,b|>

```

That's it, you're ready to render this literal (which, again, isn't valid in Python but anyway).

Or you could go further and write rendering by yourself (it's easier than it sounds):

```python
from gekkota import Expression, Config


class MyCoolSequence(Expression):
    def __init__(self, values: Sequence[Expression]):
        self.values = values

    # could be rewritten to be simpler, check `Useful utils` section below
    def render(self, config: Config) -> StrGen:
        yield "<|"

        for i, item in enumerate(self.values):
            yield from item.render(config)

            if i + 1 < len(self.values): # no comma after last element
                yield ","
                yield " "

        yield "|>"
```

It's fairly easy, just render every part in the right order:

- To render a string, use `yield string`
- To render a `Renderable`, use `yield from renderable.render(config)`


### Choosing a right base class

To choose a right base class, think in what context you want to use your renderable.    
If there is a similar context in Python (e.g. your renderable is a block statement, like `for` or `if`), extend that class.    

After choosing a right base class, check if it has a predefined render, maybe you won't need to write everything by yourself.    
For example, with `BlockStmt` you need to provide `render_head` instead:

```python
# that's the actual source from module, not an example

class BlockStmt(Statement):
    body: Statement

    def render_head(self, config: Config) -> StrGen:
        return NotImplemented

    def render(self, config: Config) -> StrGen:
        yield from self.render_head(config)
        yield ":"
        yield " "
        yield from self.body.render(config)

[...]

class ElseStmt(BlockStmt):
    def __init__(self, body: Statement):
        self.body = body

    def render_head(self, config: config) -> StrGen:
        yield "else"
```

### Useful utils

`gekkota.utils` provides `Utils` class which is useful for custom renderables. For example, custom `MyCoolSequence` could be implemented as:

```python
from gekkota import Expression, Utils


class MyCoolSequence(Expression):
    def __init__(self, values: Sequence[Expression]):
        self.values = values

    def render(self, config: config) -> StrGen:
        yield from Utils.wrap(
            ["<|", "|>"],
            Utils.comma_separated(self.values, config)
        )
```

Methods provided in `Utils`:

- `add_tab(generator: StrGen, config: Config) -> StrGen`    
    Adds indentation to a stream of tokens, using provided `config`    
    For example, `Utils.add_tab(Name("a").render(config), config)` -> Iterable of ['    ', 'a']

- `separated(separator: Sequence[str], renderables: Sequence[Renderable], config: Config) -> StrGen`    
    Inserts separator between renderables (and renders them in stream)    
    For example: `Utils.separated([",", " "], self.values, config)` - inserts ", " between elements of `self.values`    

- `separated_str(separator: Sequence[str], strings: Sequence[str], config: Config)`    
    Same as previous, but for `str` sequences

- `comma_separated(renderables: Sequence[Renderable], config: Config) -> StrGen`    
    Alias for `Utils.separated([",", " "], renderables, config)`

- `make_compact(generator: StrGen, config: Config) -> StrGen`    
    Filters all unneccessary whitespace from stream (doesn't respect `config["compact"]`). Config is unused at the moment, but provided for compatibility with future updates

- `wrap(parens: Sequence[str], generator: StrGen) -> StrGen`    
    Wraps a token stream with strings from `parens` array (should have 2 elements).    
    In other words, inserts `parens[0]` at the start of the stream, and `parens[1]` at the end