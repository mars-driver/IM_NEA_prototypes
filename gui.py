import PySimpleGUI as sg
import server

# GUI

def proto_GUI_connect():
    layout = [[sg.Button("CONNECT")],
              [sg.Button("quit")]]
    window = sg.Window("CONNECT", layout)
    event, values = window.read()
    while True:
        if event == "CONNECT":
            server_socket, client_socket, addr = server.connect()
            proto_GUI_server(server_socket, client_socket, addr)
            event = "quit"
        if event == sg.WINDOW_CLOSED or event == "quit":
            break

def proto_GUI_server(server_socket, client_socket, addr):
    layout = [[sg.Text(addr)],
              [sg.Text(size=(40, 1), key="OUTPUT1")],
              [sg.Text(size=(40, 1), key="OUTPUT2")],
              [sg.Text("Type message here: ")],
              [sg.Input(key="MESSAGE OUT")],
              [sg.Button("send"), sg.Button("quit")]
              ]
    window = sg.Window("PROTO server", layout, resizable=True)
    messages = []
    while True:
        event, values = window.read()
        if event == "send":
            message_out = values["MESSAGE OUT"]
            messages.append(message_out)
            if len(messages) > 1: window["OUTPUT1"].update(messages[-2])
            window["OUTPUT2"].update(message_out)
            server.send_data(client_socket, message_out)
        if event == sg.WINDOW_CLOSED or event == "quit":
            server.close_connection(client_socket)
            server.close_connection(server_socket)
            break