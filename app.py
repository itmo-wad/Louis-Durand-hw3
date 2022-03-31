from flask import Flask, flash, render_template, request, url_for, redirect, make_response
from pymongo import MongoClient
import os.path
import random
import hashlib

# Upload folder for pictures and extensions
UPLOAD_FOLDER = "static/pictures"
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png"])
PASSWORD_HASH = "pgWTs7h25g8L5BH"

# Flask app with upload folder
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Secret key for flash messages
app.secret_key= b'_5#y2L"F4Q8z\n\xec]/'

# Mongodb client
client = MongoClient('localhost', 27017)
db = client.louisdurandhw3

# Mongodb collections
users = db.users
blogsDb = db.blogs


@app.route('/', methods=('GET', 'POST'))
def blogs():
    user_cookie = request.cookies.get('userID')
    blogs = blogsDb.find({'privacy': 'public'})
    return render_template('blogs.html', stylesheet="/static/css/style.css", user = user_cookie, blogs=blogs)

@app.route('/register', methods=('GET', 'POST'))
def register():
    user_cookie = request.cookies.get('userID')
    if user_cookie:
        flash('You are already logged in')
        return redirect(url_for('blogs'))
    if request.method=='POST':
        # Account creation
        username = request.form["username"]
        password = request.form["password"]
        password_c = request.form["password_c"]
        if not username:
            flash('You have not provided a username')
        elif not password or not password_c:
            flash('You have not provided a password')
        elif password != password_c:
            flash('Passwords don\'t match')
        else:
            same_username = users.find_one({'username': username})
            if same_username:
                flash('This username is already taken, please choose another one')
                return redirect(url_for('register'))
            password = password + PASSWORD_HASH
            encrypted_password = hashlib.md5(password.encode())
            users.insert_one({'username': username, 'password': encrypted_password.hexdigest()})
            flash('Account created with success')
            return redirect(url_for('login'))
    return render_template('register.html', stylesheet="/static/css/style.css")

@app.route('/login', methods=('GET', 'POST'))
def login():
    # Check if user already has a user cookie
    user_cookie = request.cookies.get('userID')
    if user_cookie:
        flash('You are already logged in')
        return redirect(url_for('blogs'))
    # Account login
    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]
        if not username:
            flash('You have not provided a username')
        elif not password:
            flash('You have not provided a password')
        else:
            password = password + PASSWORD_HASH
            encrypted_password = hashlib.md5(password.encode())
            user_exists = users.find_one({'username': username, 'password': encrypted_password.hexdigest()})
            if not user_exists:
                flash('Wrong login or password')
                return redirect(url_for('login'))
            flash('Logged in successfully.')
            resp = make_response(redirect(url_for('blogs')))
            resp.set_cookie('userID', username)
            return resp

    return render_template('login.html', stylesheet="/static/css/style.css")


@app.route('/disconnect')
def disconnect():
    resp = make_response(redirect(url_for('blogs')))
    resp.delete_cookie('userID')
    flash("Disconnected successfully.")
    return resp


@app.route('/posts', methods=('GET', 'POST'))
def posts():
    # Check if user already has a user cookie
    user_cookie = request.cookies.get('userID')
    if not user_cookie:
        flash('You are not logged in')
        return redirect(url_for('login'))
    blogs = blogsDb.find({'author': user_cookie})
    return render_template('posts.html', name=user_cookie, stylesheet="/static/css/style.css", blogs=blogs)


@app.route('/add-blog', methods=('GET', 'POST'))
def addBlog():
    # Check if user already has a user cookie
    user_cookie = request.cookies.get('userID')
    if not user_cookie:
        flash('You are not logged in')
        return redirect(url_for('login'))
    if request.method=='POST':
        title = request.form["title"]
        text = request.form["text"]
        privacy = request.form["privacy"]
        author = user_cookie
        if not title:
            flash('You have not provided a title')
        elif not text:
            flash('You have not provided a text')
        else:
            blogsDb.insert_one({'author': author, 'title': title, 'text': text, 'privacy': privacy})
            flash('Blog created with success')
            return redirect(url_for('posts'))
    return render_template('add-blog.html', name=user_cookie, stylesheet="/static/css/style.css")

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)