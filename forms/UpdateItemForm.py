import PySimpleGUI as sg

from common.constants import *
from gui.layout import button_params


class UpdateItemForm(object):
    EMPTY_TEXT_ERROR = "Text cannot be empty."
    INPUT_KEY = 'updated_text'

    def __init__(self, return_to, form_name, updated_item_key, updated_item_type, handler, stories):
        self.return_to = return_to
        self.updated_item_key = updated_item_key
        self.updated_item_type = updated_item_type
        self.handler = handler
        self.stories = stories
        self.form = sg.FlexForm(form_name, return_keyboard_events=True)

    def layout(self, old_text):
        update_text_layout = [
            [sg.InputText(key=self.INPUT_KEY, default_text=old_text)],
            [sg.Button(ACTION_SUBMIT, **button_params(green_button)),
             sg.Button(ACTION_CANCEL, **button_params(orange_button))]
        ]
        return update_text_layout

    def process(self):
        self.return_to.Disable()
        node_data = self.handler.tree_data.get_node_data_by_key(self.updated_item_key)
        self.form.Layout(self.layout(node_data['text']))

        while True:
            button, values = self.form.Read()
            if button in DEFAULT_FORM_SUBMIT_ACTIONS:
                if values[self.INPUT_KEY] == '':
                    sg.Popup(self.EMPTY_TEXT_ERROR, icon=sg.SYSTEM_TRAY_MESSAGE_ICON_CRITICAL, keep_on_top=True)
                else:
                    self.handler.tree.update_node(self.updated_item_key, values['updated_text'])
                    if node_data['text'] in self.handler.items:
                        del self.handler.items[node_data['text']]
                        self.handler.items[values[self.INPUT_KEY]] = self.updated_item_key
                    for item in self.stories.tree_data.tree_dict.keys():
                        data = self.stories.tree_data.get_node_data_by_key(item)
                        if data['values'] and data['values'][0] == self.updated_item_type and data['text'] == node_data['text']:
                            self.stories.tree.update_node(item, values['updated_text'])
                self.form.close()
                break
            elif button in DEFAULT_FORM_CANCEL_ACTIONS:
                self.form.close()
                break
        self.handler.sort_alphabetically()
        self.return_to.bring_to_front()
        self.return_to.Enable()
