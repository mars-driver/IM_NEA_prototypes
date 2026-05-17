# prototype to test signing up

import re # regex module to assist with validity checks
import PySimpleGUI as sg # library for GUI
import hashlib
import secrets

def proto_username_exists(newUsername, accounts):
    return newUsername in accounts

def proto_correct_password(account, newPassword):
    correctPassword = account.hashedpassword
    newPassword = str(hashlib.sha256((newPassword + account.salt).encode()).hexdigest())
    return newPassword == correctPassword

def proto_is_locked(account):
    return account.locked

# GUI
def proto_GUI_login():
    layout = [[sg.Text("enter username:")],
              [sg.Input(key="USERNAME")],
              [sg.Text("enter password:")],
              [sg.Input(key="PASSWORD")],
              [sg.Text(size=(40, 1), key="OUTPUT")],
              [sg.Button("ok"), sg.Button("quit")]]
    window = sg.Window("PROTO log in", layout)
    while True:
        success = False
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'quit':
            break
        if event == "ok":
            success = proto_log_in(values.values())
            if success == True:
                window["OUTPUT"].update("log in successful!")
                print("Success")
                return values
            else:
                window["OUTPUT"].update(success)

def proto_log_in(values):
    username, password = values
    if proto_username_exists(username, accounts) == False:
         return "Username invalid."
    if proto_correct_password(accounts[username], password) == False:
        return "Password invalid."
    if proto_is_locked(accounts[username]) == True:
        return "Account locked."
    return True

# test data

class Account:
    def __init__(self, newUsername, newHashedPassword, newSalt, newLocked):
        self.username = newUsername
        self.hashedpassword = newHashedPassword
        self.salt = newSalt
        self.locked = newLocked

# this represents my database
accounts = {
    "existinguser1": Account("existinguser1", "2adab35acedea9f643c441921a70156c1280860ab22db8d85a9a2f5dc1f07776", "31975e6429893d51f4eeecd793dc4235", False), # password: correctPassw0rd!
    "janeSmith123": Account("janeSmith123", "61dbb73c56a7b89c7eda3fc7a71f5ebb6d3962b4450da2bcfb3c51807cf70c9a", "a2597646e630b7905301ed9495f55796",True), # password: super_Secure123
    "marsjdriver": Account("marsjdriver", "f611bf33a30e39a21d3cd46bfe1e0bbde2179769f9c79d97a776520b86553e0b", "eff83ac16979a3737bc1d0501a9b6a73", False) # password: Tp1tmlltwfmiatsnwy!mb
}

print(proto_GUI_login())
