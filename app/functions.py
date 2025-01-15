from .models import Role, Utilisateur, Classe, Appartenir, Message, Scenario, Partie, Carte, Contient, Exercice, Tileset, Piece, Contien, Cacher, db
from werkzeug.security import generate_password_hash, check_password_hash










def new_exo(typeQuestion, question, proposition, correction, createur_id, nivDifficulte = 1):
    """Creation d'un nouveau exo

    Args:
        typeQuestion (String): type de l'exo va etre choisi par le prof
        question (String): Une exo à afficher dans le jeu
        proposition (list de string): liste des propositions des repenses
        correction (String ):la correstion de l'exo
        createur_id (int): l'id de la personne qui a creé l'exo
        nivDifficulte (int, 1): le niveau de difficulté. Defaults to 1.
    Return:
        None
    """
    exo = Exercice(typeQuestion = typeQuestion, question = question, proposition = proposition, correction = correction , createur_id = createur_id, nivDifficulte = nivDifficulte)
    db.session.add(exo)
    db.session.commit()


def new_user(pseudo, nom, adresseMail, mdp, id_R=1):
    """Creation d'un niveau utilisateur
    
    
    Args:
        pseudo (String): Le pseudo de l'utilisateur
        nom (String): le nom de l'utilisateur
        adresseMail (String):Email de l'utilisateur
        mdp (String): Le mot de passe de l'utilisateur
        id_R (int, 1): L'id de rôle de l'utilisateur. Defaults to 1.
        
        #NOTE A VOIR!!!!
        id_R -> (1, 2, 3)
            1: Eleve
            2: Prof
            3: Admin
        Image et avatar sont mises par defaut !
    
    Return:
        None
    """
    
    
    image = "user_img_default.png"
    avatar = "profil_ava_default.png"
    
    u = Utilisateur(pseudo = pseudo, nom = nom, adresseMail = adresseMail, mdp = mdp,  image= image, avatar = avatar, id_R=id_R)
    db.session.add(u)
    db.session.commit()
    if id_R == 1:
        a = Appartenir(classe_id = 1, utilisateur_id = u.id)
        db.session.add(a)
        db.session.commit()
    
    
    
def new_class(nomClasse, gerant_id):
    """Creation d'une nouvelle classe

    Args:
        nomClasse (String): Le nom de la classe
        gerant_id (int): L'id du respensable de cette classe
        
    Return:
        None
    """
    c = Classe(nomClasse = nomClasse, gerant_id = gerant_id)
    db.session.add(c)
    db.session.commit()
    
    
    
def new_relationship_class_user(class_id, user_id):
    """Creation de la relation entre un etudient et une classe

    Args:
        class_id (int): l'id de la classe
        user_id (int): l'id du etudient
        
    Return:
        None
    """
    a = Appartenir(classe_id = class_id, utilisateur_id = user_id)
    db.session.add(a)
    db.session.commit()
    
    
    
    
#####################################################################
#####################################################################
#                         INIT
#####################################################################
#####################################################################
    
    
    
def init_role_ids():
    """creation des rôles
    """
    r1 = Role(id = 1, nomRole = "student")
    r2 = Role(id = 2, nomRole = "teacher")
    r3 = Role(id = 3, nomRole = "admin")
    db.session.add(r1)
    db.session.add(r2)
    db.session.add(r3)
    db.session.commit()
    

def __run_db__():
    __drop_db__()
    __create_db__()
    __init_db__()
    print("\n"*5 + "*"*10 + " Database was created and Application started successfully " + "*"*10+ "\n"*5)



def __drop_db__():
    db.drop_all()
    print("\n"*5 + "*"*10 + " Database droped " + "*"*10+ "\n"*5)

def __create_db__():
    db.create_all()
    print("\n"*5 + "*"*10 + " Database created " + "*"*10+ "\n"*5)

def __init_db__():
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
    print("\n"*5 + "*"*10 + " Database initialization " + "*"*10+ "\n"*5)
    
    s1 = Scenario(
        responsable_id = 2,
        titreScenario = "Scenario de malade",
        resumeScenario = "encore scenario de malade",
        iconeScenario = "C://dans le truc aussi",
        tempsMaxScenario = 15
        )
    s2 = Scenario(
        responsable_id = 2,
        titreScenario = "Scenario de malade",
        resumeScenario = "encore scenario de malade",
        iconeScenario = "C://dans le truc aussi",
        tempsMaxScenario = 15
        )
    s3 = Scenario(
        responsable_id = 2,
        titreScenario = "Scenario de malade",
        resumeScenario = "encore scenario de malade",
        iconeScenario = "C://dans le truc aussi",
        tempsMaxScenario = 15
        )


    p1 = Partie(
        utilisateur_id = 1,
        scenario_id = 1,
        notePartie = 15,
        nbExoFaites = 20,
        dureePartie = 150,
        nbSalleDebloquees = 7
        )

    p2 = Partie(
        utilisateur_id = 1,
        scenario_id = 1,
        notePartie = 15,
        nbExoFaites = 20,
        dureePartie = 150,
        nbSalleDebloquees = 45
        )
    p3 = Partie(
        utilisateur_id = 1,
        scenario_id = 1,
        notePartie = 15,
        nbExoFaites = 20,
        dureePartie = 150,
        nbSalleDebloquees = 15
        )

    
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.commit()
    
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.commit()

    
    #__test_db__()
    carte = Carte(
    utilisateur_id = 2,
    nomCarte = "carte 1",
    planCarte = 'premiere'
    )
    db.session.add(carte)
    db.session.commit()

     
    



def __test_db__():
    print("\n"*5 + "*"*10 + "Testing zone" + "*"*10+ "\n"*5)
    print()
    print()
    

    
    
    
    
    
    
#####################################################################
#####################################################################
#                         VALIDATIONS
#####################################################################
#####################################################################




def valiation_pseudo(pseudo):
    """Validation du pseudo de l'etilisateur

    Args:
        pseudo (String): le pseudo

    Returns:
        var: Une instance du l'objet utilisateur, sinon retuen None
    """
    
    return Utilisateur.query.filter_by(pseudo = pseudo).one_or_none()



def validitor_sign_in(email, password):
    """Validation de l'exisatnce de l'utilisateur

    Args:
        email (String): Email
        password (String): Mot de passe

    Returns:
        Var: True si l'utilisateur existe, String sinon
    """
    
    user = Utilisateur.query.filter_by(adresseMail=email).first()
    if user:
        if check_password_hash(user.password, password):
            return True
    return "Invalid email or password!"


def is_admin(user):
    """Validation de l'utilisateur

    Args:
        user (Objet): L'utilisateur

    Returns:
        Var: True l'utilisateur est un admin, None sinone
    """
    return Utilisateur.query.filter_by(id = user.id).filter_by(id_R = 3).one_or_none()


def is_teacher(user):
    """Validation de l'utilisateur

    Args:
        user (Objet): L'utilisateur

    Returns:
        Var: True l'utilisateur est un prof, None sinone
    """
    return Utilisateur.query.filter_by(id = user.id).filter_by(id_R = 2).one_or_none()

def is_student(user):
    
    """Validation de l'utilisateur

    Args:
        user (Objet): L'utilisateur

    Returns:
        Var: True l'utilisateur est un eleve, None sinone
    """
    return Utilisateur.query.filter_by(id = user.id).filter_by(id_R = 1).one_or_none()



#####################################################################
#####################################################################
#                         GETEURS
#####################################################################
#####################################################################



    
def get_status(email):
    
    """Récupérer l'etat actuil d'une personne

    Args:
        email (String): L'email de l'utilisateur

    Returns:
        bool: True l'utilisateur est en ligne, None sinone
    """
    u = Utilisateur.query.filter_by(adresseMail = email).one()
    return u.est_active


def get_classes_par_prof(prof_id):
    
    """Récupérer la liste des classe qui sont gérées par un prof
    Args:
        prof_id (int): L'id de ce prof

    Returns:
        List<Objet<classe>>: Liste des classes gérées par ce prof
    """
    return Classe.query.filter_by(gerant_id = prof_id).all()





def get_students_list_for_teacher(teacher_id):
    
    """Récupérer la liste des élèves chez un prof

    Args:
        teacher_id (int): L'id de ce prof

    Returns:
        List<objet<Utilisateur>>: Liste des élèves qui sont gérés par ce prof
    """
    classes_liste = Classe.query.filter_by(gerant_id = teacher_id).all()
    student_liste = list()
    for i in classes_liste:
        a = Appartenir.query.filter_by(classe_id = i.id).all() #Une classe appartient à un prof
        if len(a) > 0:
            for j in a:
                user = j.utilisateur
                student_liste.append(user)
    return student_liste



def get_user_role_by_email(email):
    
    """Récupérer Le rôle d'un personne par sont email

    Args:
        email (String): L'email de l'utilisateur

    Returns:
        int: L'id de rôle de cette personne : id_R = 1 : Eleve
                                              id_R = 2 : prof
                                              id_R = 3 : admin
    """
    u = Utilisateur.query.filter_by(adresseMail = email).one()
    return u.id_R



def get_all_teachers_info():
    """Récupérer les informations de tous les profs

    Args:
        None
    Returns:
    List<List<String, String, List<String>, int>> : Une liste d'un liste dans la quelle il y a les informations des prof
                                                    Index 1 : le nom du prof
                                                    Index 2 : l'email du prof
                                                    Index 3 : liste des noms des classes gérées par ce prof
                                                    Index 4 : l'id de ce prof
    """

    users = Utilisateur.query.filter_by(id_R = 2).all() #La liste des prof_stats_eleve
    final_data = list()
    for user in users:
        classes = Classe.query.filter_by(gerant_id = user.id).all()
        final_data.append([user.nom, user.adresseMail, [classe.nomClasse for classe in classes], user.id])
    return final_data


def get_classe_by_eleve(liste_eleve):
    """Récupérer la classe de chaque élève

    Args:
        None
    Returns:
    Dict<Object<Utilisateur>, String> : Une diceonnaire de données compose de:
                                                                             clé : une personne 
                                                                             val : le nom de sa classe
    """
    data = dict()
    for i in liste_eleve:
        ap = Appartenir.query.filter_by(utilisateur_id = i.id).one()
        cl = ap.classe
        data[i] = cl.nomClasse
    return data



def get_year_by_nomClass(nom_class):
    """Récupérer l'année de cette classe

    Args:
        nomClasse (String) : Le nom de la classe en question
    Returns:
        val (String) : l'année de cette classe
        #NOTE A VOIR:
                    On sepose que les noms de classe sont identiques à celle de l'IUT.
                    Exemple: la classe '2A3B'
                            2 : Indique l'année.
                            A : Indique le mot année.
                            A : Indique le groupe.
                            A : Indique le sousgroupe.
    """
    return nom_class[:1]


def get_group_by_nomClass(nom_class):

    """Récupérer le nom de cette classe

    Args:
        nomClasse (String) : Le nom de la classe en question
    Returns:
        val (String) : l'année de cette classe
        #NOTE A VOIR:
                    On sepose que les noms de classe sont identiques à celle de l'IUT.
                    Exemple: la classe '2A3B'
                            2 : Indique l'année.
                            A : Indique le mot année.
                            A : Indique le groupe.
                            A : Indique le sousgroupe.
    """
    return nom_class[2:]



def get_all_classes_info():

    """Récupérer les informations des classes

    Args:
        None
    Returns:
        Var (List<String, String, Objet<Utilisateur>, int>) : la liste dans la quelle il y a les inforamtions des classes
                                                             Index 1 : l'année de la classe
                                                             Index 2 : le nom de la classe
                                                             Index 3 : Une personne
                                                             Index 4 : l'id de la classe
    """


    classes = Classe.query.all()
    final_data = list()
    for classe in classes:
        teacher = Utilisateur.query.filter_by(id = classe.gerant_id).first()
        temp_list = [get_year_by_nomClass(classe.nomClasse), get_group_by_nomClass(classe.nomClasse), teacher, classe.id]
        final_data.append(temp_list)
    return final_data


def get_all_students_info():
    """Récupérer les informations des classes

    Args:
        None
    Returns:
        Var (List<String, String, String, Objet<Classe>, int>) : la liste dans la quelle il y a les inforamtions des classes
                                                       Index 1 : L'image de l'utilisateur
                                                       Index 2 : Le nom de l'utilisateur
                                                       Index 3 : L'email de l'utilisateur
                                                       Index 4 : L'id dde la personne
    """
    
    students = Utilisateur.query.filter_by(id_R = 1).all()
    final_data = list()
    for student in students:
        final_data.append([student.image, student.nom, student.adresseMail, get_class_by_stId(student.id), student.id])
    return final_data
        
        

def get_messages_for_tow_users(user1, user2):

    """Récupérer les message entre deux personnes

    Args:
        user1 (int) :L'id du expediteur de la message
        user2 (int) :L'id du destinataire de la message
    Returns:
        var (tuble(String, String)) : Les message entre des deux personne
    """

    messages1to2 = Message.query.filter_by(expediteur = user1).filter_by(destinataire = user2).all()
    messages2to1 = Message.query.filter_by(expediteur = user1).filter_by(destinataire = user2).all()
    pass #A COMPLITER

def get_info_for_user(id):
    """Récupérer les informations pour une personne

    Args:
        id (int) :L'id de cette personne
    Returns:
        var (Objet<Utilisateur>) : L'objet de cette personne
    """
    return Utilisateur.query.filter_by(id = id).first()
    

def get_list_classes():
    return Classe.query.all()[1:]




def get_class_by_stId(id):
    """Récupérer la classe d'un eleve

    Args:
        id (int) :L'id de cette eleve
    Returns:
        var (String) : Le nom du l'eleve
    """
    ap = Appartenir.query.filter_by(utilisateur_id = id).one_or_none()
    classe_id = ap.classe_id
    classe = Classe.query.filter_by(id = classe_id).one_or_none()
    return classe.nomClasse

def get_teachers_info():

    """Récupérer les informations de les prof

    Args:
        None

    Returns:
        var (Objet<Utilisateur>) : Les information de tous les profs
    """
    return Utilisateur.query.filter_by(id_R = 2).all()


def get_class_by_id(id):

    """Récupérer la classe oar son id

    Args:
        id (int) :L'id de cette classe
    Returns:
        var (Objet<Classe>) : L'objet de cette classe
    """
    return Classe.query.filter_by(id = id).first()


def get_user_by_id(id):

    """Récupérer l'objet d'un eleve par son id

    Args:
        id (int) :L'id de cette eleve
    Returns:
        var (Objet<Utilisateur>) : L'objet de ce eleve
    """

    return Utilisateur.query.filter_by(id = id).first()



def get_score_by_eleve_id(id):

    """Récupérer la score d'un eleve

    Args:
        id (int) :L'id de cette eleve
    Returns:
        var (List<List<int, float>>) : La liste des score d'une persoone
                                     Index 1 : Le nombre de salles débloquées (Entre 0 et 9) pour l'insatnt
                                     Index 2 : Le score obtenu dans cette partie


    #NOTE A VOIR :
                  Si l'eleve n'as damais joué dans cette partie, il aura donc 0, 0

    """

    user = Utilisateur.query.filter_by(id = id).first()
    final_data = list()
    parties = Partie.query.filter_by(scenario_id = 1).filter_by(utilisateur_id = id).all()
    if len(parties) > 0:
        liste_temp = list()
        for i in range(3):
            partie = parties[i]
            if partie:
                nbExoFaites = partie.nbExoFaites
                nbSalleDebloquees = partie.nbSalleDebloquees
                score = partie.notePartie + partie.nbExoFaites + partie.nbSalleDebloquees  /  partie.dureePartie 
                liste_temp = [nbSalleDebloquees, round(score)]
                final_data.append(liste_temp)
            else:
                liste_temp = [0, 0]
                final_data.append(liste_temp)
    else:
        for i in range(3):
            liste_temp = [0, 0]
            final_data.append(liste_temp)
    return final_data
            

def get_score_total_for_eleve(id):
    """Récupérer la score total d'un eleve

    Args:
        id (int) :L'id de cette eleve
    Returns:
        var (int) : Le score total de cet élève


    #NOTE A VOIR :
                  Si l'eleve n'as damais joué dans cette partie, il aura donc 0, 0
                  
    """
    data = get_score_by_eleve_id(id)
    final_score = 0
    for i in range(3):
        final_score += data[i][1]
    return int(final_score)

#####################################################################
#####################################################################
#                         SETEURS
#####################################################################
#####################################################################


def set_status(email, new_status):
    """Modifier l'était actucil de cette élève

    Args:
        email (String) :L'email de cet eleve
        new_status (boolean) :La nouvelle état de cet élève
    Returns:
    None               
    """
    u = Utilisateur.query.filter_by(adresseMail = email).first()
    u.est_active = new_status
    db.session.commit()
    

#####################################################################
#####################################################################
#                         UPDATE
#####################################################################
#####################################################################

def update_user(user_id, new_pseudo, new_email, mdp, img):
    """Modifier de la profile l'utilisateur

    Args:
        user_id (int) :L'id de cet personne
        new_pseudo (String) :Le nouveau pseudo de cet personne
        new_email (String) :Le nouveau email de cet personne
        mdp (String) :Le nouveau mot de passe de cet personne
        img (String) :la nouvelle image de cet personne
    Returns:
        var (bool) : True si c'est possible, False sinon
                          Si les mots de passe sont identiques.
                          Si le schéma de l'image              
    """
    user = Utilisateur.query.filter_by(id=user_id).first()
    if not check_password_hash(user.mdp, mdp):  
        return False
    user.pseudo = new_pseudo
    user.adresseMail = new_email
    if img != None:
        user.image = img
    db.session.commit()
    return True


def delete_user_by_id(id):
    """" Suppression d'une personne

    Args:
        id (int) :L'id de cet personne a supprimer
    Returns:
        None            
    """
    user = Utilisateur.query.filter_by(id = id).one_or_none()
    if user:
        db.session.delete(user)
        db.session.commit()


    
def delete_classe_by_id(id):
    """" Suppression d'une classe

    Args:
        id (int) :L'id de cet classe a supprimer
    Returns:
        None            
    """
    classe = Classe.query.filter_by(id = id).one_or_none()
    if classe:
        db.session.delete(classe)
        db.session.commit()


def changer_classe(student_id, class_id):
    """Modifier la classe d'un élève

    Args:
        student_id (int) :L'id de cet eleve
        class_id (int) :La nouvelle classe pour cet élève
    Returns:
        None               
    """
    print(class_id)
    print(type(class_id))
    ap = Appartenir.query.filter_by(utilisateur_id = student_id).first()
    ap.classe_id = int(class_id)
    db.session.commit()

