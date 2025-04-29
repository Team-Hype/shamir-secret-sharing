#!/usr/bin/env python3
import os
import json
import sys
import click
from typing import Optional
import hashlib
from .shamir import generate_text_shares, reconstruct_text_secret


@click.group()
def cli():
    """Shamir's Secret Sharing CLI.

    This CLI allows you to split a secret into multiple shares and reconstruct it
    when a minimum number of shares are available.
    """
    pass


@cli.command("split")
@click.option(
    "--secret",
    "-s",
    type=str,
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="The secret text to be split into shares.",
)
@click.option(
    "--threshold",
    "-t",
    type=click.IntRange(2, 100),
    required=True,
    help="Minimum number of shares required to reconstruct the secret.",
)
@click.option(
    "--shares",
    "-n",
    type=click.IntRange(2, 100),
    required=True,
    help="Total number of shares to generate.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=True, file_okay=False),
    help="Directory to save shares as individual files. If not provided, shares will be displayed.",
)
@click.option(
    "--verify/--no-verify",
    default=True,
    help="Verify generated shares by reconstructing the secret.",
)
def split(
    secret: str, threshold: int, shares: int, output: Optional[str], verify: bool
):
    """Split a secret into multiple shares using Shamir's Secret Sharing scheme."""
    if threshold > shares:
        click.echo(
            "Error: Threshold must be less than or equal to the number of shares.",
            err=True,
        )
        sys.exit(1)

    # Calculate hash of the original secret for verification
    secret_hash = hashlib.sha256(secret.encode()).hexdigest()

    try:
        # Generate shares
        generated_shares = generate_text_shares(secret, threshold, shares)

        # Prepare the output
        result_shares = []
        for idx, (share_id, share_data) in enumerate(generated_shares):
            share_obj = {
                "id": share_id,
                "threshold": threshold,
                "total_shares": shares,
                "data": share_data,
                "hash": secret_hash,  # Include the hash for verification
            }
            result_shares.append(share_obj)

        # Verify by reconstructing (optional)
        if verify:
            # Use the minimum number of shares to verify
            verification_shares = [
                (s["id"], s["data"]) for s in result_shares[:threshold]
            ]
            reconstructed = reconstruct_text_secret(verification_shares)

            reconstructed_hash = hashlib.sha256(reconstructed.encode()).hexdigest()
            if reconstructed_hash != secret_hash:
                click.echo(
                    "Error: Verification failed! The reconstructed secret doesn't match the original.",
                    err=True,
                )
                sys.exit(1)
            click.echo(f"✅ Verification successful with {threshold} shares.")

        # Output handling
        if output:
            # Ensure the output directory exists
            os.makedirs(output, exist_ok=True)

            for i, share in enumerate(result_shares):
                filename = os.path.join(output, f"share_{share['id']}.json")
                with open(filename, "w") as f:
                    json.dump(share, f, indent=2)

            click.echo(
                f"✅ Generated {shares} shares (threshold: {threshold}) and saved to {output}/"
            )
        else:
            # Display shares
            click.echo(f"✅ Generated {shares} shares (threshold: {threshold}):")
            for i, share in enumerate(result_shares):
                click.echo(f"\nShare {share['id']}:")
                click.echo(json.dumps(share, indent=2))

    except Exception as e:
        click.echo(f"Error generating shares: {str(e)}", err=True)
        sys.exit(1)


@cli.command("combine")
@click.argument(
    "share_files",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    required=False,
)
@click.option(
    "--input-dir",
    "-i",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory containing share files.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    help="File to save the reconstructed secret. If not provided, the secret will be displayed.",
)
@click.option(
    "--verify/--no-verify",
    default=True,
    help="Verify the reconstructed secret against the hash.",
)
def combine(share_files, input_dir, output, verify):
    """Reconstruct a secret from shares using Shamir's Secret Sharing scheme."""

    files_to_read = list(share_files)

    # If input directory is provided, read all JSON files from it
    if input_dir:
        for filename in os.listdir(input_dir):
            if filename.endswith(".json"):
                files_to_read.append(os.path.join(input_dir, filename))

    if not files_to_read:
        click.echo(
            "Error: No share files provided. Use 'share_files' arguments or --input-dir option.",
            err=True,
        )
        sys.exit(1)

    # Read shares from files
    shares = []
    secret_hash = None
    threshold = None

    for file_path in files_to_read:
        try:
            with open(file_path, "r") as f:
                share = json.load(f)

            # Validate share format
            if not all(key in share for key in ["id", "data", "threshold", "hash"]):
                click.echo(f"Error: Invalid share format in file {file_path}", err=True)
                continue

            # Use the first valid hash and threshold we find
            if secret_hash is None:
                secret_hash = share["hash"]
            if threshold is None:
                threshold = share["threshold"]

            shares.append((share["id"], share["data"]))

        except Exception as e:
            click.echo(f"Error reading share from {file_path}: {str(e)}", err=True)

    if not shares:
        click.echo("Error: No valid shares found.", err=True)
        sys.exit(1)

    if len(shares) < threshold:
        click.echo(
            f"Error: Not enough shares. Need at least {threshold}, but only have {len(shares)}.",
            err=True,
        )
        sys.exit(1)

    # Reconstruct the secret
    try:
        reconstructed_secret = reconstruct_text_secret(shares)

        # Verify the reconstructed secret
        if verify and secret_hash:
            reconstructed_hash = hashlib.sha256(
                reconstructed_secret.encode()
            ).hexdigest()
            if reconstructed_hash != secret_hash:
                click.echo(
                    "⚠️ Warning: The reconstructed secret's hash doesn't match the original!",
                    err=True,
                )
            else:
                click.echo("✅ Secret successfully reconstructed and verified.")
        else:
            click.echo("✅ Secret successfully reconstructed.")

        # Output handling
        if output:
            with open(output, "w") as f:
                f.write(reconstructed_secret)
            click.echo(f"Secret saved to {output}")
        else:
            click.echo("\nReconstructed Secret:")
            click.echo("-------------------")
            click.echo(reconstructed_secret)
            click.echo("-------------------")

    except Exception as e:
        click.echo(f"Error reconstructing secret: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
