![Tests](https://github.com/Team-Hype/shamir-secret-sharing/actions/workflows/package-test.yaml/badge.svg)
![PYPI](https://img.shields.io/pypi/v/shamir_ss.svg)
![versions](https://img.shields.io/pypi/pyversions/shamir_ss.svg)

# Shamir Secret Sharing (SSS)

Secure cryptographic implementation of Shamir's Secret Sharing scheme for splitting secrets into multiple shares. Designed for both short secrets and large text/data with automatic chunking.

## Features

- 🔒 Cryptographic security using Mersenne prime modulus (2¹²⁷-1)
- 📦 CLI interface and Python API
- ✨ Automatic chunking for large secrets
- 🚀 Cython-optimized core implementation
- ✅ Hash-based secret integrity verification

## Installation

```bash
pip install shamir_ss
```
## Development

For developement see following [guide](development.md)

## Python API

### Example
```python
from shamir_ss import generate_text_shares, reconstruct_text_secret

def main():
    secret = "My top secret"

    shares = generate_text_shares(secret, 3, 5)

    reconstructed = reconstruct_text_secret(shares[:3])
    print(reconstructed)

if __name__ == "__main__":
    main()

```

## CLI Application
### Features

 - 🔐 Interactive secret input with hidden typing
 - 📁 Multiple input formats (files/directories/text)
 - 🛡️ SHA-256 hash verification
 - 🔄 Automatic share validation

### Usage
```bash
python -m shamir_ss <command> <...args>
```
### Command list
```bash
shamir_ss --help         # Show all commands
shamir_ss split --help   # Split command help
shamir_ss combine --help # Combine command help
shamir_ss help           # Detailed usage examples
```

### Examples

```bash
python -m shamir_ss split \
  --secret "My top secret" \
  -t 3 -n 5 \
  --output shares
```
> Split secret to 5 shares with treshold 3 and put output to shares dir


```bash
python -m shamir_ss combine \
  -i shares
```
> Reconstruct secret from shares dir w/o hash validation (will be prompted interactively)


```bash
shamir_ss combine --text
```
> Reconstruct secret using interactive mode
