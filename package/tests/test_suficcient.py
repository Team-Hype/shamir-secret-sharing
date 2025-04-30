from shamir_ss import generate_text_shares, reconstruct_text_secret


def test_symbol_secret():
    text = "4"
    shares = generate_text_shares(text, 3, 5)
    reconstructed = reconstruct_text_secret(shares[:3])
    assert reconstructed == text


def test_small_secret():
    text = "My top secret"
    shares = generate_text_shares(text, 3, 5)
    reconstructed = reconstruct_text_secret(shares[:3])
    assert reconstructed == text


def test_long_secret():
    text = "My top secret" * 500
    shares = generate_text_shares(text, 3, 5)
    reconstructed = reconstruct_text_secret(shares[:3])
    assert reconstructed == text


def test_huge_secret():
    text = "My top secret" * 10000
    shares = generate_text_shares(text, 5, 5)
    reconstructed = reconstruct_text_secret(shares)
    assert reconstructed == text


def test_10_shares():
    text = "My top secret" * 500
    shares = generate_text_shares(text, 10, 10)
    reconstructed = reconstruct_text_secret(shares)
    assert reconstructed == text


def test_100_shares():
    text = "My top secret" * 500
    shares = generate_text_shares(text, 100, 100)
    reconstructed = reconstruct_text_secret(shares)
    assert reconstructed == text
