#!/usr/bin/env python3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import base64
import pickle
import hashlib
import sys
import tempfile


# Import the Shamir Secret Sharing functions
from shamir_ss import generate_text_shares, reconstruct_text_secret

# Create Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # For flash messages and sessions
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

@app.route('/')
def index():
    """Render the main page with tabs for splitting and combining secrets."""
    return render_template('index.html')

@app.route('/combine')
def combine_page():
    """Render the main page with the combine tab active."""
    return render_template('index.html', active_tab='combine')

@app.route('/split', methods=['POST'])
def split():
    """Split a secret into shares using Shamir's Secret Sharing scheme."""
    secret = request.form.get('secret', '')
    threshold = int(request.form.get('threshold', 2))
    num_shares = int(request.form.get('shares', 3))
    verify = 'verify' in request.form
    
    if not secret:
        flash('Secret cannot be empty', 'error')
        return redirect(url_for('index'))
    
    if threshold > num_shares:
        flash('Threshold must be less than or equal to the number of shares', 'error')
        return redirect(url_for('index'))
    
    try:
        # Calculate the hash of the original secret
        secret_hash = hashlib.sha256(secret.encode()).hexdigest()
        
        # Generate shares
        generated_shares = generate_text_shares(secret, threshold, num_shares)
        
        # Encode shares to base64
        encoded_shares = []
        for share in generated_shares:
            # Serialize the share tuple to bytes
            share_bytes = pickle.dumps(share)
            # Encode to base64
            share_base64 = base64.b64encode(share_bytes).decode('utf-8')
            encoded_shares.append(share_base64)
        
        # Verify by reconstructing (optional)
        verification_result = None
        if verify:
            verification_shares = []
            for encoded_share in encoded_shares[:threshold]:
                share_bytes = base64.b64decode(encoded_share)
                share = pickle.loads(share_bytes)
                verification_shares.append(share)
                
            reconstructed = reconstruct_text_secret(verification_shares)
            verification_result = (reconstructed == secret)
            
        # Store results in session
        session['shares'] = encoded_shares
        session['threshold'] = threshold
        session['secret_hash'] = secret_hash
        session['verification_result'] = verification_result
        
        return render_template(
            'results.html', 
            shares=encoded_shares, 
            threshold=threshold, 
            secret_hash=secret_hash,
            verification_result=verification_result
        )
    
    except Exception as e:
        flash(f'Error generating shares: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/combine', methods=['POST'])
def combine():
    """Reconstruct a secret from shares using Shamir's Secret Sharing scheme."""
    # Handle text input
    if 'shares_text' in request.form and request.form['shares_text'].strip():
        shares_text = request.form['shares_text'].strip()
        original_hash = request.form.get('hash', '')
        
        shares, hash_from_text = parse_shares_from_text(shares_text)
        
        # Use hash from text if provided and no hash from form
        if not original_hash and hash_from_text:
            original_hash = hash_from_text
    
    # Handle file upload
    elif 'shares_file' in request.files and request.files['shares_file'].filename:
        shares_file = request.files['shares_file']
        original_hash = request.form.get('hash', '')
        
        # Save the file temporarily
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'shares.txt')
        shares_file.save(file_path)
        
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read().strip()
        
        # Parse the file content
        shares, hash_from_file = parse_shares_from_text(content)
        
        # Use hash from file if provided and no hash from form
        if not original_hash and hash_from_file:
            original_hash = hash_from_file
        
        # Clean up the temporary file
        os.remove(file_path)
    
    else:
        flash('No shares provided', 'error')
        return redirect(url_for('index'))
    
    if not shares:
        flash('No valid shares found', 'error')
        return redirect(url_for('index'))
    
    try:
        # Reconstruct the secret
        reconstructed_secret = reconstruct_text_secret(shares)
        
        # Calculate the hash of the reconstructed secret
        reconstructed_hash = hashlib.sha256(reconstructed_secret.encode()).hexdigest()
        
        # Check if we have the original hash to verify
        hash_match = None
        if original_hash:
            hash_match = (reconstructed_hash == original_hash)
        
        return render_template(
            'reconstructed.html',
            secret=reconstructed_secret,
            reconstructed_hash=reconstructed_hash,
            original_hash=original_hash,
            hash_match=hash_match
        )
    
    except Exception as e:
        flash(f'Error reconstructing secret: {str(e)}', 'error')
        return redirect(url_for('index'))

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

@app.route('/download_shares')
def download_shares():
    """Create a file with all shares and hash for download."""
    from flask import Response
    
    if 'shares' not in session or 'secret_hash' not in session:
        flash('No shares available to download', 'error')
        return redirect(url_for('index'))
    
    shares = session['shares']
    secret_hash = session['secret_hash']
    
    # Create content
    content = f"Hash: {secret_hash}\n"
    for share in shares:
        content += f"{share}\n"
    
    # Return as a downloadable file
    return Response(
        content,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=all_shares.txt"}
    )

if __name__ == "__main__":
    # Make sure templates directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
    
    # Make sure static/images directory exists for the bow image
    os.makedirs(os.path.join(os.path.dirname(__file__), 'static', 'images'), exist_ok=True)
    
    # Run the app
    app.run(host='0.0.0.0', port=5001)