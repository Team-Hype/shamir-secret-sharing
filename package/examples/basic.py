from shamir_ss import generate_text_shares, reconstruct_text_secret


def main():
    secret = "My top secret"

    shares = generate_text_shares(secret, 3, 5)

    reconstructed = reconstruct_text_secret(shares[:3])
    print(reconstructed)


if __name__ == "__main__":
    main()
