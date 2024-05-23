import sqlite3

def create_connection():
    connection = sqlite3.connect('../game_sphere.db')
    return connection

def new_admin(nom_utilisateur, mot_de_passe):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO ADMINS (nom_utilisateur, mot_de_passe)
        VALUES (?, ?)
    ''', (nom_utilisateur, mot_de_passe))
    connection.commit()
    connection.close()

def new_utilisateur(prenom, nom, mot_de_passe, image, mail, date_naissance, solde=0):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO UTILISATEURS (prenom, nom, mot_de_passe, image, mail, date_naissance, solde)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (prenom, nom, mot_de_passe, image, mail, date_naissance, solde))
    connection.commit()
    connection.close()

def new_jeux(image, nom, prix, note_moyenne=None, avis_utilisateur=None, quantite=0):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO JEUX (image, nom, prix, note_moyenne, avis_utilisateur, quantite)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (image, nom, prix, note_moyenne, avis_utilisateur, quantite))
    connection.commit()
    connection.close()

def new_avis(user_id, game_id, body, note):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO AVIS (user_id, game_id, body, note)
        VALUES (?, ?, ?, ?)
    ''', (user_id, game_id, body, note))
    connection.commit()
    connection.close()

def new_facture(id_game_user, total, ancien_solde, nouveau_solde, date_facture):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO FACTURES (id_game_user, total, ancien_solde, nouveau_solde, date_facture)
        VALUES (?, ?, ?, ?, ?)
    ''', (id_game_user, total, ancien_solde, nouveau_solde, date_facture))
    connection.commit()
    connection.close()

def new_jeux_user(user_id, game_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO JEUX_USERS (user_id, game_id)
        VALUES (?, ?)
    ''', (user_id, game_id))
    connection.commit()
    connection.close()

def new_jeux_avis(avis_id, game_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO JEUX_AVIS (avis_id, game_id)
        VALUES (?, ?)
    ''', (avis_id, game_id))
    connection.commit()
    connection.close()
