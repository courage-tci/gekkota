from gekkota import Name, Literal, SliceExpr, Parens, StarArg, DoubleStarArg, CallArg


a = Name("a")
b = Name("b")
c = Name("c")

class TestClass:
    def test_names(self):
        assert a.render_str() == "a"
        assert b.render_str() == "b"

    def test_unop(self):
        assert (-a).render_str() == "-a"
        assert (+a).render_str() == "+a"
        assert (~a).render_str() == "~a"
        assert a.not_().render_str() == "not a"

    def test_binop(self):
        assert (a + b).render_str() == "a + b"
        assert (a - b).render_str() == "a - b"
        assert (a * b).render_str() == "a * b"
        assert (a / b).render_str() == "a / b"
        assert (a // b).render_str() == "a // b"
        assert (a % b).render_str() == "a % b"
        assert (a @ b).render_str() == "a @ b"
        assert (a > b).render_str() == "a > b"
        assert (a < b).render_str() == "a < b"
        assert (a >= b).render_str() == "a >= b"
        assert (a <= b).render_str() == "a <= b"
        assert (a ^ b).render_str() == "a ^ b"
        assert (a | b).render_str() == "a | b"
        assert (a & b).render_str() == "a & b"
        assert (a ** b).render_str() == "a ** b"
        assert (a >> b).render_str() == "a >> b"
        assert (a << b).render_str() == "a << b"
        assert a.or_(b).render_str() == "a or b"
        assert a.and_(b).render_str() == "a and b"
        assert a.in_(b).render_str() == "a in b"
        assert a.not_in(b).render_str() == "a not in b"
        assert a.is_(b).render_str() == "a is b"
        assert a.is_not(b).render_str() == "a is not b"
        assert a.eq(b).render_str() == "a == b"
        assert a.neq(b).render_str() == "a != b"

    def test_priorities(self):
        assert ((a + b) * a).render_str() == "(a + b) * a"
        assert (a * (a + b)).render_str() == "a * (a + b)"
        assert (-(a + b)).render_str() == "-(a + b)"
        assert (a.and_(b)).not_().render_str() == "not (a and b)"
        assert (a << (b << c)).render_str() == "a << (b << c)"
        assert (a >> (b >> c)).render_str() == "a >> (b >> c)"

    def test_attr(self):
        assert a.getattr("b").render_str() == "a.b"
        assert Literal(-1).getattr("b").render_str() == "(-1).b" 
        assert Literal(6.7).getattr("b").render_str() == "(6.7).b" 

    def test_index(self):
        assert a[b].render_str() == "a[b]"
        assert a.index(b).render_str() == "a[b]"
        assert (a + b).index(a).render_str() == "(a + b)[a]"
        
        # slices
        assert a.index(SliceExpr(a, b, c)).render_str() == "a[a:b:c]"
        assert a.index(SliceExpr(a, b)).render_str() == "a[a:b]"
        assert a.index(SliceExpr(a)).render_str() == "a[a:]"
        assert a.index(SliceExpr(stop=b)).render_str() == "a[:b]"
        assert a.index(SliceExpr(step=c)).render_str() == "a[::c]"
        assert a.index([SliceExpr(start=a), SliceExpr(stop=b), SliceExpr(step=c)]).render_str() == "a[a:, :b, ::c]"

        assert a.index(slice(a, b, c)).render_str() == "a[a:b:c]"

    def test_call(self):
        assert a(a, b).render_str() == "a(a, b)"
        assert a(a=b).render_str() == "a(a=b)"
        assert a(**{"a": b, "b": a}).render_str() == "a(a=b, b=a)"

    def test_await(self):
        assert a.await_().render_str() == "await a"
        assert (a.await_()()).render_str() == "(await a)()"
    
    def test_assignment_expr(self):
        assert a.assign(b).render_str() == "a := b"

    def test_parens(self):
        assert Parens(a).render_str() == "(a)"

    def test_args(self):
        assert CallArg("a", b).render_str() == "a=b"

        assert StarArg(a).render_str() == "*a"
        assert DoubleStarArg(a).render_str() == "**a"

        assert StarArg(a + b).render_str() == "*(a + b)"
        assert DoubleStarArg(a + b).render_str() == "**(a + b)"

    def test_compact(self):
        one = Literal(1)
        two = Literal(2)
        half_float = Literal(0.5)

        assert (one + two).render_str(compact=True) == "1+2"
        assert one.and_(two).render_str(compact=True) == "1and 2"
        assert one.and_(half_float).render_str(compact=True) == "1and.5"
        assert (a + b).render_str(compact=True) == "a+b"
        assert a.and_(b).render_str(compact=True) == "a and b"


