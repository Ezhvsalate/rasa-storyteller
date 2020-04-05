import base64
import io

import PySimpleGUI as sg
from PIL import Image

from common.constants import *

sg.theme(APP_THEME)
sg.set_options(auto_size_buttons=True, border_width=0,
               button_color=sg.COLOR_SYSTEM_DEFAULT)
wcolor = (APP_THEME_BG_COLOR, APP_THEME_BG_COLOR)


def image_file_to_bytes(image64, size):
    image_file = io.BytesIO(base64.b64decode(image64))
    img = Image.open(image_file)
    img.thumbnail(size, Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    imgbytes = bio.getvalue()
    return imgbytes


def button_params(button_image):
    button_params = {"image_data": image_file_to_bytes(button_image, (110, 50)),
                     "button_color": wcolor,
                     "font": "Any 11",
                     "border_width": 0}
    return button_params


def generate_main_window_layout(nlu_tree_data, response_tree):
    intent_tab_layout = [[sg.Text(TAB_INTENTS_DESCRIPTION)],
                         [nlu_tree_data],
                         [sg.Button(ACTION_ADD_INTENT, **button_params(green_button)),
                          sg.Button(BUTTON_ADD_EXAMPLE, key=ACTION_ADD_INTENT_EXAMPLE, **button_params(black_button)),
                          sg.Button(ACTION_UPDATE_INTENT, **button_params(blue_button)),
                          sg.Button(ACTION_REMOVE_INTENT, **button_params(orange_button))]]

    response_tab_layout = [[sg.Text(TAB_RESPONSES_DESCRIPTION)],
                           [response_tree],
                           [sg.Button(ACTION_ADD_RESPONSE, **button_params(green_button)),
                            sg.Button(BUTTON_ADD_EXAMPLE, key=ACTION_ADD_RESPONSE_EXAMPLE, **button_params(black_button)),
                            sg.Button(ACTION_UPDATE_RESPONSE, **button_params(blue_button)),
                            sg.Button(ACTION_REMOVE_RESPONSE, **button_params(orange_button))]]

    stories_tab_layout = [[sg.Text(TAB_STORIES_DESCRIPTION)],
                          # [stories_tree],
                          [sg.Button(ACTION_ADD_CHILD, **button_params(green_button)),
                           sg.Button(ACTION_ADD_SIBLING, **button_params(green_button)),
                           sg.Button(ACTION_REMOVE_STORY_ITEM, **button_params(orange_button)),
                           sg.Button(ACTION_MOVE_STORY_ITEM_UP, **button_params(black_button)),
                           sg.Button(ACTION_MOVE_STORY_ITEM_DOWN, **button_params(black_button))]]

    main_window_layout = [[sg.TabGroup([[sg.Tab(TAB_INTENTS_HEADING, intent_tab_layout),
                                         sg.Tab(TAB_RESPONSES_HEADING, response_tab_layout),
                                         sg.Tab(TAB_STORIES_HEADING, stories_tab_layout)]])],
                          [sg.Button(ACTION_EXPORT_DATA, **button_params(blue_button)),
                           sg.Button(ACTION_CLOSE_WINDOW, **button_params(orange_button))]]
    return main_window_layout


def generate_import_window_layout():
    add_intent_layout = [
        [sg.Text(LOCATE_FILE_TEXT.format(filename="nlu.md")), sg.FileBrowse(key=NLU_FILE_KEY, file_types=(("nlu", "*.md"),))],
        [sg.Text(LOCATE_FILE_TEXT.format(filename="domain.yml")), sg.FileBrowse(key=DOMAIN_FILE_KEY, file_types=(("domain", "*.yml"),))],
        [sg.Text(LOCATE_FILE_TEXT.format(filename="stories.md")), sg.FileBrowse(key=STORIES_FILE_KEY, file_types=(("stories", ".md"),))],
        [sg.Button(ACTION_SUBMIT, **button_params(green_button)),
         sg.Button(ACTION_CANCEL, **button_params(orange_button))]
    ]
    return add_intent_layout
