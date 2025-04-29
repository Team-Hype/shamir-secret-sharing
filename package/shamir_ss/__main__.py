#!/usr/bin/env python3
import os
import sys
import click
from typing import Optional
import hashlib
import base64
import pickle
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
    confirmation_prompt=False,
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

    # Calculate the hash of the original secret
    secret_hash = hashlib.sha256(secret.encode()).hexdigest()

    try:
        # Generate shares
        generated_shares = generate_text_shares(secret, threshold, shares)

        # Encode shares to base64
        encoded_shares = []
        for share in generated_shares:
            # Serialize the share tuple to bytes
            share_bytes = pickle.dumps(share)
            # Encode to base64
            share_base64 = base64.b64encode(share_bytes).decode('utf-8')
            encoded_shares.append(share_base64)

        # Verify by reconstructing (optional)
        if verify:
            # Use the minimum number of shares to verify
            # First decode back from base64
            verification_shares = []
            for encoded_share in encoded_shares[:threshold]:
                share_bytes = base64.b64decode(encoded_share)
                share = pickle.loads(share_bytes)
                verification_shares.append(share)
                
            reconstructed = reconstruct_text_secret(verification_shares)

            if reconstructed != secret:
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

            # Create a single file with all shares and the hash
            all_shares_file = os.path.join(output, "all_shares.txt")
            with open(all_shares_file, "w") as f:
                # Write the hash at the top of the file
                f.write(f"Hash: {secret_hash}\n")
                for share_base64 in encoded_shares:
                    f.write(f"{share_base64}\n")
            
            click.echo(
                f"✅ Generated {shares} shares (threshold: {threshold}) and saved to {output}/all_shares.txt"
            )
        else:
            # Display shares
            click.echo(f"✅ Generated {shares} shares (threshold: {threshold}):")
            for share_base64 in encoded_shares:
                click.echo(share_base64)
        
        # Display hash at the end
        click.echo(f"\nOriginal secret hash: {secret_hash}")
        click.echo("Keep this hash to verify your secret when reconstructing.")

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
    "--text",
    "-t",
    is_flag=True,
    help="Enter shares as text instead of from files. Will prompt for input.",
)
@click.option(
    "--hash",
    "-h",
    type=str,
    help="Hash to verify the reconstructed secret against.",
)
def combine(share_files, input_dir, output, text, hash):
    """Reconstruct a secret from shares using Shamir's Secret Sharing scheme."""

    # Parse shares from various inputs
    shares = []
    original_hash = hash  # Use the hash provided via command line if any
    
    # Option 1: Direct text input
    if text:
        click.echo("Enter your shares, one per line. Press Ctrl+D (or Ctrl+Z on Windows) when finished:")
        share_text = sys.stdin.read().strip()
        shares, file_hash = parse_shares_from_text(share_text)
        # Use hash from file if provided and no hash from command line
        if original_hash is None and file_hash is not None:
            original_hash = file_hash
    
    # Option 2: Read from files
    else:
        files_to_read = list(share_files)

        # If input directory is provided, read all share files from it
        if input_dir:
            for filename in os.listdir(input_dir):
                if filename.endswith(".txt"):
                    files_to_read.append(os.path.join(input_dir, filename))

        if not files_to_read:
            click.echo(
                "Error: No share files provided. Use 'share_files' arguments, --input-dir option, or --text flag.",
                err=True,
            )
            sys.exit(1)

        # Read shares from files
        for file_path in files_to_read:
            try:
                with open(file_path, "r") as f:
                    content = f.read().strip()
                
                # Parse the file content
                file_shares, file_hash = parse_shares_from_text(content)
                
                # Add the shares we found
                shares.extend(file_shares)
                
                # Use the first hash we find from files if no hash from command line
                if original_hash is None and file_hash is not None:
                    original_hash = file_hash

            except Exception as e:
                click.echo(f"Error reading share from {file_path}: {str(e)}", err=True)

    if not shares:
        click.echo("Error: No valid shares found.", err=True)
        sys.exit(1)

    # If no hash was provided or found, ask the user if they want to enter one
    if original_hash is None:
        if click.confirm("No hash was found. Would you like to enter a hash to verify the reconstructed secret?"):
            original_hash = click.prompt("Enter the hash of the original secret")

    # Reconstruct the secret
    try:
        reconstructed_secret = reconstruct_text_secret(shares)
        
        # Calculate the hash of the reconstructed secret
        reconstructed_hash = hashlib.sha256(reconstructed_secret.encode()).hexdigest()

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
        
        # Display hash information at the end
        click.echo("\nHash Information:")
        click.echo("-------------------")
        click.echo(f"Reconstructed secret hash: {reconstructed_hash}")
        
        # Check if we have the original hash to verify
        if original_hash:
            click.echo(f"Original secret hash: {original_hash}")
            if reconstructed_hash == original_hash:
                click.echo("✅ Hash verification successful! The reconstructed secret matches the original.")
            else:
                click.echo("⚠️ Hash verification failed! The reconstructed secret doesn't match the original.", err=True)
        else:
            click.echo("⚠️ No original hash was provided for verification.")

    except Exception as e:
        click.echo(f"Error reconstructing secret: {str(e)}", err=True)
        sys.exit(1)


def parse_shares_from_text(text):
    """Parse shares from text input, supporting base64-encoded shares."""
    shares = []
    original_hash = None
    
    # Split the text into lines
    lines = text.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for hash line
        if line.startswith("Hash:"):
            try:
                original_hash = line.split(":", 1)[1].strip()
                continue
            except:
                pass
        
        # Try different formats
        try:
            # First attempt to parse as base64
            try:
                # This handles our base64-encoded pickled tuples
                share_bytes = base64.b64decode(line)
                share = pickle.loads(share_bytes)
                if isinstance(share, tuple) and len(share) == 2:
                    share_id, share_data = share
                    if isinstance(share_id, int) and isinstance(share_data, list):
                        shares.append((share_id, share_data))
                        continue
            except:
                pass
                
            # Fallback to raw tuple format
            if (line.startswith("(") and line.endswith(")")) or "," in line:
                share = eval(line, {"__builtins__": {}}, {})
                if isinstance(share, tuple) and len(share) == 2:
                    share_id, share_data = share
                    if isinstance(share_id, int) and isinstance(share_data, list):
                        shares.append((share_id, share_data))
                continue
                
            # Last resort: Check for ID:DATA format
            if ":" in line:
                parts = line.split(":", 1)
                share_id = int(parts[0].strip())
                data_str = parts[1].strip()
                
                # Parse the data
                if data_str.startswith("[") and data_str.endswith("]"):
                    share_data = eval(data_str, {"__builtins__": {}}, {})
                    shares.append((share_id, share_data))
                    
        except Exception:
            # Skip lines we can't parse
            continue
    
    return shares, original_hash


@cli.command("help")
def help_command():
    """Display help information and usage examples for all commands."""
    click.echo("\nShamir's Secret Sharing - Usage Examples")
    click.echo("=====================================\n")
    
    click.echo("Split a secret into shares:")
    click.echo("---------------------------")
    click.echo("shamir-ss split -t 3 -n 5")
    click.echo("  - Splits a secret into 5 shares where any 3 can reconstruct it")
    click.echo("  - You will be prompted to enter the secret\n")
    
    click.echo("shamir-ss split -t 3 -n 5 -s \"My secret message\"")
    click.echo("  - Splits the specified secret text into 5 shares where any 3 can reconstruct it\n")
    
    click.echo("shamir-ss split -t 3 -n 5 -o ./shares")
    click.echo("  - Splits a secret and saves shares to the ./shares directory\n")
    
    click.echo("Combine shares to reconstruct a secret:")
    click.echo("--------------------------------------")
    click.echo("shamir-ss combine share_1.txt share_2.txt share_3.txt")
    click.echo("  - Combines the specified share files to reconstruct the secret\n")
    
    click.echo("shamir-ss combine all_shares.txt")
    click.echo("  - Reads all shares from a single file (one share per line)\n")
    
    click.echo("shamir-ss combine -i ./shares")
    click.echo("  - Reads all share files from the ./shares directory and reconstructs the secret\n")
    
    click.echo("shamir-ss combine -t")
    click.echo("  - Prompts you to enter shares directly by pasting them\n")
    
    click.echo("shamir-ss combine -h HASH")
    click.echo("  - Verifies the reconstructed secret against the provided hash\n")
    
    click.echo("shamir-ss combine share_1.txt share_2.txt -o recovered_secret.txt")
    click.echo("  - Combines shares and saves the reconstructed secret to a file\n")


# Register commands with the CLI group
cli.add_command(split)
cli.add_command(combine)
cli.add_command(help_command)

if __name__ == "__main__":
    cli()
