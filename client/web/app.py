#!/usr/bin/env python3
import os
import json
import sys
import hashlib
import tempfile
import uuid
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file

# Add package to path if necessary
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

try:
    from shamir_ss import generate_text_shares, reconstruct_text_secret
except ImportError:
    try:
        from package.shamir_ss import generate_text_shares, reconstruct_text_secret
    except ImportError:
        print("Error: Could not import shamir_ss package. Please make sure it is installed.")
        sys.exit(1)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', str(uuid.uuid4()))

# Directory to temporarily store shares
TEMP_SHARE_DIR = os.path.join(tempfile.gettempdir(), 'shamir_shares')
os.makedirs(TEMP_SHARE_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/split', methods=['GET', 'POST'])
def split():
    if request.method == 'POST':
        try:
            secret = request.form.get('secret', '')
            threshold = int(request.form.get('threshold', 2))
            shares_count = int(request.form.get('shares', 3))
            
            if not secret:
                flash("Secret cannot be empty", "error")
                return render_template('split.html')
            
            if threshold > shares_count:
                flash("Threshold must be less than or equal to the number of shares", "error")
                return render_template('split.html')
            
            if threshold < 2:
                flash("Threshold must be at least 2", "error")
                return render_template('split.html')
            
            # Calculate hash for verification
            secret_hash = hashlib.sha256(secret.encode()).hexdigest()
            
            # Generate shares
            generated_shares = generate_text_shares(secret, threshold, shares_count)
            
            # Prepare the output
            share_objects = []
            for i, (share_id, share_data) in enumerate(generated_shares):
                share_obj = {
                    "id": share_id,
                    "threshold": threshold,
                    "total_shares": shares_count,
                    "data": share_data,
                    "hash": secret_hash
                }
                share_objects.append(share_obj)
            
            # Store shares in session
            session['shares'] = [json.dumps(obj) for obj in share_objects]
            session['threshold'] = threshold
            
            return redirect(url_for('show_shares'))
        
        except Exception as e:
            flash(f"Error generating shares: {str(e)}", "error")
            return render_template('split.html')
    
    return render_template('split.html')

@app.route('/shares')
def show_shares():
    if 'shares' not in session or not session['shares']:
        flash("No shares available. Split a secret first.", "error")
        return redirect(url_for('split'))
    
    shares = [json.loads(share) for share in session['shares']]
    threshold = session.get('threshold', 2)
    
    return render_template('shares.html', shares=shares, threshold=threshold)

@app.route('/download_share/<int:index>')
def download_share(index):
    if 'shares' not in session or not session['shares']:
        flash("No shares available", "error")
        return redirect(url_for('split'))
    
    if index < 0 or index >= len(session['shares']):
        flash("Invalid share index", "error")
        return redirect(url_for('show_shares'))
    
    share = json.loads(session['shares'][index])
    
    # Create a temporary file
    share_file = os.path.join(TEMP_SHARE_DIR, f"share_{share['id']}_{uuid.uuid4()}.json")
    with open(share_file, 'w') as f:
        json.dump(share, f, indent=2)
    
    return send_file(
        share_file,
        as_attachment=True,
        download_name=f"share_{share['id']}.json",
        mimetype='application/json'
    )

@app.route('/download_all_shares')
def download_all_shares():
    if 'shares' not in session or not session['shares']:
        flash("No shares available", "error")
        return redirect(url_for('split'))
    
    # Create a temporary directory for zip
    import zipfile
    zip_filename = os.path.join(TEMP_SHARE_DIR, f"all_shares_{uuid.uuid4()}.zip")
    
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for i, share_json in enumerate(session['shares']):
            share = json.loads(share_json)
            share_file = os.path.join(TEMP_SHARE_DIR, f"share_{share['id']}.json")
            with open(share_file, 'w') as f:
                json.dump(share, f, indent=2)
            zipf.write(share_file, f"share_{share['id']}.json")
            os.remove(share_file)
    
    return send_file(
        zip_filename,
        as_attachment=True,
        download_name="all_shares.zip",
        mimetype='application/zip'
    )

@app.route('/combine', methods=['GET', 'POST'])
def combine():
    if request.method == 'POST':
        try:
            files = request.files.getlist('share_files')
            
            if not files or all(not f.filename for f in files):
                flash("No share files provided", "error")
                return render_template('combine.html')
            
            # Read shares from the uploaded files
            shares = []
            secret_hash = None
            threshold = None
            
            for file in files:
                if not file.filename:
                    continue
                
                try:
                    share_data = json.loads(file.read().decode('utf-8'))
                    
                    # Validate share format
                    if not all(key in share_data for key in ["id", "data", "threshold", "hash"]):
                        flash(f"Invalid share format in file {file.filename}", "error")
                        continue
                    
                    # Use the first valid hash and threshold
                    if secret_hash is None:
                        secret_hash = share_data["hash"]
                    if threshold is None:
                        threshold = share_data["threshold"]
                    
                    shares.append((share_data["id"], share_data["data"]))
                
                except Exception as e:
                    flash(f"Error reading share from {file.filename}: {str(e)}", "error")
            
            if not shares:
                flash("No valid shares found", "error")
                return render_template('combine.html')
            
            if threshold and len(shares) < threshold:
                flash(f"Not enough shares. Need at least {threshold}, but only have {len(shares)}.", "error")
                return render_template('combine.html')
            
            # Reconstruct the secret
            reconstructed_secret = reconstruct_text_secret(shares)
            
            # Verify the reconstructed secret
            if secret_hash:
                reconstructed_hash = hashlib.sha256(reconstructed_secret.encode()).hexdigest()
                if reconstructed_hash != secret_hash:
                    flash("Warning: The reconstructed secret's hash doesn't match the original!", "warning")
            
            return render_template('result.html', secret=reconstructed_secret)
        
        except Exception as e:
            flash(f"Error reconstructing secret: {str(e)}", "error")
            return render_template('combine.html')
    
    return render_template('combine.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 