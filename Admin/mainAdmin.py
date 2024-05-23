from flask import Flask, render_template, request, redirect, session, g, url_for
import sqlite3

from Database.new import new_jeux, new_utilisateur

app = Flask(__name__)
app.secret_key = '7s3p3uBZ'
app.database = '../game_sphere.db'

def get_db():
    db = getattr(g, '../Database/game_sphere.db', None)
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



@app.route('/admin/games', methods=['GET'])
def get_games():
    games = get_games_api()
    return render_template('games.html', games=games)


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

@app.route('/api/games', methods=['GET'])
def get_games_api():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM JEUX')
        games = cursor.fetchall()
        conn.close()
        return games
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/admin/index', methods=['GET', 'POST'])
def admin_index():
    if 'admin_logged_in' in session and session['admin_logged_in']:
        users = get_users_api()
        games = get_games_api()
        return render_template('index.html', users=users, games=games)
    else:
        return redirect('/admin/login')

@app.route('/admin/new_utilisateur', methods=['GET', 'POST'])
def add_utilisateur():
    if request.method == 'POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        mot_de_passe = request.form['mot_de_passe']
        image = request.form['image']
        mail = request.form['mail']
        date_naissance = request.form['date_naissance']
        solde = request.form['solde']
        new_utilisateur(prenom, nom, mot_de_passe, image, mail, date_naissance, float(solde))
        return redirect('/admin/index')
    return render_template('new_utilisateur.html')

@app.route('/admin/new_jeux', methods=['GET', 'POST'])
def add_jeux():
    if request.method == 'POST':
        image = request.form['image']
        nom = request.form['nom']
        prix = request.form['prix']
        note_moyenne = request.form['note_moyenne']
        avis_utilisateur = request.form['avis_utilisateur']
        quantite = request.form['quantite']

        # Print out the SQL query and its parameters
        print("SQL Query:")
        print('''
                   INSERT INTO JEUX (image, nom, prix, note_moyenne, avis_utilisateur, quantite)
                   VALUES (?, ?, ?, ?, ?, ?)
               ''')
        print("Parameters:")
        print((image, nom, prix, note_moyenne, avis_utilisateur, quantite))

        new_jeux(image, nom, float(prix), float(note_moyenne) if note_moyenne else None, avis_utilisateur if avis_utilisateur else None, int(quantite))
        return redirect('/admin/index')
    return render_template('new_jeux.html')

@app.route('/admin/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin/login')

if __name__ == '__main__':
    app.run(debug=True)
