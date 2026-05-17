# prototype to test signing up

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

# GUI
def proto_GUI_signup():
    layout = [[sg.Text("enter username:")],
              [sg.Input(key="USERNAME")],
              [sg.Text("enter email address:")],
              [sg.Input(key="EMAIL")],
              [sg.Text("enter password:")],
              [sg.Input(key="PASSWORD")],
              [sg.Text(size=(40, 1), key="OUTPUT")],
              [sg.Button("ok"), sg.Button("quit")]]
    window = sg.Window("PROTO sign up", layout)
    while True:
        success = False
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'quit':
            break
        if event == "ok":
            success = proto_sign_up(values.values())
            if success == True:
                window["OUTPUT"].update("sign up successful!")
                print("Success")
                return values
            else:
                window["OUTPUT"].update(success)

def proto_sign_up(values):
    username, email, password = values
    while proto_valid_new_username(username, accounts) == False:
         return "Username invalid."
    while proto_valid_email(email) == False:
        return "Email address invalid."
    while proto_valid_password(password) == False:
        return "Password invalid."
    return True

# test data
accounts = ["existinguser1", "janeSmith123", "marsjdriver"] # this represents my database
print(proto_GUI_signup())