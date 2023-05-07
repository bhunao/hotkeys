import logging

import PySimpleGUI as sg

from actions import hotkeys, button_pressed, save_keys, load_keys

# TODO:
#       separeta terminal and gui version
#       how it will work on linux
#       create hotkey and save hotkey
#       create sets and can save sets


logging = logging.getLogger(__name__)

otro_dict = load_keys()
mpos = 0, 0
button_text = {}


layout = [[sg.Text(mpos, key="mouse_pos")],
          [sg.Button('hotkeys', key='hotkeys')],
          [sg.Button('save_keys', key='save_keys')],
          ]

for key, value in otro_dict.items():
    button_text[key] = value  # Save the button text to the dictionary
    button = [
            sg.Button(f'set-{key}', key=f'{key}'),
            sg.Text(value, key=f'value-{key}')
            ]
    layout.append(button)

window = sg.Window('Window Title', layout)


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    elif event in otro_dict.keys():
        pos = button_pressed(event, otro_dict, window)
        window[f'value-{key}'].update(pos)
    elif event == 'hotkeys':
        print("hotkeys"*15)
        hotkeys(otro_dict)
    elif event == 'save_keys':
        print(event*15)
        save_keys(otro_dict)
    else:
        window['mouse_pos'].update("asd")
