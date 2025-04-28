from shamir_ss import generate_text_shares, reconstruct_text_secret


def test_symbol_secret():
    text = "4"
    shares = generate_text_shares(text, 3, 5)
    reconstructed = reconstruct_text_secret(shares[:3])
    assert reconstructed == text


def test_small_secret():
    text = "Hello World!"
    shares = generate_text_shares(text, 3, 5)
    reconstructed = reconstruct_text_secret(shares[:3])
    assert reconstructed == text


def test_long_secret():
    text = "Hello World!" * 500
    shares = generate_text_shares(text, 3, 5)
    reconstructed = reconstruct_text_secret(shares[:3])
    assert reconstructed == text
