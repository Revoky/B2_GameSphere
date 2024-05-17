import sqlite3
from sqlite3 import Error

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
        mail TEXT UNIQUE NOT NULL,
        date_naissance TEXT,
        solde REAL DEFAULT 0,
        num_facture INTEGER
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
    CREATE TABLE IF NOT EXISTS FACTURES (
        id INTEGER PRIMARY KEY,
        id_utilisateur INTEGER,
        nom_jeu TEXT,
        prix_jeu REAL,
        ancien_solde REAL,
        nouveau_solde REAL,
        date_facture TEXT,
        FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEURS(id)
    )
''')

connection.commit()
connection.close()
