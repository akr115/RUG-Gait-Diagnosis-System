import sys
from flask import Flask, jsonify, render_template, redirect, url_for, flash, session, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dataProcessing.process_starter import process

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

UPLOAD_FOLDER_C3D = 'uploads/c3d'
UPLOAD_FOLDER_XLSX = 'uploads/xlsx'
FILENAME_C3D = 'Walk.c3d'
FILENAME_XLSX = 'LO.xlsx'
if not os.path.exists(UPLOAD_FOLDER_C3D):
    os.makedirs(UPLOAD_FOLDER_C3D)
if not os.path.exists(UPLOAD_FOLDER_XLSX):
    os.makedirs(UPLOAD_FOLDER_XLSX)

users = {"admin": "password123"}  # In-memory user store

@app.route('/')
def index():
    return 'OK'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username in users and users[username] == password:
        session['username'] = username
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

@app.route('/protected')
def protected():
    if 'username' in session:
        return render_template('protected.html')
    else:
        flash('You need to login first', 'danger')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/upload/c3d', methods=['POST'])
def upload_c3d_files():
    if 'files' not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No selected files"}), 400

    try:
        filenames = []
        for file in files:
            if file and file.filename.endswith('.c3d'):
                filename = secure_filename(FILENAME_C3D)
                file.save(os.path.join(UPLOAD_FOLDER_C3D, filename))
                filenames.append(filename)
        return jsonify({"message": "C3D files uploaded successfully!", "filenames": filenames}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload/xlsx', methods=['POST'])
def upload_xlsx_files():
    if 'files' not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No selected files"}), 400

    try:
        filenames = []
        for file in files:
            if file and file.filename.endswith('.xlsx'):
                filename = secure_filename(FILENAME_XLSX)
                file.save(os.path.join(UPLOAD_FOLDER_XLSX, filename))
                filenames.append(filename)
        return jsonify({"message": "XLSX files uploaded successfully!", "filenames": filenames}), 200
    except Exception as e:
        print("yo")
        return jsonify({"error": str(e)}), 500

    
@app.route('/diagnose', methods=['POST'])
def diagnose_endpoint():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.xlsx'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER_XLSX, filename)
        file.save(filepath)
        # Extract numeric value from request
        file_c3d = os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER_C3D, FILENAME_C3D)
        file_xlsx = os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER_XLSX, FILENAME_XLSX)

        numeric_value = 8
        # numeric_value = request.form.get('numeric_value', type=float)
        # if numeric_value is None:
        #     return jsonify({"error": "No numeric value provided"}), 400

        results, lo = process(numeric_value, file_c3d, file_xlsx)
        results = results.to_json()
        lo = lo.to_json()
        return jsonify(results, lo), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
