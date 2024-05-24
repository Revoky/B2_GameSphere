import sqlite3
from sqlite3 import Error
import new


try :
    connection = sqlite3.connect('../game_sphere.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ADMINS (
            id INTEGER PRIMARY KEY,
            nom_utilisateur TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UTILISATEURS (
            id INTEGER PRIMARY KEY,
            prenom TEXT,
            nom TEXT,
            mot_de_passe TEXT NOT NULL,
            image TEXT,
            mail TEXT UNIQUE NOT NULL,
            date_naissance TEXT,
            solde REAL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS JEUX (
            id INTEGER PRIMARY KEY,
            image TEXT,
            nom TEXT NOT NULL,
            prix REAL NOT NULL,
            note_moyenne REAL,
            avis_utilisateur TEXT,
            quantite INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AVIS (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            game_id INTEGER,
            body TEXT,
            note INTEGER,
            FOREIGN KEY(user_id) REFERENCES UTILISATEURS(id),
            FOREIGN KEY(game_id) REFERENCES JEUX(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FACTURES (
            id INTEGER PRIMARY KEY,
            id_game_user INTEGER,
            total REAL,
            ancien_solde REAL,
            nouveau_solde REAL,
            date_facture TEXT,
            FOREIGN KEY (id_game_user) REFERENCES JEUX_USERS(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS JEUX_USERS (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            game_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES UTILISATEURS(id),
            FOREIGN KEY(game_id) REFERENCES JEUX(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS JEUX_AVIS (
            id INTEGER PRIMARY KEY,
            avis_id INTEGER,
            game_id INTEGER,
            FOREIGN KEY(avis_id) REFERENCES AVIS(id),
            FOREIGN KEY(game_id) REFERENCES JEUX(id)
        )
    ''')

    cursor.execute('''INSERT INTO ADMINS (nom_utilisateur, mot_de_passe) VALUES ("administrateur", "admin")''')


    connection.commit()
    connection.close()
except sqlite3.Error as error:
    print("Error:", error)
finally:
    if connection:
        connection.close()