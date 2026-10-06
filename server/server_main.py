import server

# CONSTANTS
homehost = "192.168.1.122"
schoolhost = "10.56.80.90"
localhost = "127.0.0.1"
grannyhost = "192.168.1.138"
my_port = 13108
host = server.get_server_address()

currenthost = schoolhost # change based on location

print("host address:", host)
assert host == currenthost

# MAIN PROGRAM
server = server.ChatServer(currenthost, my_port)
server.run()