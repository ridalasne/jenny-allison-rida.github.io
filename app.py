from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
import base64

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

    print("username " + str(request.form))

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])


    if users[POST_USERNAME]["password"] == POST_PASSWORD:
        session["username"] = POST_USERNAME;
        session['logged_in'] = True
        session["favorites"] = users[session["username"]]['favorites']

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


@app.route("/favorite", methods=["POST"])
def favorite():
    usersFile = open("users.json","r")
    users = json.load(usersFile)
    usersFile.close()

    print ('image name' + str(request.form))

    POST_IMAGE = str(request.form['imagename'])

    if POST_IMAGE in users[session["username"]]['favorites']:
        flash("You already saved this image!")
    else:
        users[session["username"]]['favorites'].append(POST_IMAGE)
        session["favorites"] = users[session["username"]]['favorites']

    favorites = session["favorites"]

    usersFile = open('users.json','w')
    json.dump(users, usersFile)
    usersFile.close()

    return render_template('favorite.html', favorites = favorites)



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
        users[POST_USERNAME] = {"password" : POST_PASSWORD , "favorites":[]}

        usersFile = open('users.json','w')
        json.dump(users, usersFile)
        usersFile.close()

    return home()



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
