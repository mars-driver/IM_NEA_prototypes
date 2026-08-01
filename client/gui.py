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
    client_object = client.ChatClient(server_ip, port, window)
    connected = False
    messages = []

    # --------------------- EVENT LOOP ---------------------
    while not connected:
        event, values = window.read()
        print("event:", event)
        print("values:", values)
        if event == sg.WINDOW_CLOSED:
            client_object.socket.close()
            break
        elif event == "send":
            name = values["-MESSAGE-"]
            client_object.connect(name)
            connected = True
            print("Connected. (gui)")
        print(connected)

    threading.Thread(target=client_object.receive).start()

    while True:
        event, values = window.read()
        print("event:", event, "values:", values)
        if event == sg.WINDOW_CLOSED:
            client_object.socket.close()
            break
        elif event == "send":
            message = values["-MESSAGE-"]
            messages.append((client_object.name, message))
            client_object.send(message)
            update_messages(messages, window)
        elif event == "-RECEIVED-":
            message = values["-RECEIVED-"]
            print("INCOMING MESSAGE:", message)
            messages.append(message)
            update_messages(messages, window)
        print("messages:", messages)

    client_object.socket.close()
    window.close()


def update_messages(messages, window):
    num_rows = 5
    visible_messages = messages[::-1]
    if len(messages) < num_rows:
        for _ in range(num_rows - len(messages)):
            visible_messages.append("")
    visible_messages = visible_messages[:num_rows][::-1]
    for i in range(num_rows):
        row = f"-OUTPUT{i+1}-"
        window[row].update(visible_messages[i])