# Cython declarations with docstrings

cdef int _PRIME = 2**127 -1


cdef object _eval_at(list poly, object x, object prime):
    """Evaluate polynomial at x using Horner's method modulo prime.

    Args:
        poly: List of polynomial coefficients (constant term first)
        x: Point at which to evaluate polynomial
        prime: Modulus

    Returns:
        Evaluated result modulo prime
    """

cdef tuple _extended_gcd(object a, object b):
    """Extended Euclidean Algorithm finding Bezout coefficients.

    Args:
        a: First integer
        b: Second integer

    Returns:
        Tuple (x, y) such that ax + by = gcd(a, b)
    """

cdef object _divmod(object num, object den, object p):
    """Perform modular division (num * den⁻¹ mod p).

    Args:
        num: Numerator
        den: Denominator
        p: Prime modulus

    Returns:
        Result of division in modular arithmetic

    Raises:
        ValueError: If denominator has no inverse modulo p
    """

cdef object _lagrange_interpolate(object x, list x_s, list y_s, object p):
    """Perform Lagrange interpolation in finite field to find y(0).

    Args:
        x: x-value to interpolate (typically 0 for secret)
        x_s: List of x-coordinates of shares
        y_s: List of y-coordinates of shares
        p: Prime modulus

    Returns:
        Interpolated secret value at x=0

    Raises:
        ValueError: If duplicate x-coordinates are provided
    """

cpdef list generate_shares(object secret, int minimum, int shares, object prime=_PRIME):
    """Generate Shamir secret shares using random polynomial coefficients.

    Args:
        secret: Integer secret to split
        minimum: Minimum shares required for reconstruction
        shares: Total number of shares to generate
        prime: Prime modulus

    Returns:
        List of (x, y) share tuples
    """

cpdef object reconstruct_secret(list shares, object prime=_PRIME):
    """Recover secret using Lagrange interpolation over finite field.

    Args:
        shares: List of (x, y) share tuples
        prime: Prime modulus used during generation

    Returns:
        Reconstructed secret integer

    Raises:
        ValueError: If insufficient shares or invalid input
    """
