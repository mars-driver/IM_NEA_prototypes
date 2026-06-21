import PySimpleGUI as sg # library for GUI
import log_in

# GUI
def proto_GUI_login(accounts):
    layout = [[sg.Text("Log In")],
              [sg.Text("enter username:")],
              [sg.Input(key="USERNAME")],
              [sg.Text("enter password:")],
              [sg.Input(key="PASSWORD")],
              [sg.Button("forgot password")],
              [sg.Text(size=(40, 1), key="OUTPUT")],
              [sg.Button("ok"), sg.Button("quit")]]
    window = sg.Window("PROTO log in", layout)
    while True:
        success = False
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'quit':
            break
        if event == "ok":
            success = log_in.proto_log_in(values.values(), accounts)
            if success == True:
                window["OUTPUT"].update("log in successful!")
                print("Success")
                return values
            else:
                window["OUTPUT"].update(success)