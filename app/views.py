from datetime import timedelta
from flask import Flask, render_template, flash, redirect, request, url_for, session
from flask_login import UserMixin, login_user, current_user, logout_user, login_required
import os
from os.path import join, dirname, realpath
from .static.python.password_generate import generate_random_password
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.request
from .models import Role, Utilisateur, Classe, Appartenir, Message, Scenario, Partie, Carte, Contient, Exercice, Tileset, Piece, Contien, Cacher
from .static.python.info_validate import *
from .app import app ,db
from .functions import is_admin, is_student, is_teacher, new_exo, new_user, init_role_ids, valiation_pseudo, validitor_sign_in, set_status, get_status, new_class, get_classes_par_prof,\
    __run_db__, __drop_db__, __create_db__, __init_db__, __test_db__, get_students_list_for_teacher, get_students_list_for_teacher, new_relationship_class_user, get_user_role_by_email,\
    get_all_teachers_info, update_user, get_classe_by_eleve, delete_user_by_id, get_year_by_nomClass, get_group_by_nomClass, get_all_classes_info, get_all_students_info, get_class_by_stId,\
    get_teachers_info, delete_classe_by_id, get_messages_for_tow_users, get_info_for_user, get_user_by_id, get_list_classes, changer_classe, get_class_by_id, get_user_by_id, get_score_by_eleve_id,\
    get_score_total_for_eleve


app = Flask(__name__)
app.config.from_object('config')







#####################################################################
#####################################################################
#                              AUTH
#####################################################################
#####################################################################


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    return_data = { 'email' : '', 'full_name' : '', 'pseudo' : ''}
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        pseudo = request.form.get('pseudo')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        
        return_data['email'] = email
        return_data['full_name'] = full_name
        return_data['pseudo'] = pseudo
        print(return_data)
        print(full_name)
        
        
        user = Utilisateur.query.filter_by(adresseMail=email).one_or_none()
        if user:
            return render_template("sign_up.html", title="Sign up", status="Email already exist", return_data = return_data)
        elif validitor_sign_up(full_name, pseudo, email, password1, password2) != True:
            return render_template("sign_up.html", title="Sign up", status=validitor_sign_up(full_name, pseudo, email, password1, password2), return_data = return_data)
        elif valiation_pseudo(pseudo):
            return render_template("sign_up.html", title="Sign up", status="Pseudo already exist.", return_data = return_data)
        else:
            new_user(pseudo, full_name, email, generate_password_hash(password1, method='sha256'))
            
            user = Utilisateur.query.filter_by(adresseMail = email).one_or_none()
            if user:
                #login_user(user, remember=True, duration=timedelta(hours=1))
                login_user(user)
                set_status(current_user.adresseMail, True)
            return redirect(url_for('home'))
    return render_template("sign_up.html", title="Create an account", return_data = return_data)

@app.route('/connexion', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember-me')
        
        user = Utilisateur.query.filter_by(adresseMail=email).one_or_none()
        if user != None:
            if check_password_hash(user.mdp, password):
                if remember_me:
                    login_user(user, remember=True, duration=timedelta(hours=1))
                else:
                    login_user(user)
                #login_user(user)
                set_status(current_user.adresseMail, True)
                return redirect(url_for('home'))
        return render_template("login.html", title="Login", status="Invalid email or password!")
    return render_template("login.html", title="Login")

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="Login or signup")


@app.route('/home', methods=['GET', 'POST'])
@app.route('/main', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.id_R == 1: #current_user is student
        return redirect(url_for('main_page_eleve'))
    
    
    elif current_user.id_R == 2: #current_user is teacher
        return redirect(url_for('main_page_prof'))
    
    
    elif current_user.id_R == 3:#current_user is admin
        return redirect(url_for('main_page_admin'))

@app.route('/logout')
@login_required
def logout():
    set_status(current_user.adresseMail, False)
    logout_user()
    return redirect(url_for('index'))



#####################################################################
#####################################################################
#                              ELEVE
#####################################################################
#####################################################################







@app.route('/main/students', methods=['GET', 'POST'])
@login_required
def main_page_eleve():
    if not is_student(current_user):
        return redirect(url_for('home'))
    return render_template('main_page_eleve.html', tittre="Main page")


@app.route('/student/stats', methods=['GET', 'POST'])
@login_required
def stats_eleve():
    if not is_student(current_user):
        return redirect(url_for('home'))
    return render_template(
        'stats_eleve.html',
        tittre="Stats Students",
        user = current_user,
        data = get_score_by_eleve_id(current_user.id),
        score_total = get_score_total_for_eleve(current_user.id))
    

UPLOAD_FOLDER = join(dirname(realpath(__file__)), "static/images/users_images")
ALLOWED_EXTENSIONS = {"png","jpg","jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/student/profil/edit', methods=['GET', 'POST'])
@login_required
def editProfil_eleve():
    if not is_student(current_user):
        return redirect(url_for('home'))
    main_edit_profile()
    return render_template('editProfil.html', title="Edit Profile", error_msg="")

def main_edit_profile():
    if request.method == 'POST':
        pseudo = request.form.get('fname')
        email = request.form.get('email')
        mdp = request.form.get('password')
        filename = None
        if current_user.pseudo != pseudo:
            if valid_user(pseudo) != True:
                return render_template('editProfil.html', title="Edit Profile", error_msg=valid_user(pseudo))
            if valiation_pseudo(pseudo):
                return render_template("editProfil.html", title="Edit Profile", error_msg="Pseudo already exist.")
        if current_user.adresseMail != email:
            if valid_email(email) != True:
                return render_template('editProfil.html', title="Edit Profile", error_msg=valid_email(email))
        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "":
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    if update_user(current_user.id, pseudo, email, mdp, filename):
                        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                        return render_template('editProfil.html', title="Edit Profile", error_msg="Information was changed successfully.")
        if update_user(current_user.id, pseudo, email, mdp, filename):
            return render_template('editProfil.html', title="Edit Profile", error_msg="Information was changed successfully.")
        return render_template('editProfil.html', title="Edit Profile", error_msg="Invalid information. Please try again.")
    
    
    

#####################################################################
#####################################################################
#                              PROF
#####################################################################
#####################################################################



@app.route('/main/teacher', methods=['GET', 'POST'])
@login_required
def main_page_prof():
    if not is_teacher(current_user):
        return redirect(url_for('home'))
    return render_template('main_page_prof.html', tittre="Main Page")




@app.route('/teacher/profil/edit/', methods=['GET', 'POST'])
@login_required
def editProfil_prof():
    if not is_teacher(current_user):
        return redirect(url_for('home'))
    main_edit_profile()
    return render_template('editProfil.html', title="Edit Profile", error_msg="")






@app.route('/teacher/stats/students/list', methods=['GET', 'POST'])
@login_required
def prof_eleves_liste():
    if not is_teacher(current_user):
        return redirect(url_for('home'))
    return render_template('students_list_prof.html', datas = get_classe_by_eleve(get_students_list_for_teacher(current_user.id)), tittre="Students List")






#unused
@app.route('/teacher/stats/students/id=<int:id_student>', methods=['GET', 'POST'])
@login_required
def prof_stats_eleve(id_student):
    if not is_teacher(current_user):
        return redirect(url_for('home'))
    return render_template(
        'stats_eleve.html',
        tittre="Stats Students",
        user = get_user_by_id(id_student),
        data = get_score_by_eleve_id(id_student),
        score_total = get_score_total_for_eleve(id_student))





#unused
@app.route('/teacher/stats/students', methods=['GET', 'POST'])
@login_required
def prof_contact_admin():
    return render_template('contact_admin.html', title="Stats Students")


#####################################################################
#####################################################################
#                              ADMIN
#####################################################################
#####################################################################






@app.route('/main/admin', methods=['GET', 'POST'])
@login_required
def main_page_admin():
    if not is_admin(current_user):
        return redirect(url_for('home'))
    return render_template('main_page_admin.html', tittre="Main Page")





@app.route('/admin/teacher/add', methods=['GET', 'POST'])
@login_required
def addTecher_admin():
    if not is_admin(current_user):
        return redirect(url_for('home'))
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        mdp = request.form.get('password')
        this_user = current_user
        user = Utilisateur.query.filter_by(adresseMail = email).one_or_none()
        if user == None:
            id_prof = Utilisateur.query.order_by(Utilisateur.id).first().id + 1
        
            new_user(fname +""+lname+str(id_prof), fname +" "+lname, email, mdp, id_R = 2) #id_R = 2 means that this user is a teacher
            return redirect(url_for('main_page_admin'))
        else:
           return render_template('addTecher_admin.html', title="Add Techer", error_msg="This email is already in use.",generate_random_password = generate_random_password(leng=10)) # If the email is already in db 
    return render_template('addTecher_admin.html', title="Add Techer", error_msg="",generate_random_password = generate_random_password(leng=10))






@app.route('/admin/add/class', methods=['GET', 'POST'])
@login_required
def addClass_admin():
    if not is_admin(current_user):
        return redirect(url_for('home'))
    if request.method == 'POST':
        class_name = request.form.get('className')
        teacher_name = request.form.get('teacher')
        new_class(class_name, teacher_name)
        return redirect(url_for('main_page_admin'))
    return render_template('addClass_admin.html', tittre="Add Class", teachers_list = get_teachers_info())


@app.route('/admin/delete/student/id=<int:id_student>', methods=['GET', 'POST'])
@login_required
def deleteStudent_admin(id_student):
    if not is_admin(current_user):
        return redirect(url_for('home'))
    return render_template('deleteStudent_admin.html', tittre="Delete Student", students_list = get_students_list())


@app.route('/admin/delete/students/list', methods=['GET', 'POST'])
@login_required
def studentList_admin():
    if not is_admin(current_user):
        return redirect(url_for('home'))
    return render_template('students_list_prof.html', tittre="Delete Student", data = get_all_teachers_info())





@app.route('/main/list_admin/<string:list_type>', methods=['GET', 'POST'])
@login_required
def List_admin(list_type):
    """

    Args:
        list_type (_type_): type de page

    Returns:
        une algo trop compliquer à comprendre 'IMPOSSIBLE DU COMPRENDRE!!!!!!'
    """
    if not is_admin(current_user):
        return redirect(url_for('home'))
    elements = list()
    dico={"teacher":{"title":"Teachers list","ths":["Full name","Email","Classes","Actions"]},
          "class":{"title":"Classes list","ths":["Year","Group","Teachers","Actions"]},
          "student":{"title":"Students list","ths":["","Full name","Email","Group","Actions"]}
          }
    if list_type == "class":
        elements = get_all_classes_info()
    
    elif list_type == "teacher":
        elements = get_all_teachers_info()
    
    elif list_type == "student":
        elements = get_all_students_info()
            

    return render_template('List_admin.html',
                            title=dico[list_type]["title"],
                            list_type=list_type,
                            ths=dico[list_type]["ths"],
                            elements=elements)
 
 

@app.route('/admin/delete/person/id=<int:id>', methods=['GET', 'POST'])
@login_required
def delete_person(id):
    if not is_admin(current_user):
        return redirect(url_for('home'))
    delete_user_by_id(id)
    return redirect(url_for('home', list_type = "teacher"))


@app.route('/admin/delete/class/id=<int:id>', methods=['GET', 'POST'])
@login_required
def delete_class(id):
    if not is_admin(current_user):
        return redirect(url_for('home'))
    delete_classe_by_id(id)
    return redirect(url_for('List_admin', list_type = "class"))



@app.route('/admin/add/student/<int:student_id>/class', methods=['GET', 'POST'])
@login_required
def add_student(student_id):
    if not is_admin(current_user):
        return redirect(url_for('home'))
    if request.method == 'POST':
        class_id = request.form.get('classe')
        changer_classe(student_id, get_class_by_id(class_id).id)
        return redirect(url_for('main_page_admin'))

    return render_template(
        "add_student_to_class.html",
        title="Add student to class",
        student = get_info_for_user(student_id),
        classes_list = get_list_classes(),
        error_msg = "")


@app.route('/jeu', methods=['GET', 'POST'])
@login_required
def jeu():
    return render_template("../static/Build_Game/Build Game/public/index.html")