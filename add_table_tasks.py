import sqlite3

connection = sqlite3.connect('database.db')
cur = connection.cursor()
print("Création de la table taches...")
cur.execute("""
    CREATE TABLE IF NOT EXISTS taches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        description TEXT,
        date_echeance DATE,
        est_terminee BOOLEAN NOT NULL DEFAULT 0
    )
""")

connection.commit()
connection.close()
print("Terminé ! La table taches a été ajoutée sans toucher aux livres.")
