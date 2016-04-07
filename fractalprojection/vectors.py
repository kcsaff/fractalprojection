from numbers import Number
from types import GeneratorType
import math


def norm(vector, power=2):
    return math.fsum(abs(a)**power for a in vector)**(1/power)


def normalized(vector, power=2, cls=None):
    if isinstance(vector, GeneratorType):
        vector = tuple(vector)
    cls = cls or type(vector)
    n = norm(vector, power)
    if n == 1:
        return vector
    else:
        return truediv(vector, n, cls=cls)


def dot(first, second):
    return math.fsum(a*b for a, b in zip(first, second))


def cross(a, b, cls=None):
    if isinstance(a, GeneratorType):
        a = tuple(a)
    cls = cls or type(a)
    if len(a) == len(b) == 3:
        return cls((
            a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0],
        ))
    else:
        raise TypeError('Can only cross vectors of length 3, not {!r} X {!r}'.format(a, b))


# Basic maths


def add(*items, cls=None):
    vector = items[0]
    cls = cls or (type(vector) if not isinstance(vector, GeneratorType) else tuple)
    if len(items) == 1:
        return items[0]
    elif len(items) == 2:  # Optimized route
        first, second = items
        if len(first) == len(second):
            return cls(
                a+b for a, b in zip(first, second)
            )
        else:
            raise TypeError('Can only add vectors of equal length, not {!r} + {!r}'.format(first, second))
    else:
        length = len(items[0])
        if all(len(item) == length for item in items):
            return cls(
                math.fsum(parts) for parts in zip(*items)
            )
        else:
            raise TypeError('Can only sum vectors of equal length')


def sub(vector, second, cls=None):
    if isinstance(vector, GeneratorType):
        vector = tuple(vector)
    cls = cls or type(vector)
    if len(vector) == len(second):
        return cls((
            a-b for a, b in zip(vector, second)
        ))
    else:
        raise TypeError('Can only subtract vectors of equal length, not {!r} - {!r}'.format(vector, second))


def mul(vector, scalar, cls=None):
    if isinstance(vector, GeneratorType):
        vector = tuple(vector)
    cls = cls or type(vector)
    if isinstance(scalar, Number):
        return cls(a*scalar for a in vector)
    elif isinstance(vector, Number):
        return mul(scalar, vector)
    else:
        raise TypeError('Can only multiply {!r} by a scalar, not {!r}'.format(vector, scalar))


def truediv(vector, scalar, cls=None):
    if isinstance(vector, GeneratorType):
        vector = tuple(vector)
    cls = cls or type(vector)
    if isinstance(scalar, Number):
        return cls(a/scalar for a in vector)
    else:
        raise TypeError('Can only divide {!r} by a scalar, not {!r}'.format(vector, scalar))


def floordiv(vector, scalar, cls=None):
    if isinstance(vector, GeneratorType):
        vector = tuple(vector)
    cls = cls or type(vector)
    if isinstance(scalar, Number):
        return cls(int(a//scalar) for a in vector)
    else:
        raise TypeError('Can only divide {!r} by a scalar, not {!r}'.format(vector, scalar))


# Derived maths


def truemean(items, cls=None):
    if isinstance(items, GeneratorType):
        items = tuple(items)
    result = add(*items, cls=cls)
    return truediv(result, len(items))


def floormean(items, cls=None):
    if isinstance(items, GeneratorType):
        items = tuple(items)
    return floordiv(add(*items, cls=cls), len(items), cls=cls)


def VectorClass(wrap=tuple):
    wrap_arg = wrap

    class VectorClassImpl(object):
        wrap = wrap_arg
        
        __slots__ = ['__coords']

        def __init__(self, coords):
            self.__coords = self.wrap(coords)

        def __repr__(self):
            return '{}({})'.format(type(self).__name__, tuple(self.__coords))

        # Sequence ops
        def __len__(self):
            return len(self.__coords)

        def __iter__(self):
            return iter(self.__coords)

        def __getitem__(self, item):
            return self.__coords[item]

        # Math ops
        def __pos__(self):
            return self * +1

        def __neg__(self):
            return self * -1

        def __add__(self, other):
            return add(self, other, cls=type(self))

        def __radd__(self, other):
            return add(self, other, cls=type(self))

        def __sub__(self, other):
            return sub(self, other, cls=type(self))

        def __rsub__(self, other):
            return sub(other, self, cls=type(self))

        def __mul__(self, scalar):
            return mul(self, scalar, cls=type(self))

        def __rmul__(self, scalar):
            return mul(self, scalar, cls=type(self))

        def __truediv__(self, scalar):
            return truediv(self, scalar, cls=type(self))

        def __mod__(self, other):
            return type(self)(a % b for a, b in zip(self, other))

        def __rmod__(self, other):
            return type(self)(b % a for a, b in zip(self, other))

        # Equality & hashing

        def __hash__(self):
            return hash(tuple(self.__coords))

        def __eq__(self, other):
            try:
                return len(self) == len(other) and all(a == b for a, b in zip(self, other))
            except TypeError:
                return False

        def __ne__(self, other):
            return not self.__eq__(other)

        # Simple conversions
        def __abs__(self):
            return norm(self, 2.0)

        def __complex__(self):
            if len(self) == 2:
                return self[0] + 1j * self[1]
            elif len(self) == 1:
                return self[0] + 0j
            else:
                raise TypeError('Can only convert length 2 vectors to complex')

    return VectorClassImpl
