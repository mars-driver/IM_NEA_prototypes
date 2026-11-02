import client

# CONSTANTS
HOMEHOST = "192.168.1.122"
SCHOOLHOST = "10.56.81.120"
LOCALHOST = "127.0.0.1"
GRANNYHOST = "192.168.1.138"
MY_PORT = 13108

currenthost = HOMEHOST

client = client.ChatClient(currenthost, MY_PORT)
client.connect()