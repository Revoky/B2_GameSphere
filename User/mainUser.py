from flask import Flask, render_template, request, redirect, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = '7s3p3uBZ'
app.database = '../Database/game_sphere.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.database)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



def getUserData(username):
    try:
        cursor = get_db().cursor()
        cursor.execute("SELECT mail, mot_de_passe FROM USERS WHERE mail = ?", (username,))
        id = cursor.fetchone()
        cursor.close()
        return id
    except sqlite3.Error as e:
        print("Error fetching user id:", e)
        return None

@app.route('/checkID', methods=['POST'])
def my_link():
    if request.method != 'POST':
        return redirect('/login')

    username = request.form.get('username')
    password = request.form.get('password')

    user = getUserData(username)

    if user and user[1] == password:
        session['user_logged_in'] = True
        return redirect('/index')
    else:
        print('Invalid username or password')
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/index')
def user_index():
    if 'user_logged_in' in session and session['user_logged_in']:
        return render_template('index.html')
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
