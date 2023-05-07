import json
import logging
import keyboard
import pyautogui

import PySimpleGUI as sg

# TODO:
#       separeta terminal and gui version
#       how it will work on linux
#       create hotkey and save hotkey
#       create sets and can save sets



logging.basicConfig(level=logging.DEBUG)

keys_dict = dict()
with open('keys.json', 'r') as file:
    saved_data = json.loads(file.read())
    keys_dict.update(saved_data)

def save_keys(keys_dictiarie: dict):
    with open("keys.json", "w") as file:
        jsn_str = json.dumps(keys_dictiarie)
        file.write(jsn_str)

for n in range(1,10):
    n = str(n)
    keys_dict[n] = keys_dict.get(n, None)

otro_dict = keys_dict.copy()
mpos = 0, 0
button_text = {}

def hotkeys():
    while True:
        key = keyboard.read_key()
        if key in otro_dict.keys():
            #mpos = pyautogui.position()
            #logging.debug(f'from position: {mpos}')
            pyautogui.moveTo(otro_dict[key])
            pyautogui.leftClick()
            logging.debug(f'clicking in positin: {mpos}')
            logging.debug(f'to positino: {mpos}')
            #pyautogui.moveTo(mpos)
        elif key == "esc":
            break

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

def button_pressed(key, values):
    keyboard.wait('space')
    mpos = pyautogui.position()
    logging.debug(f"mouse position captured at: [{mpos}]")
    pos = mpos.x, mpos.y
    otro_dict[key] = pos
    window[f'value-{key}'].update(pos)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    elif event in otro_dict.keys():
        button_pressed(event, values)
    elif event == 'hotkeys':
        print("hotkeys"*15)
        hotkeys()
    elif event == 'save_keys':
        print(event*15)
        save_keys(otro_dict)
    else:
        window['mouse_pos'].update("asd")
