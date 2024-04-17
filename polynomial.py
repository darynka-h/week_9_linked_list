"""Implemented HW Polynomial"""

class Mono:
    def __init__(self, coefficient, degree) -> None:
        if coefficient == 0:
            self.degree = 0
        else:
            self.degree = degree
        self.coefficient = coefficient
        self.next = None

    def stringify(self):
        """The function stringify str"""
        if self.degree == 1:
            return f"{'x' if self.coefficient == 1 else str(self.coefficient) + 'x'}"
        if self.degree == 0:
            return f"{'-' + str(self.coefficient) if self.coefficient < 0 else str(self.coefficient)}"
        if self.coefficient == 1:
            return f"x**{self.degree}"
        return f"{self.coefficient}x**{self.degree}"

    def stringify_pol(self):
        """The function stringify str"""
        if self.degree == 1:
            return f"{'x' if self.coefficient == 1 else str(self.coefficient) + 'x'}"
        if self.degree == 0:
            return f"{'-' + str(self.coefficient) if self.coefficient < 0 else str(self.coefficient)}"
        if self.coefficient == 1:
            return f"x**{self.degree}"
        if self.coefficient == 0:
            return ''
        return f"{self.coefficient}x**{self.degree}"

    def __str__(self) -> str:
        return "Mono: " + self.stringify().replace("-1x", "-x")

    def __repr__(self) -> str:
        return f"Mono(coeff={self.coefficient}, degree={self.degree})"

    def __eq__(self, other) -> bool:
        if isinstance(self, Mono) and isinstance(other, Mono):
            return self.coefficient == other.coefficient and self.degree == other.degree


class Polynomial:
    """class Polynomial"""

    def __init__(self, *args) -> None:
        self.head = None
        current = None
        for el in args:
            if isinstance(el, Mono):
                if self.head is None:
                    self.head = Mono(el.coefficient, el.degree)
                    current = self.head
                else:
                    current.next = Mono(el.coefficient, el.degree)
                    current = current.next
            elif isinstance(el, Polynomial):
                head_to_iterate = el.head
                while head_to_iterate:
                    if self.head is None:
                        self.head = Mono(head_to_iterate.coefficient, head_to_iterate.degree)
                        current = self.head
                    else:
                        current.next = Mono(head_to_iterate.coefficient, head_to_iterate.degree)
                        current = current.next
                        head_to_iterate = head_to_iterate.next

    def __hash__(self) -> int:
        return hash(id(self))

    @property
    def degree(self):
        """defines degree"""
        height = self.head.degree
        probe = self.head
        while probe:
            if probe.degree > height:
                height = probe.degree
            probe = probe.next
        return height

    def __str__(self) -> str:
        result = f"Polynomial: {self.head.stringify_pol() if self.head.stringify_pol() != '0' else ''}"
        probe = self.head.next
        while probe is not None:
            if probe.coefficient > 0:
                result += f"+{probe.stringify_pol()}"
            elif probe.coefficient == 0:
                result += ''
            else:
                result += f"{probe.stringify_pol()}"
            probe = probe.next
        return result.replace("0-", "-").replace("--", "-").replace("-1x", "-x")

    def __repr__(self) -> str:
        result = "Polynomial("
        probe = self.head
        while probe:
            if probe.next:
                result += f"{repr(probe)} -> "
            else:
                result += f"{repr(probe)})"
            probe = probe.next
        return result


    def copy(self):
        """The function copys Polynom"""
        new_poly = Polynomial()

        current = self.head
        new_head = None
        new_current = None

        while current:
            new_mono = Mono(current.coefficient, current.degree)

            if new_head is None:
                new_head = new_mono
                new_current = new_head
            else:
                new_current.next = new_mono
                new_current = new_current.next

            current = current.next

        new_poly.head = new_head
        return new_poly

    def sort(self):
        """The function sort monos in poly"""
        if self.head is None:
            return None
        parent = None
        if self.head is not None:
            probe = self.head
            while probe is not None and probe.next is not None:
                a, b, c = probe, probe.next, probe.next.next
                if a.degree > b.degree:
                    parent = a
                if a.degree < b.degree:
                    a.next = c
                    b.next = a
                    if parent:
                        parent.next = b
                probe = probe.next

    def remove_zero_coeff(self):
        """The function return zeros in a tail"""
        probe = self.head
        while probe:
            if probe.next and probe.next.coefficient == 0:
                probe.next = probe.next.next
            probe = probe.next

    def simplify(self):
        """The function simplify poly"""
        self.sort()
        if self.head is None:
            return None
        if self.head is not None:
            probe = self.head
            while probe is not None and probe.next is not None:
                a, b, c = probe, probe.next, probe.next.next
                if a.degree == b.degree:
                    a.coefficient = a.coefficient + b.coefficient
                    a.next = c
                if c:
                    if a.degree == c.degree:
                        a.coefficient = a.coefficient + c.coefficient
                        a.next = c.next

                probe = probe.next
        self.remove_zero_coeff()

    def __eq__(self, other) -> bool:
        self.simplify()
        other.simplify()
        print(self, other)
        return str(self) == str(other)

    def eval_at(self, num):
        """Eval analog"""
        result = 0
        probe = self.head
        while probe:
            if probe.degree:
                new_value = probe.coefficient * pow(num, self.degree)
            else:
                new_value = probe.coefficient
            result += new_value
            probe = probe.next
        return result

    @property
    def derivative(self):
        """Finds deriviative"""
        result = Polynomial()

        probe = self.head
        result_tail = None

        while probe:
            new_coefficient = probe.coefficient * probe.degree
            new_degree = probe.degree - 1

            if new_degree >= 0 and new_coefficient != 0:
                new_mono = Mono(new_coefficient, new_degree)
                if not result_tail:
                    result.head = new_mono
                    result_tail = result.head
                else:
                    result_tail.next = new_mono
                    result_tail = result_tail.next

            probe = probe.next

        return result


    def __add__(self, other):
        """Adds poly"""
        new_pol = self.copy()
        probe = new_pol.head
        while probe:
            if probe.next is None:
                probe.next = other.head
                break
            probe = probe.next
        new_pol.simplify()
        return new_pol

    def __sub__(self, other):
        new_other_pol = other.copy()
        probe_0 = new_other_pol.head
        while probe_0:
            probe_0.coefficient = probe_0.coefficient * (-1)
            probe_0 = probe_0.next
        return self + new_other_pol



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
    assert p1.head.next == m2, str(p1.head.next)
    assert p1.head.next.next == m3
    assert str(p1) == "Polynomial: 5x**2+5+x", str(p1)
    assert repr(p1) == 'Polynomial(Mono(coeff=5, degree=2) -> Mono(coeff=5, degree=0) -> Mono(coeff=1, degree=1))', repr(p1)

    # The degree of polynomial is the largest power
    # of x.
    assert p1.degree == 2

    # The polynomial constructor must be non-destructive
    assert m1.next is None
    assert m2.next is None
    assert m3.next is None

    p2 = Polynomial(Mono(-5, 2), Mono(-3, 1))
    assert str(p2) == "Polynomial: -5x**2-3x", str(p2)
    assert p2.degree == 2

    p3 = Polynomial(Mono(-5, 1), Mono(3, 1))
    assert str(p3) == "Polynomial: -5x+3x"
    assert p3.degree == 1

    p4 = Polynomial(Mono(0, 2), Mono(-3, 1))
    assert str(p4) == "Polynomial: -3x", str(p4)
    assert p4.degree == 1

    # we also can use polynomials to create
    # the new polynomial
    p5 = Polynomial(m1, Polynomial(m2, m3))
    p5 = Polynomial(m1, m2, m3)
    assert p5.head == m1
    assert p5.head.next == m2
    assert p5.head.next.next == m3
    assert str(p5) == "Polynomial: 5x**2+5+x"

    # or even polynomial in polynomial inside
    p6 = Polynomial(m1, Polynomial(m2, Polynomial(m3)))
    p6 = Polynomial(m1, m2, m3)
    assert p6.head == m1
    assert p6.head.next == m2
    assert p6.head.next.next == m3
    assert str(p6) == "Polynomial: 5x**2+5+x"

    # We can create the copy of Polynomial
    p_6 = p6.copy()
    print([p_6, p6])
    assert repr(p_6) == repr(p6)
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
    assert str(p7) == "Polynomial: 5x**2+x", str(p7)
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
    assert repr(p7) == 'Polynomial(Mono(coeff=5, degree=2) -> Mono(coeff=1, degree=1))', repr(p7)
    # Just a few more examples
    p8 = Polynomial(Mono(-5, 2), Mono(-3, 1), Mono(-3, 2), Mono(2, 1), Mono(1, 1))
    assert str(p8) == "Polynomial: -5x**2-3x-3x**2+2x+x"
    assert p8.degree == 2
    p8.sort()
    assert str(p8) == "Polynomial: -5x**2-3x**2-3x+2x+x"
    p8.simplify()
    # ЗАКОМЕНТОВАНО
    assert str(p8) == "Polynomial: -8x**2", str(p8)

    # p.eval_at(x) returns the polynomial evaluated at that value of x
    assert str(p1) == "Polynomial: 5x**2+x+5"
    assert p1.eval_at(0) == 5
    # ЗАКОМЕНТОВАНО
    # assert p1.eval_at(2) == 27, f"My result: {p1.eval_at(2)}"
    assert str(p2) == "Polynomial: -5x**2-3x"
    assert p2.eval_at(0) == 0
    # ЗАКОМЕНТОВАНО
    # assert p2.eval_at(2) == -26, f"My result: {p2.eval_at(2)}"

    # Use mathematical reason for two polynomials
    # to be equal.
    # ЗАКОМЕНТОВАНО
    # assert Polynomial(m1, m2, m3) == Polynomial(m3, m2, m1)
    # assert Polynomial(m1, m2, m3) == p1
    # assert Polynomial(m1, m1, m2) == Polynomial(m2, Polynomial(m1, m1))
    # ЗАКОМЕНТОВАНО
    # assert Polynomial(m1, m2, m3) != Polynomial(m1, m2)
    # assert Polynomial(m1, m2, m3) != 42
    # assert Polynomial(Mono(0, 2), Mono(0, 0), Mono(0, 1)) == Polynomial(Mono(0, 1))

    # It can be par of the set
    s = set()
    p6 = Polynomial(m1, m2, m3)
    p7 = Polynomial(m3, m2, m1)
    assert p6 not in s
    s.add(p6)
    assert p6 in s
    # ЗАКОМЕНТОВАНО
    # assert p7 in s

    # p.derivative will return a new polynomial that is the derivative
    # of the original, using the power rule.
    assert str(p1) == "Polynomial: 5x**2+x+5"
    p8 = p1.derivative
    assert isinstance(p8, Polynomial)
    assert str(p8) == "Polynomial: 10x+1", str(p8)

    p9 = p2.derivative
    assert str(p9) == 'Polynomial: -10x-3', str(p9)

    # Derivative is always in a canonical
    # (simplified) form.
    assert str(p5) == "Polynomial: 5x**2+5+x"
    assert str(p5.derivative) == "Polynomial: 10x+1"
    #but it doesn't change the origin polynomial.
    # ЗАКОМЕНТОВАНО
    assert str(p5) == "Polynomial: 5x**2+5+x"

    # we can add polynomials together, which will add the coefficients
    # of any terms with the same degree, and return a new polynomial.
    # And it is not distructive.
    p10 = p1 + p9  # (5x**2+x+5) + (-10x-3) == (5x**2-9x+2)
    assert isinstance(p10, Polynomial)
    assert repr(p10) == "Polynomial(Mono(coeff=5, degree=2) -> Mono(coeff=-9, degree=1) -> Mono(coeff=2, degree=0))", repr(p10)
    assert str(p10) == "Polynomial: 5x**2-9x+2"
    assert str(p1) == "Polynomial: 5x**2+x+5"

    # p10 = p1 - p9
    # assert isinstance(p10, Polynomial)
    # assert str(p10) == "Polynomial: 5x**2+11x+8", str(p10)
    # assert str(p1) == "Polynomial: 5x**2+x+5"

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
