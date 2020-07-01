import PySimpleGUI as sg

from common.constants import *
from gui.layout import button_params


class AddExampleForm(object):
    FORM_NAME = "Add example"
    INPUT_LABEL = "Example"
    EMPTY_TEXT_ERROR = "Text cannot be empty."
    ITEM_WITH_KEY_EXISTS_ERROR = "Item with such name/text already exists."
    INPUT_KEY = "example_text"

    def __init__(self, return_to, parent_name, handler, tree):
        self.return_to = return_to
        self.parent_name = parent_name
        self.handler = handler
        self.tree = tree
        self.form = sg.FlexForm(self.FORM_NAME, return_keyboard_events=True).layout(
            self.layout()
        )

    def layout(self):
        layout = [
            [sg.Text(self.INPUT_LABEL), sg.InputText(key=self.INPUT_KEY)],
            [
                sg.Button(ACTION_SUBMIT, **button_params(green_button)),
                sg.Button(ACTION_CANCEL, **button_params(orange_button)),
            ],
        ]
        return layout

    def validate(self, values):
        error = None
        if values[self.INPUT_KEY] == "":
            error = self.EMPTY_TEXT_ERROR
        if values[self.INPUT_KEY] in self.handler.items:
            error = self.ITEM_WITH_KEY_EXISTS_ERROR
        return error

    def process(self):
        self.return_to.Disable()
        new_item = None
        while True:
            button, values = self.form.Read()
            if button in DEFAULT_FORM_SUBMIT_ACTIONS:
                error = self.validate(values)
                if not error:
                    new_item = values[self.INPUT_KEY]
                    self.handler.add_example_to_node(self.parent_name, new_item)
                    self.tree.Update(values=self.handler.export_to_pysg_tree())
                    self.tree.see(new_item)
                    self.tree.selection_set([new_item])
                else:
                    sg.Popup(
                        error,
                        icon=sg.SYSTEM_TRAY_MESSAGE_ICON_CRITICAL,
                        keep_on_top=True,
                    )
                self.form.close()
                break
            elif button in DEFAULT_FORM_CANCEL_ACTIONS:
                self.form.close()
                break
        self.return_to.bring_to_front()
        self.return_to.Enable()
        return new_item
