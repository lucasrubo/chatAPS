import threading 
import socket
import emoji

host = "26.122.120.56"
port = 59000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)
clients = []
aliases = []

print("server rodando")
def broadcast(sender,message):
    for client in clients:
        if client != sender:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(client,message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(client,f"{alias} saiu do chat!".encode('utf-8'))
            aliases.remove(alias)
            break

def receive():
    while True:
        client,address = server.accept()
        print(f"Conexao estabelecida {str(address)}")
        client.send("Nome:".encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(alias)
        broadcast(client,f'{alias} entrou no chat'.encode('utf-8'))
        client.send("Conectado ".encode('utf-8'))
        thread = threading.Thread(target=handle_client,args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()

