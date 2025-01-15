import datetime
import os.path
from flask_sqlalchemy import SQLAlchemy
import click
from sqlalchemy.orm import backref
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import yaml
from .app import db


db = db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomRole = db.Column(db.String(25))


class Utilisateur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(255), unique = True)
    nom = db.Column(db.String(255))
    adresseMail = db.Column(db.String(255), unique = True)
    mdp = db.Column(db.String(255))
    image = db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    est_active = db.Column(db.Boolean, unique=False, default=False)
    id_R = db.Column(db.Integer)
    role = db.relationship("Role", foreign_keys=[id_R], primaryjoin = 'Role.id == Utilisateur.id_R' )



class Classe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nomClasse = db.Column(db.String(255))
    gerant_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"))
    gerant = db.relationship("Utilisateur", foreign_keys=[gerant_id], primaryjoin = 'Utilisateur.id == Classe.gerant_id')
    
    def __repr__(self):
        return self.id, self.nomClasse


class Appartenir(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    classe_id = db.Column(db.Integer)
    utilisateur_id = db.Column(db.Integer)
    classe = db.relationship("Classe", foreign_keys=[classe_id],primaryjoin = 'Classe.id == Appartenir.classe_id')
    utilisateur = db.relationship("Utilisateur", foreign_keys=[utilisateur_id], primaryjoin = 'Utilisateur.id == Appartenir.utilisateur_id')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    expediteur = db.Column(db.Integer)
    destinataire = db.Column(db.Integer)
    contenue = db.Column(db.String(1024))
    dateEnvoi = db.Column(db.DateTime,  default=datetime.datetime.utcnow)
    exp = db.relationship("Utilisateur", foreign_keys=[expediteur], primaryjoin = 'Utilisateur.id == Message.expediteur')
    dest = db.relationship("Utilisateur", foreign_keys = [destinataire], primaryjoin = 'Utilisateur.id == Message.destinataire')


class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    responsable_id = db.Column(db.Integer)
    titreScenario = db.Column(db.String(255))
    resumeScenario = db.Column(db.String(512))
    iconeScenario = db.Column(db.String(255))
    tempsMaxScenario = db.Column(db.Integer)   #à corriger
    dateMiseEnLigneScenario = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    resp = db.relationship("Utilisateur", foreign_keys = [responsable_id], primaryjoin = 'Utilisateur.id == Scenario.responsable_id')


class Partie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    utilisateur_id = db.Column(db.Integer)
    scenario_id = db.Column(db.Integer)
    dateDebutPartie = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    dureePartie = db.Column(db.Integer)   # à corriger
    notePartie = db.Column(db.Integer)
    nbExoFaites = db.Column(db.Integer, default = 0)
    nbSalleDebloquees = db.Column(db.Integer)
    estDebloquee = db.Column(db.Boolean, default = False)
    utilisateur = db.relationship("Utilisateur", foreign_keys = [utilisateur_id], primaryjoin = 'Utilisateur.id == Partie.utilisateur_id')
    scenario = db.relationship("Scenario", foreign_keys = [scenario_id], primaryjoin = 'Scenario.id == Partie.scenario_id')


class Carte(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    utilisateur_id = db.Column(db.Integer)
    nomCarte = db.Column(db.String(255))
    planCarte = db.Column(db.String(255))
    utilisateur = db.relationship("Utilisateur" ,foreign_keys = [utilisateur_id], primaryjoin = 'Utilisateur.id == Carte.utilisateur_id')


class Contient(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    scenario_id = db.Column(db.Integer)
    carte_id = db.Column(db.Integer)
    niveau = db.Column(db.String(255))
    scenario = db.relationship("Scenario", foreign_keys = [scenario_id], primaryjoin = 'Scenario.id == Contient.scenario_id')
    carte = db.relationship("Carte", foreign_keys = [carte_id], primaryjoin = 'Carte.id == Contient.carte_id')


class Exercice(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    createur_id  = db.Column(db.Integer)
    typeQuestion = db.Column(db.String(255))
    nivDifficulte = db.Column(db.Integer)
    #image = db.Column(db.String(255))
    question = db.Column(db.String(255))
    proposition = db.Column(db.PickleType, nullable=True)
    # proposition = db.Column(db.String(255))# db.Column(db.ARRAY(db.String(255)))
    correction = db.Column(db.String(255))
    createur = db.relationship("Utilisateur", foreign_keys = [createur_id], primaryjoin = 'Utilisateur.id == Exercice.createur_id')



    

class Tileset(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nom_Ts = db.Column(db.String(255))
    imageTS = db.Column(db.String(255))


class Piece(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tileset_id = db.Column(db.Integer)
    nomPiece = db.Column(db.String(255))
    tileset = db.relationship("Tileset", foreign_keys = [tileset_id], primaryjoin = 'Tileset.id == Piece.tileset_id')


class Contien(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    piece_id = db.Column(db.Integer)
    carte_id = db.Column(db.Integer)
    ordre = db.Column(db.String(255))
    piece = db.relationship("Piece", foreign_keys = [piece_id], primaryjoin = 'Piece.id == Contien.piece_id')
    carte = db.relationship("Carte", foreign_keys = [carte_id], primaryjoin = 'Carte.id == Contien.carte_id')


class Cacher(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    exo_id = db.Column(db.Integer, primary_key= True)
    piece_id = db.Column(db.Integer, primary_key= True)
    carte_id = db.Column(db.Integer, primary_key= True)
    numéroTuile = db.Column(db.Integer)
    exo = db.relationship("Exercice", foreign_keys = [exo_id], primaryjoin = 'Exercice.id == Cacher.exo_id')
    piece = db.relationship("Piece", foreign_keys = [piece_id], primaryjoin = 'Piece.id == Cacher.piece_id')
    carte = db.relationship("Carte", foreign_keys = [carte_id], primaryjoin = 'Carte.id == Cacher.carte_id')





#pour tester la base 
"""r = Role(
    nomRole = "Admin"
    )

u = Utilisateur(
    pseudo = "Doom",
    prenom = "Redwan",
    nom = "OMARI",
    adresseMail = "redwan.oma20@gmail.com",
    mdp = "123456",
    image = "C://user/image",
    avatar = "C://user/image",
    id_R = 1
    )


u2 = Utilisateur(
    pseudo = "Doom2",
    prenom = "Redwan2",
    nom = "OMARI2",
    adresseMail = "redwan.oma20@gmail.com2",
    mdp = "1234562",
    image = "C://user/image2",
    avatar = "C://user/image2",
    id_R = 1
    )


c = Classe(
    nomClasse = "2A3B",
    gerant_id = 1
    )


a = Appartenir(
    classe_id = 1,
    utilisateur_id = 1
    )


m = Message(
    expediteur = 1,
    destinataire = 2,
    contenue = "this is a message :)"
    )


s = Scenario(
    responsable_id = 2,
    titreScenario = "Scenario de malade",
    resumeScenario = "encore scenario de malade",
    iconeScenario = "C://dans le truc aussi",
    tempsMaxScenario = 15
    )


p = Partie(
    utilisateur_id = 2,
    scenario_id = 1,
    notePartie = 19,
    nbExoFaites = 0,
    dureePartie = 200,
    nbSalleDebloquees = 3
    )


carte = Carte(
    utilisateur_id = 2,
    nomCarte = "merde",
    planCarte = '12345;12345;12345'
    )


def __init_db__():
    db.drop_all()
    db.create_all()
    init_role_ids()
    new_user("eleve", "eleve eleve", "eleve@eleve.eleve", generate_password_hash("eleve", method='sha256'))
    new_user("prof", "prof prof", "prof@prof.prof", generate_password_hash("prof", method='sha256'), id_R = 2)
    new_user("moqim1", "moqim1", "moqim1@moqim.moqim", generate_password_hash("moqim", method='sha256'), id_R = 1)
    
    new_user("moqim2", "moqim2", "moqim2@moqim.moqim", generate_password_hash("moqim", method='sha256'))
    new_user("moqim3", "moqim3", "moqim3@moqim.moqim", generate_password_hash("moqim", method='sha256'))
    new_user("moqim4", "moqim4", "moqim4@moqim.moqim", generate_password_hash("moqim", method='sha256'))
    new_user("admin", "admin admin", "admin@admin.admin", generate_password_hash("admin", method='sha256'), id_R=3)
    
    new_class("WAIT", 2)
    new_class("2A1A", 2)
    new_class("2A1B", 2)
    new_class("2A2A", 2)
    new_class("2A2B", 2)
    new_class("2A3A", 2)
    new_class("2A3B", 2)
     
    
    print("-------------------"+"\n"*10+"-------------------jj")
    print()
    



def get_students_list_for_teacher(teacher_id):
    classes_liste = Classe.query.filter_by(gerant_id = teacher_id).all()
    student_liste = list()
    for i in classes_liste:
        a = Appartenir.query.filter_by(classe_id = i.id).all()
        if len(a) > 0:
            for j in a:
                user = j.utilisateur
                student_liste.append(user)
    return student_liste


db.session.add(c)
db.session.add(r)
db.session.add(u)
db.session.add(u2)
db.session.add(a)
db.session.add(m)
db.session.add(s)
db.session.add(p)
db.session.add(carte)
db.session.commit()


def get_list_classes():
    return Classe.query.all()[1:]

def changer_classe(student_id, class_id):
    ap = Appartenir.query.filter_by(utilisateur_id = student_id).first()
    ap.classe_id = int(class_id)
    db.session.commit()

"""
