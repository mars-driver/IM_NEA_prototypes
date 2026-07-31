import socket
import threading

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.window = None

    def send(self, message):
        message_out = f"{self.name}: {message}"
        self.socket.send(message_out.encode("utf8"))
        return message

    def connect(self, name):
        self.socket.connect((self.host, self.port))
        self.name = name

    def receive(self, name):
        message = self.socket.recv(1024).decode("utf8")
        if message == "NAME":
            self.socket.send(name.encode("utf8"))
            print("Connected.")
            self.window.write_event_value("-CONNECTED-", "")
        else:
            print(message)

    def start_threads(self, name):
        threading.Thread(target=self.receive, args=(name,)).start()

    def close(self):
        self.socket.close()