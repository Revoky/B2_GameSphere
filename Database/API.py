from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

connection = sqlite3.connect('back/game_sphere.db')
cursor = connection.cursor()

# Récupérer jeux
@app.route('/api/jeux', methods=['GET'])
def get_games():
    try:
        cursor.execute('SELECT * FROM JEUX')
        games = cursor.fetchall()
        return jsonify(games)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ajouter jeu
@app.route('/api/jeux', methods=['POST'])
def add_game():
    try:
        new_game = request.json
        cursor.execute('INSERT INTO JEUX (nom, prix) VALUES (?, ?)', (new_game['nom'], new_game['prix']))
        connection.commit()
        return jsonify({'message': 'Jeu ajouté avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Modifier jeu
@app.route('/api/jeux/<int:id>', methods=['PUT'])
def update_game(id):
    try:
        updated_game = request.json
        cursor.execute('UPDATE JEUX SET nom=?, prix=? WHERE id=?', (updated_game['nom'], updated_game['prix'], id))
        connection.commit()
        return jsonify({'message': 'Jeu modifié avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Supprimer jeu
@app.route('/api/jeux/<int:id>', methods=['DELETE'])
def delete_game(id):
    try:
        cursor.execute('DELETE FROM JEUX WHERE id=?', (id,))
        connection.commit()
        return jsonify({'message': 'Jeu supprimé avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500




# Récupérer utilisateurs
@app.route('/api/utilisateurs', methods=['GET'])
def get_users():
    try:
        cursor.execute('SELECT * FROM UTILISATEURS')
        users = cursor.fetchall()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ajouter utilisateur
@app.route('/api/utilisateurs', methods=['POST'])
def create_user():
    data = request.json
    try:
        cursor.execute('''INSERT INTO UTILISATEURS (prenom, nom, mot_de_passe, mail, date_naissance) VALUES (?, ?, ?, ?, ?)''', 
            (data['prenom'], data['nom'], data['mot_de_passe'], data['mail'], data['date_naissance']))
        connection.commit()
        return jsonify({'message': 'Utilisateur créé avec succès'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Modifier utilisateur
@app.route('/api/utilisateurs/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    try:
        cursor.execute('''UPDATE UTILISATEURS SET prenom=?, nom=?, mot_de_passe=?, mail=?, date_naissance=? WHERE id=?''', 
            (data['prenom'], data['nom'], data['mot_de_passe'], data['mail'], data['date_naissance'], id))
        connection.commit()
        return jsonify({'message': 'Utilisateur modifié avec succès'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Supprimer utilisateur
@app.route('/api/utilisateurs/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        cursor.execute('DELETE FROM UTILISATEURS WHERE id=?', (id,))
        connection.commit()
        return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)

connection.close()