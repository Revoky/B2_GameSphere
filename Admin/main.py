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

def getAdminData(username):
    try:
        cursor = get_db().cursor()
        cursor.execute("SELECT nom_utilisateur, mot_de_passe FROM ADMINS WHERE nom_utilisateur = ?", (username,))
        id = cursor.fetchone()
        cursor.close()
        return id
    except sqlite3.Error as e:
        print("Error fetching admin id:", e)
        return None

@app.route('/checkID', methods=['POST'])
def my_link():
    if request.method != 'POST':
        return redirect('/admin/login')

    username = request.form.get('username')
    password = request.form.get('password')

    admin = getAdminData(username)

    if admin and admin[1] == password:
        session['admin_logged_in'] = True
        return redirect('/admin/index')
    else:
        print('Invalid username or password')
        return redirect('/admin/login')

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/admin/index')
def admin_index():
    if 'admin_logged_in' in session and session['admin_logged_in']:
        return render_template('index.html')
    else:
        return redirect('/admin/login')

@app.route('/admin/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin/login')

if __name__ == '__main__':
    app.run(debug=True)
