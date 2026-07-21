import PySimpleGUI as sg
import server

# GUI

def proto_GUI_server(server_socket, client_socket, addr):
    layout = [[sg.Text("THIS IS THE SERVER")],
              [sg.Text(addr)],
              [sg.Text(size=(40, 1), key="OUTPUT1")],
              [sg.Text(size=(40, 1), key="OUTPUT2")],
              [sg.Text("Type message here: ")],
              [sg.Input(key="MESSAGE OUT")],
              [sg.Button("send"), sg.Button("quit")]]
    window = sg.Window("PROTO server", layout, resizable=True)
    messages = []
    while True:
        event, values = window.read()
        if event == "send":
            message_out = values["MESSAGE OUT"]
            messages.append(message_out)
            server.send_data(client_socket, message_out)
        if event == sg.WINDOW_CLOSED or event == "quit":
            break
        try:
            message_in = server.receive_data(client_socket)
            messages.append(message_in)
        except:
            print("exception")
        if len(messages) > 1: window["OUTPUT1"].update(messages[-2])
        window["OUTPUT2"].update(messages[-2])



# idk what im doing with these
def proto_GUI_connect_to_client(): #NOT IN USE
    layout = [[sg.Button(f"CONNECT to client")],
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