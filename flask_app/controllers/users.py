from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.tree import Trees


bcrypt = Bcrypt(app)



@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template('index.html')
    else:
        return redirect('/dashboard/')



@app.route('/register/', methods=['post'])
def register():
    isValid = User.validate(request.form)
    if not isValid:
        return redirect('/')
    else:
        newUser = {
            'firstName': request.form['firstName'],
            'lastName': request.form['lastName'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        id = User.save(newUser)
        if not id:
            flash('Something went wrong')
            return redirect('/')
        else:
            session['user_id'] = id
            flash("You are now logged in")
            return redirect('/dashboard/')



@app.route('/login/', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.getEmail(data) # check if the email is in the database
    if not user: # if not let them know
        flash('That email is not in our database please register')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Wrong password')
        return redirect('/')
    else:
        session['user_id'] = user.id
        flash("You are now logged in")
        return redirect('/dashboard/')



@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')



@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        theTrees = Trees.getAll()
        theUsers = User.getAll()
        return render_template('dashboard.html', user=theUser, trees=theTrees, users=theUsers)



@app.route('/usersTrees/')
def usersTrees():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        theTrees = Trees.getAll()
        theUsers = User.getAll()
        return render_template('usersTrees.html', user=theUser, trees=theTrees, users=theUsers)

        