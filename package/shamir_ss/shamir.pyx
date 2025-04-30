import secrets
import functools

_PRIME = 2**127-1
_RINT = functools.partial(secrets.SystemRandom().randint, 0)


def generate_text_shares(text: str, minimum: int, shares: int, prime: int = _PRIME):
    """Generate shares for long text with proper padding"""
    chunks = text_to_chunks(text, prime)

    all_shares = []
    for chunk in chunks:
        chunk_shares = generate_shares(chunk, minimum, shares, prime)
        all_shares.append(chunk_shares)

    return [(i+1, [s[1] for s in [share[i] for share in all_shares]])
            for i in range(shares)]


def reconstruct_text_secret(shares: list, prime: int = _PRIME) -> str:
    """Reconstruct text from shares with padding removal"""
    if not shares:
        raise ValueError("No shares provided")

    num_chunks = len(shares[0][1])
    reconstructed = []

    for chunk_idx in range(num_chunks):
        chunk_shares = [(s[0], s[1][chunk_idx]) for s in shares]
        reconstructed.append(reconstruct_secret(chunk_shares, prime))

    return chunks_to_text(reconstructed, prime)


def bytes_to_chunks(data: bytes, prime: int) -> list:
    """Convert bytes to padded integer chunks"""
    # Calculate chunk size based on prime's bit length
    max_chunk_size = (prime.bit_length() + 7) // 8
    max_chunk_value = 2 ** (8 * max_chunk_size) - 1

    # Verify prime can actually contain the chunks
    if prime > max_chunk_value:
        raise ValueError(f"Prime {prime} too large for {max_chunk_size}-byte chunks")

    # Add length header and padding
    length_header = len(data).to_bytes(8, "big")
    combined = length_header + data

    # PKCS#7 padding
    padding_needed = (-len(combined)) % max_chunk_size
    combined += bytes([padding_needed] * padding_needed)

    chunk_ints = []
    for i in range(0, len(combined), max_chunk_size):
        chunk = combined[i:i+max_chunk_size]
        chunk_int = int.from_bytes(chunk, "big")

        # Final safety check
        if chunk_int >= prime:
            required_bits = chunk_int.bit_length()
            raise ValueError(
                f"Chunk {i//max_chunk_size} requires {required_bits}-bit prime "
                f"(current: {prime.bit_length()} bits)"
            )
        chunk_ints.append(chunk_int)

    return chunk_ints


def chunks_to_bytes(chunk_ints: list, prime: int) -> bytes:
    """Convert chunks back to bytes with padding validation"""
    # Calculate chunk size based on prime's bit length
    max_chunk_size = (prime.bit_length() + 7) // 8
    _max_chunk_value = 2 ** (8 * max_chunk_size) - 1

    # Convert all chunks to bytes first
    try:
        chunk_bytes = [c.to_bytes(max_chunk_size, "big") for c in chunk_ints]
    except OverflowError as e:
        raise ValueError("Invalid chunk value detected") from e

    combined = b"".join(chunk_bytes)

    # Extract length and validate padding
    length = int.from_bytes(combined[:8], "big")
    payload = combined[8:8+length]
    padding = combined[8+length:]

    # Validate PKCS#7 padding
    if padding:
        pad_value = padding[-1]
        if pad_value == 0 or pad_value > len(padding):
            raise ValueError("Invalid padding")
        if padding != bytes([pad_value] * len(padding)):
            raise ValueError("Padding corruption detected")

    return payload


def text_to_chunks(text: str, prime: int, encoding: str = "utf-8") -> list:
    """Helper for text inputs with explicit encoding"""
    return bytes_to_chunks(text.encode(encoding, "ignore"), prime)


def chunks_to_text(chunk_ints: list, prime: int, encoding: str = "utf-8") -> str:
    """Helper for text outputs with explicit encoding"""
    return chunks_to_bytes(chunk_ints, prime).decode(encoding, "ignore")


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

    cdef list poly = [int(secret)]
    cdef object rint = _RINT

    for _ in range(minimum - 1):
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
