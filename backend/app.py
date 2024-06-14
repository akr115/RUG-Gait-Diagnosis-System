from flask import Flask, jsonify, render_template, redirect, url_for, flash, session, request
from forms import LoginForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
# csrf = CSRFProtect(app)

# CORS configuration
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory user store (for demonstration purposes)
users = {"admin": "password123"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('protected'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/protected')
def protected():
    if 'username' in session:
        return render_template('protected.html')
    else:
        flash('You need to login first', 'danger')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/api/data')
def get_data():
    if 'username' in session:
        data = {
            "message": "Hello, World!",
            "items": [1, 2, 3, 4, 5]
        }
        return jsonify(data)
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route('/upload', methods=['POST'])
def upload_files():
    print("here")
    if 'files' not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No selected files"}), 400

    try:
        filenames = []
        for file in files:
            if file and (file.filename.endswith('.c3d') or file.filename.endswith('.xlsx')):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)
        return jsonify({"message": "Files uploaded successfully!", "filenames": filenames}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle other exceptions with 500 status code

if __name__ == '__main__':
    app.run(debug=True)
