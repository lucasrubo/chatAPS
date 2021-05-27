from PySimpleGUI import PySimpleGUI as sg       ## ferramenta usada paar criar um layout
import socket                                   ## import da ferrramenta de abrir sockets
import threading                                ## ferramenta pra deixar rodando sempre a função de receber mensagem
import emoji                                    ## emoji no console
import re                                       ## ferramenta de search na variavel
import time 

## Aqui ele abre o arquivo txt aonde salva o ip,port e usuario
arquivo_config = open('configs.txt',encoding="utf8")
arquivo_config_read = arquivo_config.readlines()
arquivo_config.close()

## Aqui ele le o arquivo txt aonde salva o ip,port e usuario
for config_frase  in arquivo_config_read :
    config_frase = config_frase.replace('\n','')
    if re.search("ip", config_frase):
        host = config_frase.replace('ip=','')
        
    if re.search("porta", config_frase):
        port = config_frase.replace('porta=','')

    if re.search("usuario", config_frase):
        usuario = config_frase.replace('usuario=','')

## ferramenta de econtra a linha em que a string se localiza no txt
def encontrar_string(path,string):
    with open(path,'r') as f:
        texto=f.readlines()
    for i in texto:
        if string in i:
            return texto.index(i)

## ferramenta que altera a linha desejada no txt
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

## layout da janela do chat
def janela_chat(sala):
    # layout
    sg.theme('DarkGrey9')
    #sg.theme('GreenMono')
    layout = [
        [sg.Text('',pad=(210,0)),sg.Button('Hitórico'),sg.Button('Sair')],
        [sg.Multiline(size=(300,28), auto_refresh=True, reroute_stdout=True, reroute_cprint=True, disabled=True,autoscroll = True, key='-OUT-')],
        [sg.Multiline(size=(62,8),key="mensagem"),sg.Button('Enviar')],
    ]    
    
    nome_tela = 'ChatRoom: '+sala
    return sg.Window(nome_tela, layout,location=(120,120), size=(550,580),finalize=True)

## layout da janela do login
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
    naofoi = 0
    window, event, values = sg.read_all_windows()                   ## le os eventos,janelas,e input da tela

    if window == janela1 and event == sg.WINDOW_CLOSED:             ## se janela do login fechar ele finaliza o progama            
        break
    
    if window == janela2 and event == sg.WINDOW_CLOSED:             ## se janela do chat fechar ele fecha a janela, pois finalizar o programa causava um crash    
        janela2.close()

    if window == janela1 and event == 'Logar':                      ## se o botao Logar for assionado ele fecha o login e abre a do chat
        
        if values['usuario'] == '':                                 ## trata o input para nao deixar vazio
            naofoi = 1
        if values['porta'] == '':                                   ## trata o input para nao deixar vazio
            naofoi = 1
        if values['ip'] == '':                                      ## trata o input para nao deixar vazio
            naofoi = 1
        if naofoi == 1:
            sg.popup('Campo inválido')
        else:
            novo_ip = 'ip='+values['ip']
            novo_port = 'porta='+values['porta']
            novo_user = 'usuario='+values['usuario']

            linha_ip = encontrar_string('configs.txt', 'ip=')             
            linha_port = encontrar_string('configs.txt', 'porta=')   
            linha_user = encontrar_string('configs.txt', 'usuario=')    

            if linha_ip !='':
                alterar_linha('configs.txt',linha_ip,novo_ip)
            if linha_port !='':
                alterar_linha('configs.txt',linha_port,novo_port)
            if linha_user !='':
                alterar_linha('configs.txt',linha_user,novo_user)


            janela1.close()                                             ## fecha janela do login

            nome = values['ip']+":"+values['porta']
            janela2 = janela_chat(nome)                                 ## abre a janela do chat passando o nome dela (ip+porta)

            alais = values['usuario']
            ## função que recebe as mensagens do socket q sao passadas pelo server.py
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

            ## função de enviar a mensagem
            def client_send(message_send):
                global contar
                if(contar >= 10):                
                    sg.popup('TIMEOUT POR SPAM')                            
                else:
                    if len(message_send)>600:
                        sg.popup('Limite de caracter'+str(len(message_send))+"/600")        
                    else:
                        message = f'{alais}: {message_send}'
                        client.send(message.encode('utf-8'))
                        print(message)
                        contar+=1
                        window.FindElement('mensagem').Update('')           ## seta o campo mensagem para nada

            ## abre uma conexão com o socket
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            host = values['ip']
            port = int(values['porta'])
            client.connect((host,port))
            receving_thread =threading.Thread(target=client_receive)        ## criação de tread para receber as mensagens 
            receving_thread.start()

    ## evento do botao Enviar q chama a função client_send()
    if window == janela2 and event == 'Enviar':
        mensagem_tratada = values['mensagem'].replace('\n','')
        mensagem_tratada = mensagem_tratada.replace(' ','')
        if(mensagem_tratada !=''):
            client_send(values['mensagem'])        

    ## salva histórico de mensagem
    if window == janela2 and event == 'Hitórico':
        data_atual = time.strftime('%Y-%m-%d_%H_%M', time.localtime())
        try:
            arquivo = open("historico_chat_"+data_atual+".txt",'w')            
            arquivo.write(values['-OUT-'])
        except FileNotFoundError:
            arquivo = open("historico_chat"+data_atual+".txt", 'w')
            arquivo.write(values['-OUT-'])
        arquivo.close()

    ##sending_thread = threading.Thread(target=clinet_send)
    ##sending_thread.start()
    
    if window == janela2 and event == 'Sair':                       ## evento botao sair fecha o programa
        break

        
# Close
window.close()