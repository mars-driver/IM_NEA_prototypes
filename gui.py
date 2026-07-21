import server
import client

# GUI

def proto_GUI_server(server_socket, client_socket, addr):
    messages = []
    while True:
        message_out = input()
        messages.append(message_out)
        server.send_data(client_socket, message_out)
        try:
            message_in = server.receive_data(client_socket)
            messages.append(message_in)
        except:
            print("exception")
        # if len(messages) > 1: window["OUTPUT1"].update(messages[-2])
        # window["OUTPUT2"].update(messages[-2])


def proto_GUI_client(client_socket, server_ip):
    messages = []
    while True:
        message_out = input()
        messages.append(message_out)
        # if len(messages) > 1: window["OUTPUT1"].update(messages[-2])
        # window["OUTPUT2"].update(message_out)
        client.send_data(client_socket, message_out)


# idk what im doing with these
"""
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

def proto_GUI_connect_to_server(server_ip): # NOT IN USE
    layout = [[sg.Button("CONNECT to server")],
              [sg.Button("quit")]]
    window = sg.Window("CONNECT", layout)
    event, values = window.read()
    while True:
        if event == "CONNECT":
            server_socket, client_socket, addr = server.connect()
            proto_GUI_client(client_socket, server_ip)
            event = "quit"
        if event == sg.WINDOW_CLOSED or event == "quit":
            break
"""