from uuid import uuid4

import PySimpleGUI as sg

from common.constants import *
from gui.layout import button_params


class AddExampleForm(object):
    FORM_NAME = 'Add example'
    INPUT_LABEL = 'Example'
    EMPTY_TEXT_ERROR = "Text cannot be empty."
    INPUT_KEY = 'example_text'

    def __init__(self, return_to, parent_key, parent_type, handler):
        self.return_to = return_to
        self.parent_key = parent_key
        self.parent_type = parent_type
        self.handler = handler
        self.form = sg.FlexForm(self.FORM_NAME, return_keyboard_events=True).layout(self.layout())
        self.icon = QUESTION_ICON if self.parent_type == TYPE_INTENT else ANSWER_ICON

    def layout(self):
        layout = [
            [sg.Text(self.INPUT_LABEL), sg.InputText(key=self.INPUT_KEY)],
            [sg.Button(ACTION_SUBMIT, **button_params(green_button)),
             sg.Button(ACTION_CANCEL, **button_params(orange_button))]
        ]
        return layout

    def validate(self, values):
        error = None
        if values[self.INPUT_KEY] == '':
            error = self.EMPTY_TEXT_ERROR
        return error

    def process(self):
        self.return_to.Disable()
        new_item = None
        while True:
            button, values = self.form.Read()
            if button in DEFAULT_FORM_SUBMIT_ACTIONS:
                error = self.validate(values)
                if not error:
                    new_item = self.handler.tree.TreeData.Insert(self.parent_key, key=str(uuid4()), text=values[self.INPUT_KEY], values=[], icon=self.icon)
                    self.handler.tree.Update(values=self.handler.tree.TreeData)
                    self.handler.tree.see(new_item)
                    self.handler.tree.selection_set([new_item])
                else:
                    sg.Popup(error, icon=sg.SYSTEM_TRAY_MESSAGE_ICON_CRITICAL, keep_on_top=True)
                self.form.close()
                break
            elif button in DEFAULT_FORM_CANCEL_ACTIONS:
                self.form.close()
                break
        self.handler.sort_alphabetically()
        self.return_to.bring_to_front()
        self.return_to.Enable()
        return new_item
