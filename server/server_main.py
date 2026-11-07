import server

# CONSTANTS
HOMEHOST = "192.168.1.122"
SCHOOLHOST = "10.56.84.65"
LOCALHOST = "127.0.0.1"
GRANNYHOST = "192.168.1.138"
MY_PORT = 13108

host = server.get_server_address()
print(host)
currenthost = HOMEHOST
assert currenthost == host


# MAIN PROGRAM
server = server.ChatServer(currenthost, MY_PORT)
server.run()

#TODO note: mostly works except client 1 crashes when client 2 joins and then client 1 attempts to send a msg ???