"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, login_manager
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, Registration
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="mybook2020"
)

mycursor = mydb.cursor()

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def registerUser():
    """Render website's Registration Form."""
    form = Registration()
    mycursor = mydb.cursor()

    if request.method == "POST"  and form.validate_on_submit():
        f_name = form.f_name.data
        l_name = form.l_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        mycursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = mycursor.fetchone()
        print(user)
        if user:
            flash(u'This username is already taken', 'error')
        else:
            sql = "INSERT INTO user (f_name, l_name, username, email, password) VALUES (%s, %s, %s, %s, %s)"
            val = (f_name, l_name, username,
                email, password)

            mycursor.execute(sql, val)
            mydb.commit()

            print(mycursor.rowcount, "record inserted.")
            print("1 record inserted, ID:", mycursor.lastrowid)
            flash('Successfully registered', 'success')

            return redirect(url_for("home"))

    # Flash errors in form and redirects to Register Form
    flash_errors(form)
    return render_template('register.html', form=form)


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    mycursor = mydb.cursor()

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if user exists using MySQL
        # cursor = mysql.connection.cursor(mycursor.DictCursor)
        mycursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        user = mycursor.fetchone()
        # If user exists in users table in out database

        if user:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[3]
            # Redirect to home page
            flash('Logged in Succesfully', 'success')
        else:
            # user does not exist or username/password incorrect
            flash(u'Invalid Credentials', 'error')

    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   flash('Logged out Succesfully', 'success')
#    print(session['loggedin'])
   # Redirect to login page
   return redirect(url_for('home'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the user info for the user so we can display it on the profile page
        mycursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        user = mycursor.fetchone()
        # Show the profile page with user info
        return render_template('profile.html', user=user)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def pyhome():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

# Flash errors from the form if validation fails


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
