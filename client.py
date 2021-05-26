from PySimpleGUI import PySimpleGUI as sg
import socket
import threading
import emoji
import re

arquivo_frases_sim_n = open('configs.txt',encoding="utf8")
lista_frases_sim_n = arquivo_frases_sim_n.readlines()
arquivo_frases_sim_n.close()

for config_frase  in lista_frases_sim_n :
    config_frase = config_frase.replace('\n','')
    ##print(config_frase)
    if re.search("ip", config_frase):
        host = config_frase.replace('ip=','')
        
    if re.search("porta", config_frase):
        port = config_frase.replace('porta=','')

    if re.search("usuario", config_frase):
        usuario = config_frase.replace('usuario=','')

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

def janela_chat(sala):
    # layout
    sg.theme('DarkGrey9')
    #sg.theme('GreenMono')
    layout = [
        [sg.Text('',pad=(240,0)),sg.Button('Sair')],
        [sg.Multiline(size=(300,28), auto_refresh=True, reroute_stdout=True, reroute_cprint=True, disabled=True, key='-OUT-')],
        [sg.Multiline(size=(62,8),key="mensagem"),sg.Button('Enviar')],
    ]    
    
    nome_tela = 'ChatRoom: '+sala
    return sg.Window(nome_tela, layout,location=(120,120), size=(550,580),finalize=True)

def janela_username():
    # layout
    sg.theme('DarkGrey9')
    #sg.theme('GreenMono')
    layout = [
        [sg.Text('Usuário:')],
        [sg.Input(usuario,size=(30, 1),key='usuario')],
        [sg.Text('')],
        [sg.Text('IP:')],
        [sg.Input(host,size=(30, 1),key='ip')],
        [sg.Text('')],
        [sg.Text('Porta:')],
        [sg.Input(port,size=(30, 1),key='porta')],
        [sg.Text('',pad=(83,0)),sg.Button('Logar')],
    ]    
    
    nome_tela = 'Login'
    return sg.Window(nome_tela, layout,location=(120,120), size=(240,250),finalize=True)

# Janela
janela1,janela2 = janela_username(), None
contar = 0
while True:
    window, event, values = sg.read_all_windows()
    #window["-OUT-"](disabled=True)
    if window == janela1 and event == sg.WINDOW_CLOSED:
        break
    
    if window == janela2 and event == sg.WINDOW_CLOSED:   
        janela2.close()

    if window == janela1 and event == 'Logar':

        novo_ip = 'ip='+values['ip']
        novo_port = 'porta='+values['porta']
        novo_user = 'usuario='+values['usuario']

        linha_ip = encontrar_string('configs.txt', 'ip=')    
        linha_port = encontrar_string('configs.txt', 'porta=')   
        linha_user = encontrar_string('configs.txt', 'usuario=')    
        ##print(linha_ip)
        ##print(linha_port)
        if linha_ip !='':
            alterar_linha('configs.txt',linha_ip,novo_ip)
        if linha_port !='':
            alterar_linha('configs.txt',linha_port,novo_port)
        if linha_user !='':
            alterar_linha('configs.txt',linha_user,novo_user)


        janela1.close()
        ##janela2.un_hide()
        nome = values['ip']+":"+values['porta']
        janela2 = janela_chat(nome)

        ##alais = input("Escolha um Nome: ")

        alais = values['usuario']
        def client_receive():
            while True:
                try:
                    message = client.recv(1024)
                    message = message.decode('utf-8')
                    if message == "Nome:":
                        client.send(alais.encode('utf-8'))
                    else:
                        print(emoji.emojize(message))
                        global contar
                        contar=0
                except:
                    ##print("Error......404")
                    sg.popup('Error......404')
                    window.close()
                    client.close
                    break

        def client_send(message_send):
            global contar
            if(contar >= 10):                
                #print("TIMEOUT POR SPAM")
                sg.popup('TIMEOUT POR SPAM')
            else:
                message = f'{alais}: {message_send}'
                client.send(message.encode('utf-8'))
                print(message)
                contar+=1


        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = values['ip']
        port = int(values['porta'])
        client.connect((host,port))
        
        # Make the Output Element "read only"
        #window.Element('chat')._TKOut.output.bind("<Key>", lambda e: "break")

    if window == janela2 and event == 'Enviar':
        client_send(values['mensagem'])
        ##print("ta indo sim ")
        ##print(values['mensagem'])
        window.FindElement('mensagem').Update('')

    receving_thread =threading.Thread(target=client_receive)
    receving_thread.start()
    ##sending_thread = threading.Thread(target=clinet_send)
    ##sending_thread.start()
    
    if window == janela2 and event == 'Sair':     
        break

        
# Close
window.close()