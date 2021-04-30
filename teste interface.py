from PySimpleGUI import PySimpleGUI as sg

def janela_config():
    # layout
    sg.theme('Reddit')
    #sg.theme('GreenMono')
    layout = [
        [sg.Text('Dica amiga: Crie um instagram só para concorrer a sorteios...',text_color='red')],
        [sg.Text('Usuário:',size=(6,1))],
        [sg.Text('Vai digitar frase?')],
        [sg.Input(key='usuario',size=(20,1))],
        [sg.Button('Salvar')],
        [sg.Output(size=(600,30))]

    ]    
    
    nome_tela = 'Configuração'
    return sg.Window(nome_tela, layout,location=(120,120), size=(300,300),finalize=True)

    
# Janela
janela1,janela2 = janela_config(), None
while True:
    window, event, values = sg.read_all_windows()
    if window == janela1 and event == sg.WINDOW_CLOSED:
        break
    if window == janela2 and event == sg.WINDOW_CLOSED:
        janela2.close()

    if window == janela1 and event == 'Salvar':
        print('teste')
        print(values['usuario'])