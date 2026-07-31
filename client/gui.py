import PySimpleGUI as sg
import threading
import client

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
                  sg.Push(), sg.Text("Type message here:", size=(15, 1)),
                  sg.Input(size=(15, 1), key="-MESSAGE-"), sg.Button("send", bind_return_key=True),
                  sg.Push()
              ],
              [sg.VPush()]]

    window = sg.Window("PROTO server", layout, resizable=True, element_justification="center")

    # ----------------- RUNNING THE CLIENT -----------------
    client_socket = client.run_client(server_ip, port)

    # --------------------- EVENT LOOP ---------------------
    while True:
        event, values = window.read()
        print("event:", event)
        print("values:", values)
        if event == sg.WINDOW_CLOSED:
            break

    client_socket.close()
    window.close()