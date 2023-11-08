#!/usr/bin/env python3
import psycopg2
import random 
import string
import time
import sys

def ouvrirConnexion(database, user, password, host='localhost', port='5432'): 
    connection = psycopg2.connect(database=database, user=user, host=host, password=password, port=port)
    curseur = connection.cursor()
    return connection, curseur

try:
    connection, curseur = ouvrirConnexion("unebase", "alex", "alex")
except:
    raise Exception(f"Connection invalide, veuillez changer les informations de connexion dans le fichier : {__file__}.")
    
def executerRequete(requete:str):
    curseur.execute(requete)

def afficherLivre():
    curseur.execute('SELECT * FROM livre')
    resultat = curseur.fetchall()
    return resultat
   
def ajouterTuple(table:str,attributs:str):
    executerRequete("insert into {} values {}".format(table,attributs))
    connection.commit()

def ajouterLivreAuteur(titre,date,nom,prenom):
    executerRequete("select * from livre natural join ecrit natural join auteur where titre='{}' and nom='{}' and prenom='{}'".format(titre,nom, prenom))
    reply = curseur.fetchone() #Regarde et enlève de la table le dernière element executer

    if reply != None: # Si le l'execution du select ne marche pas None sera renvoyer par la methode fetchone
        print('Le livre est déjà dans la base de donné')
    else:
        executerRequete("select max(id_livre) from livre") #regarde le denier id de la table livre
        maxlivre = curseur.fetchone()[0]+1
        ajouterTuple('livre',"({},'{}',{})".format(maxlivre,titre,date))

        executerRequete("select id_auteur from auteur where nom='{}' and prenom='{}'".format(nom, prenom))
        reply = curseur.fetchone()
        if reply != None:
            ajouterTuple("ecrit","({},{})".format(reply[0],maxlivre))
        else:
            executerRequete("select max(id_auteur) from auteur")#regarde le denier id de la table auteur
            maxauteur = curseur.fetchone()[0]+1
            ajouterTuple("auteur","({},'{}','{}')".format(maxauteur,nom,prenom))
            ajouterTuple("ecrit","({},{})".format(maxauteur,maxlivre))

def terminerConnection():
    connection.commit()
    curseur.close()
    connection.close()

def get_random_length():
    return random.randint(2, 20)

def get_random_string(n):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(n))
    return result_str.capitalize()

def get_random_date():
    return random.randint(0, 2023)

def addLivreAllTenSecond():
    try: 
        while True:
            longueur_titre = get_random_length()
            longueur_nom = get_random_length()
            longueur_prenom = get_random_length()

            titre = get_random_string(longueur_titre)
            
            date = get_random_date()
            nom = get_random_string(longueur_nom)
            prenom = get_random_string(longueur_prenom)

            ajouterLivreAuteur(titre,date,nom,prenom)
            time.sleep(10)
    except KeyboardInterrupt: 
        pass


if __name__ == '__main__':
    if sys.argv[1]=='print': 
        print('Listes des livres') 
        print(afficherLivre())
    elif sys.argv[1]=='add': 
        print('Ajouter un livre à la bibliothèque.')

        titre = input("Veulliez renseigner le titre du livre: ")
        date = input("Veulliez renseigner la date de creation du livre: ")
        nom = input("Veulliez renseigner le nom de l'auteur: ")
        prenom = input("Veulliez renseigner le prenom de l'auteur: ")

        ajouterLivreAuteur(titre,date,nom,prenom)
    elif sys.argv[1]=='10s':
        print('Ajout de livre toutes les 10s')
        addLivreAllTenSecond()
    else: 
        print('argument:  print, add, 10s')
    terminerConnection()
