from PySimpleGUI import PySimpleGUI as sg
import emoji
import re
import threading 
import socket


def encontrar_string(path,string):
    with open(path,'r') as f:
        texto=f.readlines()
    for i in texto:
        if string in i:
            return texto.index(i)
            
def alterar_linha(path,index_linha,nova_linha):
    with open(path,'r') as f:
        texto=f.readlines()
    with open(path,'w') as f:
        for i in texto:
            if texto.index(i)==index_linha:
                if(nova_linha == ''):                    
                    f.write(nova_linha)
                else:
                    f.write(nova_linha+'\n')
            else:
                f.write(i)

arquivo_frases_sim_n = open('configs_server.txt',encoding="utf8")
lista_frases_sim_n = arquivo_frases_sim_n.readlines()
arquivo_frases_sim_n.close()

for config_frase  in lista_frases_sim_n :
    config_frase = config_frase.replace('\n','')
    ##print(config_frase)
    if re.search("ip", config_frase):
        host = config_frase.replace('ip=','')
        
    if re.search("porta", config_frase):
       port = config_frase.replace('porta=','')

def janela_username():
    # layout
    sg.theme('DarkGrey9')
    #sg.theme('GreenMono')
    layout = [
        [sg.Text('IP:')],
        [sg.Input(host,size=(30, 1),key='ip')],
        [sg.Text('')],
        [sg.Text('Porta:')],
        [sg.Input(port,size=(30, 1),key='porta')],
        [sg.Text('',pad=(83,0)),sg.Button('Iniciar')],
    ]    
    
    nome_tela = 'Login'
    return sg.Window(nome_tela, layout,location=(120,120), size=(240,250),finalize=True)
    


# Janela
janela1 = janela_username()
while True:        
    window, event, values = sg.read_all_windows()
    if window == janela1 and event == sg.WINDOW_CLOSED:
        break

    if window == janela1 and event == 'Iniciar':
        janela1.close()
        novo_ip = 'ip='+values['ip']
        novo_port = 'porta='+values['porta']

        linha_ip = encontrar_string('configs_server.txt', 'ip=')    
        linha_port = encontrar_string('configs_server.txt', 'porta=')   
        ##print(linha_ip)
        ##print(linha_port)
        if linha_ip !='':
            alterar_linha('configs_server.txt',linha_ip,novo_ip)
        if linha_port !='':
            alterar_linha('configs_server.txt',linha_port,novo_port)

        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((host,int(port)))
        server.listen(5)
        clients = []
        aliases = []

        print("Server rodando")
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
                    broadcast(client,alias+" saiu do chat!".encode('utf-8'))
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
                broadcast(client,alias+' entrou no chat'.encode('utf-8'))
                client.send("Conectado ".encode('utf-8'))
                thread = threading.Thread(target=handle_client,args=(client,))
                thread.start()

        if __name__ == "__main__":
            receive()

