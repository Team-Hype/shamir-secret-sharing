import secrets
import functools

cdef object _PRIME = (2 ** 127 - 1)
cdef object _RINT = functools.partial(secrets.SystemRandom().randint, 0)


cdef object _eval_at(list poly, object x, object prime):
    cdef object accum = 0
    cdef Py_ssize_t i
    cdef object coeff

    for i in reversed(range(len(poly))):
        coeff = poly[i]
        accum = (accum * x) + coeff
        accum %= prime
    return accum

cdef tuple _extended_gcd(object a, object b):
    cdef object x = 0
    cdef object last_x = 1
    cdef object y = 1
    cdef object last_y = 0
    cdef object quot

    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y

    return (last_x, last_y)

cdef object _divmod(object num, object den, object p):

    cdef object inv, _
    inv, _ = _extended_gcd(den, p)
    return (num * inv) % p

cdef object _lagrange_interpolate(object x, list x_s, list y_s, object p):
    cdef int k = len(x_s)
    cdef object cur, num, den, val
    cdef list nums = [], dens = []

    if k != len(set(x_s)):
        raise ValueError("points must be distinct")

    for i in range(k):
        cur = x_s[i]
        others = x_s[:i] + x_s[i+1:]

        num = 1
        for val in others:
            num *= (x - val)
        nums.append(num)

        den = 1
        for val in others:
            den *= (cur - val)
        dens.append(den)

    cdef object total_den = 1
    for den in dens:
        total_den *= den

    cdef object total_num = 0
    for i in range(k):
        numerator = (nums[i] * total_den * y_s[i]) % p
        term = _divmod(numerator, dens[i], p)
        total_num = (total_num + term) % p

    return _divmod(total_num, total_den, p) % p


def generate_shares(object secret, int minimum, int shares, object prime=_PRIME):
    if minimum > shares:
        raise ValueError("Pool secret would be irrecoverable.")

    cdef list poly = [secret]
    cdef int i
    cdef object rint = _RINT

    for i in range(minimum - 1):
        poly.append(rint(prime - 1))

    cdef list points = [
        (i, _eval_at(poly, i, prime))
        for i in range(1, shares + 1)
    ]

    return points


def reconstruct_secret(list shares, object prime=_PRIME):

    cdef list x_s = [s[0] for s in shares]
    cdef list y_s = [s[1] for s in shares]

    return _lagrange_interpolate(0, x_s, y_s, prime)
