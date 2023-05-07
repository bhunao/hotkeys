import json
import logging
import argparse
from pathlib import Path

import pyautogui
import keyboard


logging.basicConfig(level=logging.DEBUG)


def load_keys(keys_file='keys.json'):
    keys_dict = dict()
    path = Path(keys_file)

    if not path.is_file():
        return {}

    with open(keys_file, 'r') as file:
        saved_data = json.loads(file.read())
        keys_dict.update(saved_data)

    for n in range(1, 10):
        n = str(n)
        keys_dict[n] = keys_dict.get(n, None)
    return keys_dict


def hotkeys(otro_dict, back_to_origin=False, escape_key='esc'):
    key = keyboard.read_key()
    while key != escape_key:
        if key in otro_dict.keys():
            if back_to_origin:
                mpos = pyautogui.position()
                logging.debug(f'initial mouse position: [{mpos}]')

            pyautogui.moveTo(otro_dict[key])
            pyautogui.leftClick()
            logging.debug(f'moved and clicked at: [{otro_dict[key]}], with key: [{key}]')

            if back_to_origin:
                logging.debug(f'going back to initial position: [{mpos}]')
                pyautogui.moveTo(mpos)

        key = keyboard.read_key()


def save_keys(keys_dict: dict, keyset_file="keys.json"):
    with open(keyset_file, "w") as file:
        jsn_str = json.dumps(keys_dict)
        file.write(jsn_str)


def button_pressed(key, keys_dict):
    keyboard.wait('space')
    mpos = pyautogui.position()
    logging.debug(f"mouse position captured at: [{mpos}]")
    pos = mpos.x, mpos.y
    keys_dict[key] = pos
    return pos


def set_pos(escape_key='esc'):
    key = keyboard.read_key()
    if key != escape_key:
        mouse_pos = pyautogui.position()
        logging.debug(f"mouse position captured at: [{mouse_pos}], key: [{key}]")
        return key, mouse_pos
    else:
        logging.debug('exiting [get_button]')
    return key, None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            prog='hotkeys',
            description='perform setup hotkeys',
            epilog='create hotkeys and use')
    parser.add_argument('-b', '--back', action='store_true')
    parser.add_argument('option', type=str)
    parser.add_argument('keyset', type=str)

    args = parser.parse_args()

    if args.keyset == '.':
        args.keyset = 'keys.json'
    print(args)

    keys_dict = load_keys(args.keyset)

    match args.option:
        case 'start':
            hotkeys(keys_dict)
        case 'set-pos':
            key, pos = set_pos()
            keys_dict[key] = pos
            save_keys(keys_dict, args.keyset)
        case 'set-set':
            key = keyboard.read_key()
            while key != 'esc':
                key, pos = set_pos()
                keys_dict[key] = pos
            else:
                save_keys(keys_dict, args.keyset)
