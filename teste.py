import PySimpleGUI as sg
import time

cprint = sg.cprint          # make it really easy to call cprint

layout = [  [sg.Multiline(size=(80,20), auto_refresh=True, reroute_stdout=True, reroute_cprint=True, write_only=True, key='-OUT-')],
            [sg.Button('Exit')]  ]

window = sg.Window('Window Title', layout, finalize=True)

print('Starting up my normal program')

cprint('My program is starting', colors='white on red')

for i in range(100):
    print(i)


cprint('About to do operations that sleep... this normally causes programs to "hang"', colors='red on yellow')
time.sleep(2)

for i in range(10):
    print(f'This is a sleeping loop... count = {i}')
    time.sleep(1)

cprint('Done with sleeping loop', colors='white on red')

sg.popup('about to exit')
window['-OUT-'].restore_stdout()

window.close()

print('exiting the program')
sg.popup('Just before exit')