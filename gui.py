import sign_up
import PySimpleGUI as sg # library for GUI

# GUI
def proto_GUI_signup(accounts):
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
            success = sign_up.proto_sign_up(values.values(), accounts)
            if success == True:
                window["OUTPUT"].update("sign up successful!")
                print("Success")
                return values
            else:
                window["OUTPUT"].update(success)