import PySimpleGUI as sg
import threading
from server import CustomThread, connect, run_server, receive

def proto_GUI_server(port):

    clients = {}
    server_address, server = run_server(port)
    print("connected.")  # todo

    layout = [[sg.VPush()],
              [sg.Text("THIS IS THE SERVER")],
              [sg.Text("Server address:"), sg.Text(server_address)],
              [sg.Text("Message log:")],
              [sg.Text(size=(40, 1), key="OUTPUT1")],
              [sg.Text(size=(40, 1), key="OUTPUT2")],
              [sg.VPush()]]
    window = sg.Window("PROTO server", layout, resizable=True, element_justification="center")

    while True:
        event, values = window.read(timeout=100)
        #client, address, name, clients = receive(server, clients)
        receive_thread = CustomThread(target=receive, args=(server, clients))
        receive_thread.start()
        #return_values = receive_thread.join() # WHY
        print(receive_thread.join()) #todo
        print("values printed")

        #message, clients = server.handle(client, clients)
        if event == sg.WINDOW_CLOSED:
            break




























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