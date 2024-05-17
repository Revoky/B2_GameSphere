import sqlite3

connection = sqlite3.connect('../game_sphere.db')
cursor = connection.cursor()

def newAdmin(username, password) :
    try:
        cursor.execute("INSERT INTO ADMINS (nom_utilisateur, mot_de_passe) VALUES (?, ?)", (username, password))
        connection.commit()
        print("Données ajoutées avec succès à la table ADMIN.")
    except sqlite3.Error as e:
        print("Erreur lors de l'insertion des données:", e)


def newUser(first_name, last_name, password, email, date_of_birth, balance=0, bill_number=None):
    try:
        cursor.execute("INSERT INTO UTILISATEURS (prenom, nom, mot_de_passe, mail, date_naissance, solde, num_facture) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (first_name, last_name, password, email, date_of_birth, balance, bill_number))
        connection.commit()
        print("Données ajoutées avec succès à la table UTILISATEURS.")
    except sqlite3.Error as e:
        print("Erreur lors de l'insertion des données:", e)


def newGame(image, name, price, average_rating=None, user_reviews=None, quantity=0):
    try:
        cursor.execute("INSERT INTO JEUX (image, nom, prix, note_moyenne, avis_utilisateur, quantite) VALUES (?, ?, ?, ?, ?, ?)",
                       (image, name, price, average_rating, user_reviews, quantity))
        connection.commit()
        print("Données ajoutées avec succès à la table JEUX.")
    except sqlite3.Error as e:
        print("Erreur lors de l'insertion des données:", e)


def newBill(user_id, game_name, game_price, old_balance, new_balance, bill_date):
    try:
        cursor.execute("INSERT INTO FACTURES (id_utilisateur, nom_jeu, prix_jeu, ancien_solde, nouveau_solde, date_facture) VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, game_name, game_price, old_balance, new_balance, bill_date))
        connection.commit()
        print("Données ajoutées avec succès à la table FACTURES.")
    except sqlite3.Error as e:
        print("Erreur lors de l'insertion des données:", e)

cursor.close()
connection.close()
