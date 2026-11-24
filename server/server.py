import socket
import selectors
import cbor2
import server_encryption

class Client:
    def __init__(self):
        self.__encryption_cipher = None
        self.__name = None
        self.__current_room_id = None

    def get_encryption_cipher(self):
        return self.__encryption_cipher
    def get_name(self):
        return self.__name
    def get_current_room_id(self):
        return self.__current_room_id
    def set_encryption_cipher(self, new_encryption_cipher):
        self.__encryption_cipher = new_encryption_cipher
    def set_name(self, new_name):
        self.__name = new_name
    def set_current_room_id(self, new_room_id):
        self.__current_room_id = new_room_id
        

class ChatRoom:
    def __init__(self, new_room_id, new_name, new_host):
        self.__room_id = new_room_id
        self.__name = new_name
        self.__host = new_host
        self.__members = []

    def get_room_id(self):
        return self.__room_id
    def get_name(self):
        return self.__name
    def get_host(self):
        return self.__host
    def get_members(self):
        return self.__members
    def add_member(self, new_user):
        self.__members.append(new_user)
    def remove_member(self, old_user):
        self.__members.remove(old_user)

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.clients = {}
        self.chatrooms = {}
        self.read_selector = selectors.DefaultSelector()
        self.write_selector = selectors.DefaultSelector()

    def init_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server is listening on port {self.port}...")
        self.read_selector.register(self.socket, selectors.EVENT_READ, self.accept_connection)

    def accept_connection(self, server_socket):
        client_socket, address = server_socket.accept()
        print(f"Connected with {str(address)}")
        print("Registering client...")

        self.clients[client_socket] = Client()
        client_object = self.clients[client_socket]
        self.read_selector.register(client_socket, selectors.EVENT_READ, self.receive_message)
        self.write_selector.register(client_socket, selectors.EVENT_WRITE)

        # exchanging of keys
        key_bytes = client_socket.recv(1024)
        key_dict = cbor2.loads(key_bytes)
        assert key_dict["message_type"] == "-KEY-"
        client_public_key_string = key_dict["client_public_key_string"]
        client_public_key = server_encryption.string_to_key(client_public_key_string)
        server_private_key, server_public_key, signature = server_encryption.initial_connection(client_public_key)
        message_bytes = message_to_bytes("-SERVER-KEYS-", {
            "server_public_key_string": server_encryption.key_to_string(server_public_key),
            "signature": signature
        })
        client_socket.send(message_bytes)
        encryption_cipher = server_encryption.generate_cipher(server_private_key, client_public_key)
        client_object.set_encryption_cipher(encryption_cipher)
        print("Encryption key established.")


    def receive_message(self, client_socket):
        client_object = self.clients[client_socket]
        client_encryption_cipher = client_object.get_encryption_cipher()
        message_dict = receive_and_decrypt(client_socket, client_encryption_cipher)
        message_type = message_dict["message_type"]

        if message_type == "-TEXT-":
            room_id = client_object.get_current_room_id()
            self.broadcast(client_socket, cbor2.dumps(message_dict), room_id)

        elif message_type == "-USERNAME-":
            username = message_dict["username"]
            client_object.set_name(username)
            print("Client's username is", username)

        elif message_type == "-LEAVE-ROOM-":
            name = client_object.get_name()
            room_id = client_object.get_current_room_id()
            room_object = self.chatrooms[room_id]
            room_object.remove_member(client_socket)
            message_bytes = message_to_bytes("-DISCONNECT-", {"user": name})
            self.broadcast(client_socket, message_bytes, room_id)
            client_object.set_current_room_id(None)
            print(name, "left room", room_id)

        elif message_type == "-CURRENT-ROOM-ID-":
            room_id = message_dict["room_id"]
            client_object.set_current_room_id(room_id)
            if room_id is not None:
                room_object = self.chatrooms[room_id]
                room_object.add_member(client_socket)
                client_name = client_object.get_name()
                message_bytes = message_to_bytes("-JOIN-", {"user": client_name})
                self.broadcast(client_socket, message_bytes, room_id)
            print(client_object.get_name(), "joined room", client_object.get_current_room_id())

        elif message_type == "-GET-ROOM-ID-":
            room_id = client_object.get_current_room_id()
            message_bytes = message_to_bytes("-ROOM-ID-", {"room_id": room_id})
            encrypt_and_send(client_socket, message_bytes, client_encryption_cipher)

        elif message_type == "-ROOM-DETAILS-":
            room_id = client_object.get_current_room_id()
            room_dict = self.get_room_details(room_id)
            message_bytes = message_to_bytes("-ROOM-DETAILS-", {"room_dict": room_dict})
            encrypt_and_send(client_socket, message_bytes, client_encryption_cipher)

        elif message_type == "-CHATROOMS-":
            print("sending chatrooms to client", client_object.get_name())
            chatrooms_list = []
            for room in self.chatrooms.values(): # list of chatroom objects
                room_id = room.get_room_id()
                room_dict = self.get_room_details(room_id)
                chatrooms_list.append(room_dict)
            message_bytes = message_to_bytes("-CHATROOMS-", {"chatrooms": chatrooms_list})
            encrypt_and_send(client_socket, message_bytes, client_encryption_cipher)

        else:
            print("other message")

    def get_room_details(self, room_id):
        room = self.chatrooms[room_id]
        current_members = room.get_members()  # list of client sockets
        current_usernames = []  # empty list that will contain list of usernames
        for current_socket in current_members:
            current_client_object = self.clients[current_socket]  # the current client object
            username = current_client_object.get_name()  # the username of the client object
            current_usernames.append(username)
        room_dict = {
            "id": room.get_room_id(),
            "name": room.get_name(),
            "host": room.get_host(),
            "members": current_usernames
        }
        return room_dict

    def broadcast(self, current_client_socket, message_bytes, room_id):
        room_object = self.chatrooms[room_id] # todo ???
        members = room_object.get_members()
        if len(members) > 0:
            for client_socket in members:
                if client_socket is not current_client_socket:
                    encryption_cipher = self.clients[client_socket].get_encryption_cipher()
                    encrypt_and_send(client_socket, message_bytes, encryption_cipher)
            print("broadcast:", message_bytes, "to room", room_id)

    def run(self):
        self.init_server()
        print("Running server...")
        while True:
            for key, _ in self.read_selector.select():
                socket, callback = key.fileobj, key.data
                try:
                    callback(socket)
                except ConnectionResetError:
                    name = self.clients[socket].get_name()
                    print("socket error", name)
                    room_id = self.clients[socket].get_current_room_id()
                    self.read_selector.unregister(socket)
                    self.write_selector.unregister(socket)
                    self.clients.pop(socket)
                    socket.close()
                    message_bytes = message_to_bytes("-DISCONNECT-", {"user": name})
                    if room_id is not None:
                        self.chatrooms[room_id].remove_member(socket)
                        self.broadcast(socket, message_bytes, room_id)

def message_to_bytes(message_type, values_dict):
    """
    A function which takes the message type and remaining items as parameters
    and returns the encoded equivalent in bytes
    """
    message_dict = {key: value for key,value in values_dict.items()}
    message_dict["message_type"] = message_type
    message_bytes = cbor2.dumps(message_dict)
    return message_bytes

def encrypt_and_send(client_socket, message_bytes, encryption_cipher):
    """
    Encrypts the given message with the given cipher
    and sends it across the given socket
    """
    print("encrypting and sending:", message_bytes)
    encrypted_message = server_encryption.encrypt_message(message_bytes, encryption_cipher)
    client_socket.send(encrypted_message)

def receive_and_decrypt(client_socket, encryption_cipher):
    """
    Receives a new message from the given socket
    and decrypts it with the given cipher
    Returns the decrypted message dictionary
    """
    encrypted_message = client_socket.recv(1024)
    message_bytes = server_encryption.decrypt_message(encrypted_message, encryption_cipher)
    message_dict = cbor2.loads(message_bytes)
    return message_dict

def get_server_address():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip
