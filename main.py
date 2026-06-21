# prototype to test signing up

import gui
import re # regex module to assist with validity checks
import PySimpleGUI as sg # library for GUI

def proto_valid_new_username(newUsername, accounts):
    return newUsername.isalnum() and newUsername not in accounts

def proto_valid_email(newEmail):
    newEmail = newEmail.split("@")
    if len(newEmail) != 2:
        return False
    if "." not in newEmail[1]:
        return False
    return True

def proto_valid_password(newPassword):
    if (len(newPassword) >= 8
        and re.search("[a-z]", newPassword)
        and re.search("[A-Z]", newPassword)
        and re.search("[0-9]", newPassword)
        and re.search("[`!\"£$%^&*()_+{}\[\]~:;@'|<,>.?/]", newPassword)):
        return True
    return False

def proto_sign_up(values):
    username, email, password = values
    while proto_valid_new_username(username, accounts) == False:
         return "Username invalid."
    while proto_valid_email(email) == False:
        return "Email address invalid."
    while proto_valid_password(password) == False:
        return "Password invalid."
    return "Sign up successful."

# test data
accounts = ["existinguser1", "janeSmith123", "marsjdriver"] # this represents my database
print(proto_GUI_signup())