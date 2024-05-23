from flask import Flask, render_template, request, redirect, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = '7s3p3uBZ'
app.database = '../game_sphere.db'

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

def get_game_by_id(game_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM JEUX WHERE id = ?', (game_id,))
        game = cursor.fetchone()
        conn.close()
        if game:
            return dict(game)  # Convert Row object to dictionary
        return None
    except Exception as e:
        print(f"Error fetching game: {e}")
        return None



def getUserData(username):
    try:
        cursor = get_db().cursor()
        cursor.execute("SELECT mail, mot_de_passe FROM UTILISATEURS WHERE mail = ?", (username,))
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
        games = get_games_api()
        return render_template('index.html', games=games)
    else:
        return redirect('/login')


@app.route('/index/<int:game_id>')
def game_detail(game_id):
    game = get_game_by_id(game_id)
    if game:
        return render_template('game_detail.html', game=game)
    else:
        return "Game not found", 404


@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
