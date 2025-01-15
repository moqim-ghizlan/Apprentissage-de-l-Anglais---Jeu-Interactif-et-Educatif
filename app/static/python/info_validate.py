import re

def valid_full_name(full_name):
    cpt = 0
    if len(full_name) > 32 or len(full_name) < 2:
        return "You must use your real name, Ex : 'Jhon Smith'."
    if full_name[0] == " " or full_name[len(full_name)-1] == " ":
        return "You must use your real name, Ex : 'Jhon Smith'."
    if " " not in full_name:
        return "You must enter your first name + spaces + last name, Ex : 'Jhon Smith'."
    for i in full_name:
        if i == " ":
            cpt +=1
    if cpt > 3:
        return "You must use your real name, Ex : 'Jhon Smith'."
    return True
    

def valid_user(user):
    cpt = 0
    if len(user) < 6:
        return "Username must be at least 6 letters or numbers, Ex : 'Jh0n.Smith' ."
    for i in user:
        if i.isalpha():
            cpt += 1
    if cpt == 0:
        return "Username must have at least one letter : EX : Jhon.15 ."
    else:
        return True


def valid_email(email):
    if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
        return True
    else:
        return "Invalid Email. You must enter a valide email"


def validitor_sign_up(full_name, user, email, password1, password2):
    if valid_full_name(full_name) != True :
        return valid_full_name(full_name)
    elif valid_user(user) != True:
        return valid_user(user)
    elif valid_email(email) != True:
        return valid_email(email)
    elif password_check(password1, password2) != True:
        return password_check(password1, password2)
    else:
        return True
    
def password_check(passwd1, passwd2):
    #SpecialSym =['$', '@', '#', '%']
    if passwd1 != passwd2:
        return f"Passwords doesn't match"
    elif len(passwd1) < 8:
        return 'Length should be at least 8 characters'
    elif len(passwd1) > 36:
        return 'Length should be not be greater than 36 characters'
    elif not any(char.isdigit() for char in passwd1):
        return 'Password should have at least one numeral'
    elif not any(char.isupper() for char in passwd1):
        return 'Password should have at least one uppercase letter'
    elif not any(char.islower() for char in passwd1):
        return 'Password should have at least one lowercase letter'
    #elif not any(char in SpecialSym for char in passwd1):
    #    return 'Password should have at least one of the symbols $@#'
    return True
