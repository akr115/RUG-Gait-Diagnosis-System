from flask import Flask, jsonify, request
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
csrf = CSRFProtect(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    try:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"message": f"File {filename} uploaded successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle other exceptions with 500 status code

if __name__ == '__main__':
    app.run(debug=True)
