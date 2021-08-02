from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.secret_key = 'aslkdfjhklajsfdsafyeqbeyoaiuyebw67283098767a2343haksdkfjhklajshsdfiuy20387632987aysdfjsdakj'
# finding the current app path. (Location of this file)
project_dir = os.path.dirname(os.path.abspath(__file__))

# creating a database file (bookdatabase.db) in the above found path.
database_file = "sqlite:///{}".format(os.path.join(project_dir, "contacts.db"))

# connecting the database file (bookdatabase.db) to the sqlalchemy dependency.
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# connecting this app.py file to the sqlalchemy
db = SQLAlchemy(app)

# @app.before_first_request
# def create_table():
#     db.create_all()

# creating a model for the book table in the diagram
class Contact(db.Model):
    name = db.Column(db.String(80), unique = False, nullable = False)
    email = db.Column(db.String(80), unique = False, nullable = False, primary_key = True)
    message = db.Column(db.String(80), unique = False, nullable = False)
    # message = db.Column(db.String(80), unique = True, nullable = False)
    
    def __repr__(self):
        return "<Title: {}>".format(self.email)

class User(db.Model):
    username = db.Column(db.String(80), unique = False, nullable = False, primary_key = True)
    password = db.Column(db.String(80), unique = False, nullable = False)
    # message = db.Column(db.String(80), unique = True, nullable = False)
    def __repr__(self):
        return "<Title: {}>".format(self.username)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.form:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        contactInfo = Contact(name=name, email=email, message=message)
        db.session.add(contactInfo)
        db.session.commit()
    return render_template('contacts.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        users = User.query.all()
        for user in users:
            if username == user.username and password == user.password:
                session['user'] = user.username
                print("Logged in")
                return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if "user" in session:
        contacts = Contact.query.all()
        return render_template('admin.html', contacts=contacts)
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)