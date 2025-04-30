from shamir_ss import generate_text_shares, reconstruct_text_secret


def main():
    secret = "My top secret"
    # secp256k1 prime
    new_prime = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
    shares = generate_text_shares(secret, 3, 5, prime=new_prime, verbose=True)

    reconstructed = reconstruct_text_secret(shares[:3], prime=new_prime, verbose=True)
    print(reconstructed)


if __name__ == "__main__":
    main()
