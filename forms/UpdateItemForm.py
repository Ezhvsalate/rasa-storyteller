import PySimpleGUI as sg

from common.constants import *
from gui.layout import button_params


class UpdateItemForm(object):
    EMPTY_TEXT_ERROR = "Text cannot be empty."
    INPUT_KEY = 'updated_text'
    ITEM_WITH_KEY_EXISTS_ERROR = "Item with such name/text already exists."

    def __init__(self, return_to, form_name, updated_item_key, updated_item_type, handler, tree, stories, stories_tree):
        self.return_to = return_to
        self.updated_item_key = updated_item_key
        self.updated_item_type = updated_item_type
        self.handler = handler
        self.stories = stories
        self.tree = tree
        self.stories_tree = stories_tree
        self.form = sg.FlexForm(form_name, return_keyboard_events=True)

    def layout(self, old_text):
        update_text_layout = [
            [sg.InputText(key=self.INPUT_KEY, default_text=old_text)],
            [sg.Button(ACTION_SUBMIT, **button_params(green_button)),
             sg.Button(ACTION_CANCEL, **button_params(orange_button))]
        ]
        return update_text_layout

    def validate(self, values):
        error = None
        if values[self.INPUT_KEY] == '':
            error = self.EMPTY_TEXT_ERROR
        elif values[self.INPUT_KEY] in self.handler.items:
            error = self.ITEM_WITH_KEY_EXISTS_ERROR
        return error

    def process(self):
        self.return_to.Disable()
        self.form.Layout(self.layout(self.updated_item_key))

        while True:
            button, values = self.form.Read()
            if button in DEFAULT_FORM_SUBMIT_ACTIONS:
                error = self.validate(values)
                if not error:
                    self.handler.update_node_value(self.updated_item_key, values['updated_text'])
                    self.tree.Update(self.handler.export_to_pysg_tree())
                    self.tree.see(values['updated_text'])
                    self.tree.selection_set([values['updated_text']])
                    self.stories_tree.Update(self.stories.export_to_pysg_tree())
                else:
                    sg.Popup(error, icon=sg.SYSTEM_TRAY_MESSAGE_ICON_CRITICAL, keep_on_top=True)
                self.form.close()
                break
            elif button in DEFAULT_FORM_CANCEL_ACTIONS:
                self.form.close()
                break
        # self.handler.sort_alphabetically()
        self.return_to.bring_to_front()
        self.return_to.Enable()
