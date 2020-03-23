import PySimpleGUI as sg

from common.constants import *
from gui.layout import button_params


class AddStoryItemForm(object):
    INPUT_LABEL = "Item"
    INPUT_KEY_NAME = 'add_item'

    def __init__(self, return_to, form_name, parent_object_key, stories):
        self.return_to = return_to
        self.stories = stories
        self.parent_object_key = parent_object_key
        self.parent_object_type = stories.tree_data.get_node_data_by_key(parent_object_key)['values'][0] if parent_object_key != '' else 'root'
        available_values = None
        if self.parent_object_type == TYPE_INTENT:
            available_values = sorted(self.stories.resp.items.keys())
        elif self.parent_object_type in (TYPE_RESPONSE, 'root'):
            available_values = sorted(self.stories.nlu.items.keys())
        self.form = sg.FlexForm(form_name, return_keyboard_events=True).layout(self.layout(available_values))

    def layout(self, available_values):
        layout = [
            [sg.Text(self.INPUT_LABEL), sg.Combo(size=(50, 30), key=self.INPUT_KEY_NAME, font='Any 12', values=tuple(available_values))],
            [sg.Button(ACTION_SUBMIT, **button_params(green_button)),
             sg.Button(ACTION_CANCEL, **button_params(orange_button))]
        ]
        return layout

    def process(self):
        self.return_to.Disable()
        new_item = None
        while True:
            button, values = self.form.Read()
            if button in DEFAULT_FORM_SUBMIT_ACTIONS:
                self.stories.add_item(parent_key=self.parent_object_key, parent_type=self.parent_object_type, text=values[self.INPUT_KEY_NAME])
                self.form.close()
                break
            elif button in DEFAULT_FORM_CANCEL_ACTIONS:
                self.form.close()
                break
        self.stories.sort_alphabetically()
        self.return_to.bring_to_front()
        self.return_to.Enable()
        return new_item
