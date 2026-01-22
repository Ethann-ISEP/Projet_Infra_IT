from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
#              ACCUEIL GENERAL
# ==========================================
@app.route('/')
def index():
    html = """
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: auto; padding: 20px; }
        .btn { display: inline-block; padding: 10px 20px; text-decoration: none; color: white; border-radius: 5px; margin: 10px; }
        .btn-lib { background-color: #3498db; }
        .btn-task { background-color: #27ae60; }
        h1 { text-align: center; }
    </style>
    <h1>Bienvenue sur mon Portail SI</h1>
    <div style="text-align:center">
        <a href="/bibliotheque" class="btn btn-lib">📚 Accéder à la Bibliothèque</a>
        <a href="/taches" class="btn btn-task">✅ Accéder aux Tâches</a>
    </div>
    """
    return html

# ==========================================
#           PARTIE 1 : BIBLIOTHEQUE
# ==========================================
@app.route('/bibliotheque')
def bibliotheque():
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres').fetchall()
    conn.close()
    
    html = "<h1>📚 Ma Bibliothèque</h1>"
    html += "<p><a href='/'>🏠 Retour Portail</a> | <a href='/admin'>➕ Ajouter Livre</a></p><ul>"
    for livre in livres:
        html += f"<li><b>{livre['titre']}</b> ({livre['stock']} en stock) "
        if livre['stock'] > 0:
            html += f"<a href='/emprunter/{livre['id']}'>[Emprunter]</a>"
        html += "</li>"
    html += "</ul>"
    return html

@app.route('/emprunter/<int:id_livre>')
def emprunter(id_livre):
    conn = get_db_connection()
    conn.execute('UPDATE livres SET stock = stock - 1 WHERE id = ? AND stock > 0', (id_livre,))
    conn.commit()
    conn.close()
    return redirect('/bibliotheque')

@app.route('/admin', methods=('GET', 'POST'))
def admin():
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute('INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)',
                     (request.form['titre'], request.form['auteur'], request.form['stock']))
        conn.commit()
        conn.close()
        return redirect('/bibliotheque')
    
    return "<h1>Ajouter Livre</h1><form method='post'>Titre: <input name='titre'><br>Auteur: <input name='auteur'><br>Stock: <input name='stock'><br><input type='submit'></form>"

# ==========================================
#           PARTIE 2 : GESTION DE TACHES
# ==========================================

# 1. Afficher les tâches (Livrable: Liste visible )
@app.route('/taches')
def taches():
    conn = get_db_connection()
    # On récupère les tâches, les non-terminées en premier
    taches = conn.execute('SELECT * FROM taches ORDER BY est_terminee ASC, date_echeance ASC').fetchall()
    conn.close()

    html = "<h1>✅ Mes Tâches</h1>"
    html += "<p><a href='/'>🏠 Retour Portail</a> | <a href='/ajouter_tache'>➕ Nouvelle Tâche</a></p>"
    
    html += "<table border='1' cellpadding='10' style='border-collapse: collapse; width: 100%;'>"
    html += "<tr><th>Terminée?</th><th>Tâche</th><th>Description</th><th>Échéance</th><th>Actions</th></tr>"
    
    for tache in taches:
        # Style barré si terminée
        style = "text-decoration: line-through; color: gray;" if tache['est_terminee'] else ""
        etat = "🟢 Fait" if tache['est_terminee'] else "🔴 A faire"
        
        html += f"<tr style='{style}'>"
        html += f"<td>{etat}</td>"
        html += f"<td><b>{tache['titre']}</b></td>"
        html += f"<td>{tache['description']}</td>"
        html += f"<td>{tache['date_echeance']}</td>"
        html += f"<td>"
        if not tache['est_terminee']:
            html += f"<a href='/terminer_tache/{tache['id']}'>✅ Valider</a> | "
        html += f"<a href='/supprimer_tache/{tache['id']}' style='color:red'>🗑 Supprimer</a>"
        html += "</td></tr>"
    html += "</table>"
    return html

# 2. Ajouter une tâche (Livrable: Formulaire )
@app.route('/ajouter_tache', methods=('GET', 'POST'))
def ajouter_tache():
    if request.method == 'POST':
        titre = request.form['titre']
        desc = request.form['description']
        date = request.form['date']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO taches (titre, description, date_echeance) VALUES (?, ?, ?)',
                     (titre, desc, date))
        conn.commit()
        conn.close()
        return redirect('/taches')

    html = "<h1>➕ Nouvelle Tâche</h1>"
    html += "<form method='post'>"
    html += "Titre (*) : <br><input type='text' name='titre' required><br>"
    html += "Description : <br><textarea name='description'></textarea><br>"
    html += "Date d'échéance : <br><input type='date' name='date'><br><br>"
    html += "<input type='submit' value='Ajouter la tâche'>"
    html += "</form>"
    html += "<p><a href='/taches'>Annuler</a></p>"
    return html

# 3. Marquer comme terminée (Livrable: Tâche terminée )
@app.route('/terminer_tache/<int:id_tache>')
def terminer_tache(id_tache):
    conn = get_db_connection()
    conn.execute('UPDATE taches SET est_terminee = 1 WHERE id = ?', (id_tache,))
    conn.commit()
    conn.close()
    return redirect('/taches')

# 4. Supprimer une tâche (Livrable: Suppression )
@app.route('/supprimer_tache/<int:id_tache>')
def supprimer_tache(id_tache):
    conn = get_db_connection()
    conn.execute('DELETE FROM taches WHERE id = ?', (id_tache,))
    conn.commit()
    conn.close()
    return redirect('/taches')
