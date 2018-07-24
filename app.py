from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json

app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return start()

@app.route('/login', methods=['POST'])
def do_admin_login():

    usersFile = open("users.json","r")
    users = json.load(usersFile)
    usersFile.close()

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    '''
    if POST_PASSWORD == users[POST_USERNAME]["password"]:
        session['logged_in'] = True '''

    if users[POST_USERNAME]["password"] == POST_PASSWORD:
        session["username"] = POST_USERNAME;
        session['logged_in'] = True
    else:
        flash('wrong password!')

    return home()


@app.route('/homepage')
def start():
    if session['logged_in'] == True:
        return render_template('index.html')
    else:
        return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/register")
def register():
        return render_template('register.html')

@app.route("/aboutUS")
def aboutUs():
        return render_template('aboutus.html')

@app.route("/photoloc")
def photoloc():
    return render_template('picturelocations.html')

@app.route("/foodloc")
def foodloc():
    return render_template('foodlocations.html')

@app.route("/touristicloc")
def touristicloc():
    return render_template('touristicdestinations.html')


@app.route("/workscited")
def workscited():
    return render_template('workscited.html')
"""
@app.route("/workscited")
def touristicloc():
    return render_template('workscited.html')
"""
@app.route("/createUser", methods=['POST'])
def createUser():

    usersFile = open("users.json","r")
    users = json.load(usersFile)
    usersFile.close()

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    if POST_USERNAME in users:
        flash("This username exists")
    else:
        users[POST_USERNAME] = {"password" : POST_PASSWORD}

        usersFile = open('users.json','w')
        json.dump(users, usersFile)
        usersFile.close()

    return home()



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
