from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Fonction pour se connecter à la base de données
def get_db_connection():
    # On se connecte au fichier créé juste avant
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ROUTE 1 : Accueil - Affiche la liste des livres
@app.route('/')
def index():
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres').fetchall()
    conn.close()
    
    # Construction d'un HTML simple pour voir le résultat tout de suite
    html = "<h1>📚 Ma Bibliothèque</h1>"
    html += "<p><a href='/recherche'>🔍 Rechercher un livre</a></p>"
    html += "<ul>"
    for livre in livres:
        stock_text = f"✅ (Dispo: {livre['stock']})" if livre['stock'] > 0 else "❌ Rupture"
        html += f"<li><b>{livre['titre']}</b> de {livre['auteur']} - {stock_text}</li>"
    html += "</ul>"
    return html

# ROUTE 2 : Recherche de livres (Demandé dans la Séquence 6)
@app.route('/recherche')
def recherche():
    query = request.args.get('q') # Récupère le mot tapé dans l'URL
    html = "<h1>🔍 Recherche de livre</h1>"
    html += "<form><input name='q' placeholder='Titre du livre...'><input type='submit' value='Chercher'></form>"

    if query:
        conn = get_db_connection()
        # Le symbole % permet de chercher "ce qui contient le texte"
        livres = conn.execute('SELECT * FROM livres WHERE titre LIKE ?', ('%' + query + '%',)).fetchall()
        conn.close()
        
        html += "<h3>Résultats :</h3><ul>"
        for livre in livres:
            html += f"<li>{livre['titre']} ({livre['auteur']})</li>"
        html += "</ul>"
        
    return html
