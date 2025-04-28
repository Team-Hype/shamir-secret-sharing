# Shamir's Secret Sharing Web Application

This is a web application for Shamir's Secret Sharing, allowing users to split secrets into multiple shares and reconstruct them when a threshold number of shares is available.

## Features

- Split secrets into multiple shares with a customizable threshold
- Download shares individually or as a ZIP file
- Reconstruct secrets by uploading share files
- Security verification through hashing
- Educational information about the algorithm

## Requirements

- Python 3.9 or higher
- Flask and other dependencies listed in `requirements.txt`
- The Shamir's Secret Sharing package (`shamir_ss`)

## Installation

1. Ensure you have Python 3.9+ installed
2. Install the `shamir_ss` package (if not already installed)
3. Install the web application dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

From the project root directory, run:

```bash
python -m client.web.app
```

The application will be available at http://localhost:5000

## Security Considerations

This web application is intended for educational purposes and basic usage. For high-security applications, consider the following:

- Use the CLI version in an isolated environment
- Never enter or reconstruct highly sensitive information on a compromised machine
- Always distribute shares securely to different trusted individuals or locations
- Consider the operational security implications of your threshold settings