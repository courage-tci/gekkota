from gekkota import Name, Literal, SliceExpr, Parens, StarArg, DoubleStarArg, CallArg


a = Name("a")
b = Name("b")
c = Name("c")


class TestClass:
    def test_names(self):
        assert str(a) == "a"
        assert str(b) == "b"

    def test_unop(self):
        assert str(-a) == "-a"
        assert str(+a) == "+a"
        assert str(~a) == "~a"
        assert str(a.not_()) == "not a"

    def test_binop(self):
        assert str(a + b) == "a + b"
        assert str(a - b) == "a - b"
        assert str(a * b) == "a * b"
        assert str(a / b) == "a / b"
        assert str(a // b) == "a // b"
        assert str(a % b) == "a % b"
        assert str(a @ b) == "a @ b"
        assert str(a > b) == "a > b"
        assert str(a < b) == "a < b"
        assert str(a >= b) == "a >= b"
        assert str(a <= b) == "a <= b"
        assert str(a ^ b) == "a ^ b"
        assert str(a | b) == "a | b"
        assert str(a & b) == "a & b"
        assert str(a**b) == "a ** b"
        assert str(a >> b) == "a >> b"
        assert str(a << b) == "a << b"
        assert str(a.or_(b)) == "a or b"
        assert str(a.and_(b)) == "a and b"
        assert str(a.in_(b)) == "a in b"
        assert str(a.not_in(b)) == "a not in b"
        assert str(a.is_(b)) == "a is b"
        assert str(a.is_not(b)) == "a is not b"
        assert str(a.eq(b)) == "a == b"
        assert str(a.neq(b)) == "a != b"

    def test_priorities(self):
        assert str((a + b) * a) == "(a + b) * a"
        assert str(a * (a + b)) == "a * (a + b)"
        assert str(-(a + b)) == "-(a + b)"
        assert str((a.and_(b)).not_()) == "not (a and b)"
        assert str(a << (b << c)) == "a << (b << c)"
        assert str(a >> (b >> c)) == "a >> (b >> c)"
        assert str(a * b * c) == "a * b * c"

    def test_attr(self):
        assert str(a.getattr("b")) == "a.b"
        assert str(Literal(-1).getattr("b")) == "(-1).b"
        assert str(Literal(6.7).getattr("b")) == "(6.7).b"
        assert str(a.getattr("b").getattr("c")) == "a.b.c"

    def test_index(self):
        assert str(a[b]) == "a[b]"
        assert str(a.index(b)) == "a[b]"
        assert str((a + b).index(a)) == "(a + b)[a]"

        # slices
        assert str(a.index(SliceExpr(a, b, c))) == "a[a:b:c]"
        assert str(a.index(SliceExpr(a, b))) == "a[a:b]"
        assert str(a.index(SliceExpr(a))) == "a[a:]"
        assert str(a.index(SliceExpr(stop=b))) == "a[:b]"
        assert str(a.index(SliceExpr(step=c))) == "a[::c]"
        assert (
            str(a.index([SliceExpr(start=a), SliceExpr(stop=b), SliceExpr(step=c)]))
            == "a[a:, :b, ::c]"
        )

        # typechecker is disabled here because slice cannot be used here with a typechecker, check Expression.index for explanation
        assert str(a.index(slice(a, b, c))) == "a[a:b:c]"  # type: ignore

    def test_conditional(self):
        assert str(b.if_(a, c)) == "b if a else c"

    def test_call(self):
        assert str(a(a, b)) == "a(a, b)"
        assert str(a(a=b)) == "a(a=b)"
        assert str(a(**{"a": b, "b": a})) == "a(a=b, b=a)"

    def test_await(self):
        assert str(a.await_()) == "await a"
        assert str(a.await_()()) == "(await a)()"

    def test_assignment_expr(self):
        assert str(a.assign(b)) == "a := b"

    def test_parens(self):
        assert str(Parens(a)) == "(a)"

    def test_args(self):
        assert str(CallArg("a", b)) == "a=b"

        assert str(StarArg(a)) == "*a"
        assert str(DoubleStarArg(a)) == "**a"

        assert str(StarArg(a + b)) == "*(a + b)"
        assert str(DoubleStarArg(a + b)) == "**(a + b)"

    def test_compact(self):
        one = Literal(1)
        two = Literal(2)
        half_float = Literal(0.5)

        assert (one + two).render_str({"compact": True}) == "1+2"
        assert one.and_(two).render_str({"compact": True}) == "1and 2"
        assert one.and_(half_float).render_str({"compact": True}) == "1and.5"
        assert (a + b).render_str({"compact": True}) == "a+b"
        assert a.and_(b).render_str({"compact": True}) == "a and b"
