from shamir_ss import generate_text_shares, reconstruct_text_secret


def test_insufficient_share_3_5():
    text = "Secret will be corrupted during encoding with 2 shares"
    shares = generate_text_shares(text, 3, 5)
    reconstructed = reconstruct_text_secret(shares[:2])
    assert reconstructed != text


def test_insufficient_share_10_10():
    text = "Secret will be corrupted during encoding"
    shares = generate_text_shares(text, 10, 10)
    reconstructed = reconstruct_text_secret(shares[:9])
    assert reconstructed != text


def test_great_treshold():
    try:
        text = "Can not generate shares where minimum > total shares"
        shares = generate_text_shares(text, 11, 10)
        assert not shares
    except ValueError as e:
        assert e
