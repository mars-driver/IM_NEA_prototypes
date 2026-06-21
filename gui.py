import sign_up
import PySimpleGUI as sg # library for GUI

# GUI
def proto_GUI_signup(accounts):
    layout = [[sg.Text("Sign Up")],
              [sg.Text("enter username:")],
              [sg.Input(key="USERNAME")],
              [sg.Text("enter email address:")],
              [sg.Input(key="EMAIL")],
              [sg.Text("enter password:")],
              [sg.Input(key="PASSWORD")],
              [sg.Text(size=(40, 1), key="OUTPUT")],
              [sg.Text("Already have an account?"), sg.Button("log in")],
              [sg.Button("ok"), sg.Button("quit")]]
    window = sg.Window("PROTO sign up", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'quit':
            break
        if event == "ok":
            result = sign_up.proto_sign_up(values.values(), accounts)
            window["OUTPUT"].update(result)