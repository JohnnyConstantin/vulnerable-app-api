from flask import Flask, request, render_template_string
import sqlite3
import hashlib
import subprocess
import pickle
import yaml
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-123'
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    
    conn = sqlite3.connect('users.db')
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    
    try:
        result = conn.execute(query).fetchone()
        if result:
            return f"Welcome, {username}!"
        return "Login failed"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/ping')
def ping():
    host = request.args.get('host', '127.0.0.1')
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return f"<pre>{result.decode()}</pre>"
@app.route('/load')
def load():
    data = request.args.get('data', '')
    obj = pickle.loads(data.encode())
    return str(obj)

@app.route('/config')
def config():
    yaml_str = request.args.get('yaml', '')
    config = yaml.load(yaml_str)
    return str(config)
@app.route('/hello')
def hello():
    name = request.args.get('name', 'World')
    template = f"<h1>Hello, {name}!</h1>"
    return render_template_string(template)

@app.route('/hash')
def hash_password():
    password = request.args.get('password', '')
    hashed = hashlib.md5(password.encode()).hexdigest()
    return f"MD5 hash: {hashed}"

@app.route('/read')
def read_file():
    filename = request.args.get('file', '')
    content = open(filename, 'r').read()
    return f"<pre>{content}</pre>"

@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f"<h1>Search results for: {query}</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
