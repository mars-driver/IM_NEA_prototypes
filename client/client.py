import socket
import threading

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None

    def _input_and_send_loop(self):
        while True:
            message = f"{self.name}: {input()}"
            print(message)
            self.socket.send(message.encode("utf8"))

    def connect(self):
        self.socket.connect((self.host, self.port))
        name = input("Enter your name: ")
        self.name = name
        threading.Thread(target=self._input_and_send_loop).start()
        while True:
            message = self.socket.recv(1024).decode("utf8")
            if message == "NAME":
                self.socket.send(name.encode("utf8"))
            else:
                print(message)