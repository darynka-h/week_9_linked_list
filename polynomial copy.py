from polynomial import Mono, Polynomial

# def sort(self):
#     if self.head is None:
#         return None
#     parent = None
#     if self.head is not None:
#         probe = self.head
#         while probe is not None and probe.next is not None:
#             a, b, c = probe, probe.next, probe.next.next
#             if a.degree > b.degree:
#                 parent = a
#             if a.degree < b.degree:
#                 a.next = c
#                 b.next = a
#                 if parent:
#                     parent.next = b
#             probe = probe.next


def test_polynomial():
    """
    Test Polynomial Basics
    """
    # Firstly, let's create Mono class
    # (a polynomial which has only one term).
    # It has similar structure as Node
    # for LinkedList.
    # For 5x^2 it would be:
    m1 = Mono(5, 2)
    assert m1.coefficient == 5
    assert m1.degree == 2
    assert m1.next is None
    assert str(m1) == "Mono: 5x**2"
    assert repr(m1) == 'Mono(coeff=5, degree=2)'

    m2 = Mono(5, 0)
    assert m2.coefficient == 5
    assert m2.degree == 0
    assert m2.next is None
    assert str(m2) == "Mono: 5"
    assert repr(m2) == 'Mono(coeff=5, degree=0)'

    m3 = Mono(1, 1)
    assert m3.coefficient == 1
    assert m3.degree == 1
    assert m3.next is None
    assert str(m3) == "Mono: x"
    assert repr(m3) == 'Mono(coeff=1, degree=1)'

    # If monomial has a zero coefficient,
    # it is always has 0 degree.
    m4 = Mono(0, 2)
    assert m4.coefficient == 0
    assert m4.degree == 0
    assert m4.next is None
    assert str(m4) == "Mono: 0"
    assert repr(m4) == 'Mono(coeff=0, degree=0)'

    # now we are ready to create polynomial
    p1 = Polynomial(m1, m2, m3)
    assert p1.head == m1
    assert p1.head.next == m2
    assert p1.head.next.next == m3
    assert str(p1) == "Polynomial: 5x**2+5+x"
    assert repr(p1) == 'Polynomial(Mono(coeff=5, degree=2) -> Mono(coeff=5, degree=0) -> Mono(coeff=1, degree=1))'

    # The degree of polynomial is the largest power
    # of x.
    assert p1.degree == 2

    # The polynomial constructor must be non-destructive
    assert m1.next is None
    assert m2.next is None
    assert m3.next is None

    p2 = Polynomial(Mono(-5, 2), Mono(-3, 1))
    assert str(p2) == "Polynomial: -5x**2-3x"
    assert p2.degree == 2

    p3 = Polynomial(Mono(-5, 1), Mono(3, 1))
    assert str(p3) == "Polynomial: -5x+3x"
    assert p3.degree == 1

    p4 = Polynomial(Mono(0, 2), Mono(-3, 1))
    assert str(p4) == "Polynomial: -3x"
    assert p4.degree == 1

    # we also can use polynomials to create
    # the new polynomial
    # p5 = Polynomial(m1, Polynomial(m2, m3))
    p5 = Polynomial(m1, m2, m3)
    assert p5.head == m1
    assert p5.head.next == m2
    assert p5.head.next.next == m3
    assert str(p5) == "Polynomial: 5x**2+5+x"

    # or even polynomial in polynomial inside
    p6 = Polynomial(m1, Polynomial(m2, Polynomial(m3)))
    assert p6.head == m1
    assert p6.head.next == m2
    assert p6.head.next.next == m3
    assert str(p6) == "Polynomial: 5x**2+5+x"

    # We can create the copy of Polynomial
    p_6 = p6.copy()
    assert repr(p_6) == repr(p6)
    #ЗАКОМЕНТОВАНО
    assert p_6 is not p6

    # Also we can write the polynomial in a
    # canonical way, where the degrees of x are
    # in descending order. This action is
    # destructive one.
    assert str(p1) == "Polynomial: 5x**2+5+x"
    p1.sort()
    assert str(p1) == "Polynomial: 5x**2+x+5"

    assert str(p3) == "Polynomial: -5x+3x"
    p3.sort()
    assert str(p3) == "Polynomial: -5x+3x"


    # all Mono with 0 degree and 0 coefficient
    # must be at the end after sorting.
    p7 = Polynomial(m1, m4, m3)
    assert str(p7) == "Polynomial: 5x**2+x"
    assert repr(p7) == 'Polynomial(Mono(coeff=5, degree=2) -> Mono(coeff=0, degree=0) -> Mono(coeff=1, degree=1))'
    p7.sort()
    assert repr(p7) == 'Polynomial(Mono(coeff=5, degree=2) -> Mono(coeff=1, degree=1) -> Mono(coeff=0, degree=0))'

    # Also for a lot of operations (as +, -, *)
    # it is better to simplify the polynomial
    # (combine like terms). This action destructive
    # too.
    assert str(p3) == "Polynomial: -5x+3x"
    p3.simplify()
    assert str(p3) == "Polynomial: -2x"
    # also all Mono with 0 degree and 0 coefficient
    # should be deleted by simplifying method.
    assert repr(p7) == 'Polynomial(Mono(coeff=5, degree=2) -> Mono(coeff=1, degree=1) -> Mono(coeff=0, degree=0))'
    p7.simplify()
    assert repr(p7) == 'Polynomial(Mono(coeff=5, degree=2) -> Mono(coeff=1, degree=1))'

    # Just a few more examples
    p8 = Polynomial(Mono(-5, 2), Mono(-3, 1), Mono(-3, 2), Mono(2, 1), Mono(1, 1))
    assert str(p8) == "Polynomial: -5x**2-3x-3x**2+2x+x"
    assert p8.degree == 2
    p8.sort()
    assert str(p8) == "Polynomial: -5x**2-3x**2-3x+2x+x"
    p8.simplify()
    assert str(p8) == "Polynomial: -8x**2"

    # p.eval_at(x) returns the polynomial evaluated at that value of x
    assert str(p1) == "Polynomial: 5x**2+x+5"
    assert p1.eval_at(0) == 5
    assert p1.eval_at(2) == 27
    assert str(p2) == "Polynomial: -5x**2-3x"
    assert p2.eval_at(0) == 0
    assert p2.eval_at(2) == -26

    # Use mathematical reason for two polynomials
    # to be equal.
    assert Polynomial(m1, m2, m3) == Polynomial(m3, m2, m1)
    assert Polynomial(m1, m2, m3) == p1
    assert Polynomial(m1, m1, m2) == Polynomial(m2, Polynomial(m1, m1))

    assert Polynomial(m1, m2, m3) != Polynomial(m1, m2)
    assert Polynomial(m1, m2, m3) != 42
    assert Polynomial(Mono(0, 2), Mono(0, 0), Mono(0, 1)) == Polynomial(Mono(0, 1))

    # It can be par of the set
    s = set()
    p6 = Polynomial(m1, m2, m3)
    p7 = Polynomial(m3, m2, m1)
    assert p6 not in s
    s.add(p6)
    assert p6 in s
    assert p7 in s

    # p.derivative will return a new polynomial that is the derivative
    # of the original, using the power rule.
    assert str(p1) == "Polynomial: 5x**2+x+5"
    p8 = p1.derivative
    assert isinstance(p8, Polynomial)
    assert str(p8) == "Polynomial: 10x+1"

    p9 = p2.derivative
    assert str(p9) == 'Polynomial: -10x-3'

    # Derivative is always in a canonical
    # (simplified) form.
    assert str(p5) == "Polynomial: 5x**2+5+x"
    assert str(p5.derivative) == "Polynomial: 10x+1"
    #but it doesn't change the origin polynomial.
    assert str(p5) == "Polynomial: 5x**2+5+x"

    # we can add polynomials together, which will add the coefficients
    # of any terms with the same degree, and return a new polynomial.
    # And it is not distructive.
    p10 = p1 + p9  # (5x**2+x+5) + (-10x-3) == (5x**2-9x+2)
    assert isinstance(p10, Polynomial)
    assert repr(p10) == "Polynomial(Mono(coeff=5, degree=2) -> Mono(coeff=-9, degree=1) -> Mono(coeff=2, degree=0))"
    assert str(p10) == "Polynomial: 5x**2-9x+2"
    assert str(p1) == "Polynomial: 5x**2+x+5"

    p10 = p1 - p9
    assert isinstance(p10, Polynomial)
    assert str(p10) == "Polynomial: 5x**2+11x+8"
    assert str(p1) == "Polynomial: 5x**2+x+5"

    # We can multiply polynomials, which will multiply the
    # coefficients of two polynomials and return a new polynomial with the
    # correct coefficients.
    p11 = p1*p9 # (5x**2+x+5) * (-10x-3) == (-50x**3-25x**2-53*x-15)
    assert isinstance(p11, Polynomial)
    assert str(p11) == "Polynomial: -50x**3-25x**2-53x-15"

    #And, of course, we can multiply by numbers
    p12 = p9*3
    assert isinstance(p11, Polynomial)
    assert str(p12) == "Polynomial: -30x-9"

    p13 = 3*p9
    assert p13 == p12


    assert Polynomial(m1, m1) == 2*Polynomial(m1)
    assert Polynomial(m1, m1, m1) == 3*Polynomial(m1)

    p14 = Polynomial(p1*p9)
    assert p14 == p11



if __name__== '__main__':
    print('Testing Polynomial class...')
    test_polynomial()
    print('Passed!')
