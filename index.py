#!/usr/bin/env python3

from flask import Flask, render_template, request
import database

app = Flask(__name__)

@app.route('/')
def index():
    livres = database.afficherLivre()
    return render_template("afficheLivreSQL.html",livres=livres)

@app.route('/add', methods=['GET', 'POST'])
def add_values_sql(): 
    if request.method == "POST":
        titre = request.form['titre']
        date = request.form['date']
        nom = request.form['nom']
        prenom = request.form['prenom']

        database.ajouterLivreAuteur(titre, date, nom, prenom)
    
    return render_template("formLivreSQL.html")

if __name__ == '__main__':
    try: 
        app.run(host='localhost', port=81, debug=True)
    except:
        database.terminerConnection()
