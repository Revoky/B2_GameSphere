from flask import Flask, render_template, request, redirect, session, g, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = '7s3p3uBZ'
app.database = '../Database/game_sphere.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.database)
    return db

def get_db_connection():
    conn = sqlite3.connect('../game_sphere.db')
    conn.row_factory = sqlite3.Row
    return conn

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

#('/api/utilisateurs', methods=['GET'])
def get_utilisateurs():
    try:
        cur = get_db().cursor()
        cur.execute('SELECT * FROM UTILISATEURS')
        rows = cur.fetchall()
        cur.close()

        # Assuming your table has columns id and name
        utilisateurs = [{'id': row[0], 'name': row[1]} for row in rows]
        return jsonify(utilisateurs)
    except Exception as e:
        print('Error fetching users:', e)
        return jsonify({'error': 'Internal Server Error'}), 500

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

@app.route('/admin/users', methods=['GET'])
def get_users():
    users = get_users_api()
    return render_template('users.html', users=users)

# Récupérer utilisateurs
@app.route('/api/utilisateurs', methods=['GET'])
def get_users_api():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM UTILISATEURS')
        users = cursor.fetchall()
        conn.close()
        return users
    except Exception as e:
        return {'error': str(e)}, 500

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
