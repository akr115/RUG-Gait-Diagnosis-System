from flask import Flask, jsonify, render_template, redirect, url_for, flash, session
from forms import LoginForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app)

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
            # flash('Login successful', 'success')
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

if __name__ == '__main__':
    app.run(debug=True)
