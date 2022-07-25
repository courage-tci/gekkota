from gekkota import Name, Literal, SliceExpr, Parens, StarArg, DoubleStarArg, CallArg


a = Name("a")
b = Name("b")

class TestClass:
    def test_names(self):
        assert a.render_str() == "a"
        assert b.render_str() == "b"

    def test_unop(self):
        assert (-a).render_str() == "-a"
        assert (+a).render_str() == "+a"
        assert (~a).render_str() == "~a"

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
        assert a.or_(b).render_str() == "a or b"
        assert a.and_(b).render_str() == "a and b"
        assert a.in_(b).render_str() == "a in b"
        assert a.not_in(b).render_str() == "a not in b"
        assert a.is_(b).render_str() == "a is b"
        assert a.is_not(b).render_str() == "a is not b"
        assert a.eq(b).render_str() == "a == b"
        assert a.neq(b).render_str() == "a != b"

    def test_priorities(self):
        assert (a * (a + b)).render_str() == "a * (a + b)"

    def test_attr(self):
        assert a.getattr("b").render_str() == "a.b"
        assert Literal(-1).getattr("b").render_str() == "(-1).b" 
        assert Literal(6.7).getattr("b").render_str() == "(6.7).b" 

    def test_index(self):
        assert a.index(b).render_str() == "a[b]"
        
        # slices
        assert a.index(SliceExpr(b, b, b)).render_str() == "a[b:b:b]"
        assert a.index(SliceExpr(b, b)).render_str() == "a[b:b]"
        assert a.index(SliceExpr(b)).render_str() == "a[b:]"
        assert a.index(SliceExpr(stop=b)).render_str() == "a[:b]"
        assert a.index(SliceExpr(step=b)).render_str() == "a[::b]"

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


