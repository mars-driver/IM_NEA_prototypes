import server

# CONSTANTS
HOMEHOST = "192.168.1.122"
SCHOOLHOST = "10.56.81.185"
LOCALHOST = "127.0.0.1"
GRANNYHOST = "192.168.1.138"
MARSHOST = "10.58.50.14"
MY_PORT = 13108

currenthost = HOMEHOST

host = server.get_server_address()
print(host)
assert host == currenthost

# SERVER
my_server = server.ChatServer(currenthost, MY_PORT)

# TEST ROOM
test_room = server.ChatRoom("001", "test room", "admin")
my_server.chatrooms["001"] = test_room
my_server.chatrooms["002"] = server.ChatRoom("002", "test room 2 :3", "admin")

# MAIN PROGRAM
my_server.run()