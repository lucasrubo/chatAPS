import socket
import threading

HOST = input("Host: ")
PORT = int(input("Port: "))

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print(f'Server is Up and Listening on {HOST}:{PORT}')

clients = []
usernames = []

def globalMessage(message):
    for client in clients:
        client.send(message)

def handleMessages(client):
    while True:
        try:
            receiveMessageFromClient = client.recv(2048).decode('ascii')
            globalMessage(f'{usernames[clients.index(client)]} :{receiveMessageFromClient}'.encode('ascii'))
        except:
            clientLeaved = clients.index(client)
            client.close()
            clients.remove(clients[clientLeaved])
            clientLeavedUsername = usernames[clientLeaved]
            print(f'{clientLeavedUsername} has left the chat...')
            globalMessage(f'{clientLeavedUsername} has left us...'.encode('ascii'))
            usernames.remove(clientLeavedUsername)


def initialConnection():
    while True:
        try:
            client, address = server.accept()
            print(f"New Connetion: {str(address)}")
            clients.append(client)
            client.send('getUser'.encode('ascii'))
            username = client.recv(2048).decode('ascii')
            usernames.append(username)
            globalMessage(f'{username} just joined the chat!'.encode('ascii'))
            user_thread = threading.Thread(target=handleMessages,args=(client,))
            user_thread.start()
        except:
            pass

initialConnection()