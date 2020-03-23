import PySimpleGUI as sg

from common.constants import *
from core.TreeNode import TreeNode
from gui.layout import button_params


class AddItemForm(object):
    INPUT_EXAMPLES_LABEL = "Text examples (may fill blank some)"
    EMPTY_NAME_ERROR = "Name cannot be empty."
    NO_EXAMPLES_ERROR = "There should be at least one example."
    NON_UNIQUE_NAME_ERROR = "Name is not unique."
    INPUT_KEY_NAME = 'item_name'

    def __init__(self, return_to, form_name, item_type, handler):
        self.return_to = return_to
        self.item_type = item_type
        self.handler = handler
        self.form = sg.FlexForm(form_name, return_keyboard_events=True).layout(self.layout())
        self.parent_icon = ANSWER_ICON
        self.children_icon = QUESTION_ICON if self.item_type == TYPE_INTENT else ANSWER_ICON

    def layout(self):
        layout = [
            [sg.Text(self.item_type), sg.InputText(key=self.INPUT_KEY_NAME)],
            [sg.Text(self.INPUT_EXAMPLES_LABEL)],
            [sg.InputText()],
            [sg.InputText()],
            [sg.InputText()],
            [sg.InputText()],
            [sg.InputText()],
            [sg.InputText()],
            [sg.InputText()],
            [sg.InputText()],
            [sg.InputText()],
            [sg.InputText()],
            [sg.Button(ACTION_SUBMIT, **button_params(green_button)),
             sg.Button(ACTION_CANCEL, **button_params(orange_button))]
        ]
        return layout

    def validate(self, values):
        error = None
        if values[self.INPUT_KEY_NAME] == '':
            error = self.EMPTY_NAME_ERROR
        elif all([v == '' for k, v in values.items() if k != self.INPUT_KEY_NAME]):
            error = self.NO_EXAMPLES_ERROR
        elif values[self.INPUT_KEY_NAME] in self.handler.items.keys():
            error = self.NON_UNIQUE_NAME_ERROR
        return error

    def process(self):
        self.return_to.Disable()
        new_item = None
        while True:
            button, values = self.form.Read()
            if button in DEFAULT_FORM_SUBMIT_ACTIONS:
                error = self.validate(values)
                if not error:
                    parent_node = TreeNode(text=values[self.INPUT_KEY_NAME], values=[], icon=self.parent_icon)
                    kids = [TreeNode(text=value, values=[], icon=self.children_icon) for value in [v for k, v in values.items() if k != self.INPUT_KEY_NAME and v != '']]
                    new_item = self.handler.tree.add_node_to_root_with_children(parent_node, kids)
                    self.handler.items[values[self.INPUT_KEY_NAME]] = new_item
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
