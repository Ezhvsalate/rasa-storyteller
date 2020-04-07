import PySimpleGUI as sg

from common.constants import *
from gui.layout import button_params


class AddStoryItemForm(object):
    INPUT_LABEL = "Item"
    INPUT_KEY_NAME = 'add_item'

    def __init__(self, return_to, form_name, parent_object_key, stories, tree):
        self.return_to = return_to
        self.stories = stories
        self.tree = tree
        self.parent_object_key = parent_object_key
        self.available_values = self.stories.get_available_children_by_parent_id(parent_object_key)
        self.form = sg.FlexForm(form_name, return_keyboard_events=True).layout(self.layout(self.available_values))

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
                new_item = self.stories.add_item(parent_object_id=self.parent_object_key, text=values[self.INPUT_KEY_NAME])
                self.tree.Update(self.stories.export_to_pysg_tree())
                self.tree.see(new_item.id)
                self.tree.selection_set([new_item.id])
                self.form.close()
                break
            elif button in DEFAULT_FORM_CANCEL_ACTIONS:
                self.form.close()
                break
        self.return_to.bring_to_front()
        self.return_to.Enable()
        return new_item
