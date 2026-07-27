import PySimpleGUI as sg
import threading
from server import connect, run_server, receive, broadcast

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
    server_address, server = run_server(port)
    receive(server, clients, start_handle_thread, window)

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



# threading !

def handle_thread(client, clients, window):
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast(message.encode(), clients)
            window.write_event_value(('-THREAD-', 'SEND MESSAGE'), message)
        except:
            broadcast(f"{clients[client].name} left the chat".encode(), clients)
            clients.pop(client)
            break

def start_handle_thread(client, clients, window):
    window.start_thread(lambda: handle_thread(client, clients, window), ('-THREAD-', '-THREAD ENDED-'))

def update_display(message, messages, window):
    messages.append(message)
    if len(messages) == 1:
        window["-OUTPUT1-"].update(message)
    else:
        window["-OUTPUT1-"].update(messages[-2])
        window["-OUTPUT2-"].update(messages[-1])
    return messages