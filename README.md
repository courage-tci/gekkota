This is a Python code-generation module.    

- Generates any Python statement/expression
- Places parens to ensure expression priorities are unchanged
- Places extra newlines before/after class/function definitions to conform with PEP 8
- 100% coverage of type hints, passing MyPy with `--disallow-any-expr`
- Meaningful type hierarchy inspired by Python grammar
- Covered with ~~diamonds~~ tests completely


## Expressions

### Basic expressions

Your starting points would be `Literal` and `Name`:

```python
from gekkota import Name, Literal

# Name(self, name: str, annotation: Optional[Expression] = None)
# Literal(self, value: Union[int, float, complex, str, bytes, bool, None])

a = Name("a")
b = Name("b")
six = Literal(6)

# prints 'a + b * 6'
print(
    (a + b * six).render_str()
)

```

`Name`, as many other classes in the module, is an `Expression` object

Expressions support most operations to combine with other expressions.    
Exceptions are:

- Attribute reference: for that you should use `Expression.getattr(self, other: str)`
- Indexing: `Expression.index(self, index: Expression)`
- Slicing: `Expression.index(self, index: Union[SliceExpr, Sequence[SliceExpr]])`
- Equality / Inequality: `Expression.eq(self, other: Expression)` and `Expression.neq(self, other: Expression)` respectively
- `is`, `is not`, `in`, `not in`, `and`, `or`: `Expression.is_`, `Expression.is_not`, `Expression.in_`, `Expression.not_in`, `Expression.and_`, `Expression.or_`
- `await`: `Expression.await_(self)`
- `:=` aswsignment: `Expression.assign`

For example:

```python
from gekkota import Name, Literal

a = Name("a")
b = Name("b")

expression = a.await_().in_(b)

print(expression.render_str()) # await a in b

```


For any other operation on expressions you can just use familiar Python syntax:


```python
from gekkota import Name

a = Name("a")
b = Name("b")
c = Name("c")

print(
    (a + b * c / a(b, c)).render_str() # 'a + b * c / a(b, c)'
)


```

### Sequences

There is a common class for all sequences, `SequenceExpr`.
It has 4 children: `TupleExpr`, `ListExpr`, `SetExpr` and `DictExpr`.
All have same signature: `SequenceExpr(self, values: Sequence[Expression])`:

```python
from gekkota import ListExpr, TupleExpr, DictExpr, KeyValue, SetExpr, Name

a = Name("a")
b = Name("b")

print(
    TupleExpr([a, b, Literal(6)]).render_str(), # '(a, b, 6)'
    TupleExpr([a]).render_str(),                # '(a, )'
    ListExpr([a, b]).render_str(),              # '[a, b]'
    ListExpr([]).render_str(),                  # '[]'
    DictExpr([KeyValue(a, b)]).render_str(),    # '{a: b}'
    SetExpr([]).render_str()                    # 'set()'
)
```


## Statements

### Small statements

Here is an example of a few small statements:

```python
from gekkota import Name, SequenceExpr
from gekkota import ReturnStmt, DelStmt, AssertStmt, BreakStmt, ContinueStmt, YieldStmt, YieldFromStmt, NonLocalStmt, GlobalStmt, PassStmt, RaiseStmt, AsyncStmt

a = Name("a")
b = Name("b")


    print(ReturnStmt(a).render_str()) # 'return a'

    print(YieldStmt(a).render_str()) # 'yield a'
    print(YieldFromStmt(b).render_str()) # 'yield from b'
    
    print(DelStmt(a).render_str()) # 'del a'
    
    print(AssertStmt(a).render_str()) # 'assert a'
    
    print(BreakStmt().render_str()) # 'break'
    
    print(ContinueStmt().render_str()) # 'continue'
    
    print(GlobalStmt([a, b]).render_str()) # 'global a, b'
    print(NonLocalStmt([a, b]).render_str()) # 'nonlocal a, b'
    
    print(PassStmt().render_str()) # 'pass'

    print(RaiseStmt().render_str()) # 'raise' 
    print(RaiseStmt(a).render_str()) # 'raise a'
    print(RaiseStmt(a, b).render_str()) # 'raise a from b'

    print(AsyncStmt(a).render_str()) # 'async a'
```


**End of documentation :(**    
You can check out tests for an explanation, check out code or your IDE's code completion.    
This documentation would be filled later, when I would have time and energy for that.    