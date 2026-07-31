import PySimpleGUI as sg
import threading
from server import run_server, new_client

def proto_GUI_server(port):

    # window creation
    layout = [[sg.VPush()],
              [sg.Text("THIS IS THE SERVER")],
              [sg.Text("Server address:"), sg.Text("", key="-ADDRESS-")],
              [sg.Text("Message log:")],
              [sg.Text(size=(40, 1), key="-OUTPUT1-")],
              [sg.Text(size=(40, 1), key="-OUTPUT2-")],
              [sg.VPush()]]
    window = sg.Window("PROTO server", layout, resizable=True, element_justification="center")

    # initialising & running server
    clients = {}
    messages = []
    server_address, server = run_server(port, window)
    #window.start_thread(lambda: receive(server, clients, start_handle_thread, window), ("-THREAD-", "-THREAD ENDED-"))
    #receive(server, clients, start_handle_thread, window)
    newclient_thread = threading.Thread(target=new_client, args=(server, clients, window))
    newclient_thread.start()

    # --------------------- EVENT LOOP ---------------------
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event[0] == "-THREAD-":
            if event[1] == "SEND MESSAGE":
                event_key = (event[0], event[1])
                message = values[event_key]
                messages = update_display(message, messages, window)
        elif event == "-PRINT-":
            message = "".join(values["-PRINT-"])
            update_display(message, messages, window)


def update_display(message, messages, window):
    messages.append(message)
    if len(messages) == 1:
        window["-OUTPUT1-"].update(message)
    else:
        window["-OUTPUT1-"].update(messages[-2])
        window["-OUTPUT2-"].update(messages[-1])
    return messages

# threading !

"""

def handle(client, clients, window):
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast(message.encode(), clients)
            window.write_event_value(("-THREAD-", "SEND MESSAGE"), message)
        except:
            broadcast(f"{clients[client].name} left the chat".encode(), clients)
            clients.pop(client)
            break

def start_handle_thread(client, clients, window):
    handle_thread = threading.Thread(target=handle, args=(client, clients, window))
    handle_thread.start()
    #window.start_thread(lambda: handle(client, clients, window), ("-THREAD-", "-THREAD ENDED-"))
    
"""




















"""
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
"""