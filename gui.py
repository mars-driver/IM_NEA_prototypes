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