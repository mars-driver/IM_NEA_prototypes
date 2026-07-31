import PySimpleGUI as sg
import client
import threading

def proto_GUI_client(server_ip, port):

    # ------------------- WINDOW CREATION ------------------
    layout = [[sg.VPush()],
              [sg.Text("THIS IS THE CLIENT")],
              [sg.Text("Server address:"), sg.Text("", key="-ADDRESS-")],
              [sg.Text(size=(40, 1), key="-OUTPUT1-")],
              [sg.Text(size=(40, 1), key="-OUTPUT2-")],
              [sg.Text(size=(40, 1), key="-OUTPUT3-")],
              [sg.Text(size=(40, 1), key="-OUTPUT4-")],
              [sg.Text(size=(40, 1), key="-OUTPUT5-")],
              [
                  sg.Push(), sg.Text("Enter your name:", size=(15, 1)),
                  sg.Input(size=(15, 1), key="-MESSAGE-"), sg.Button("send", bind_return_key=True),
                  sg.Push()
              ],
              [sg.VPush()]]

    window = sg.Window("PROTO server", layout, resizable=True, element_justification="center")

    # ----------------- RUNNING THE CLIENT -----------------
    client_object = client.ChatClient(server_ip, port)
    client_object.window = window
    connected = False
    messages = []
    #client_object.connect()

    # --------------------- EVENT LOOP ---------------------
    while not connected:
        event, values = window.read(timeout=100)
        print("event:", event)
        print("values:", values)
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "send":
            name = values["-MESSAGE-"]
            client_object.connect(name)
            connected = True
        elif event == "-CONNECTED-":
            connected = True
            print("Connected. (gui)")
        print(connected)

    client_object.start_threads(name)

    while True:
        event, values = window.read(timeout=100)
        print("event:", event)
        print("values:", values)
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "send":
            message = values["-MESSAGE-"]
            messages.append(message)
            client_object.send(message)

    window.close()