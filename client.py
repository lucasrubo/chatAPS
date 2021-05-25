from PySimpleGUI import PySimpleGUI as sg
import socket
import threading
import emoji

def janela_chat(sala):
    # layout
    sg.theme('Black')
    #sg.theme('GreenMono')
    layout = [
        [sg.Output(size=(400,30), key='chat')],
        [sg.Multiline(size=(62,8),key="mensagem"),sg.Button('Enviar')],
    ]    
    
    nome_tela = 'ChatRoom: '+sala
    return sg.Window(nome_tela, layout,location=(120,120), size=(550,580),finalize=True)

def janela_username():
    # layout
    sg.theme('Black')
    #sg.theme('GreenMono')
    layout = [
        [sg.Text('Usuário:')],
        [sg.Input("user",size=(30, 1),key='usuario')],
        [sg.Text('')],
        [sg.Text('IP:')],
        [sg.Input("26.122.120.56",size=(30, 1),key='ip')],
        [sg.Text('')],
        [sg.Text('Porta:')],
        [sg.Input("59000",size=(30, 1),key='porta')],
        [sg.Text('',pad=(83,0)),sg.Button('Logar')],
    ]    
    
    nome_tela = 'Login'
    return sg.Window(nome_tela, layout,location=(120,120), size=(240,250),finalize=True)

    


# Janela
janela1,janela2 = janela_username(), None
contar = 0
while True:
    window, event, values = sg.read_all_windows()
    if window == janela1 and event == sg.WINDOW_CLOSED:
        break
    
    if window == janela2 and event == sg.WINDOW_CLOSED:   
        janela2.close()

    if window == janela1 and event == 'Logar':
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
                    print("Error......404")
                    window.close()
                    client.close
                    break

        def client_send(message_send):
            global contar
            if(contar >= 10):                
                print("TIMEOUT POR SPAM")
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
    
# Close
window.close()