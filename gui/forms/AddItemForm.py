import PySimpleGUI as sg

from common.constants import *
from gui.layout import button_params


class AddItemForm(object):
    INPUT_EXAMPLES_LABEL = "Text examples (may fill blank some)"
    EMPTY_NAME_ERROR = "Name cannot be empty."
    NO_EXAMPLES_ERROR = "There should be at least one example."
    INPUT_KEY_NAME = 'item_name'
    ITEM_WITH_KEY_EXISTS_ERROR = "Item with such name/example text already exists. All elements in a tree should be unique."
    ITEM_NAME_IS_DUPLICATED_IN_EXAMPLES = "Item name is duplicated in one of examples"
    THERE_ARE_DUPLICATES_IN_EXAMPLES = "There are duplicates in examples. Examples should be unique."

    def __init__(self, return_to, form_name, item_type, handler, tree):
        self.return_to = return_to
        self.item_type = item_type
        self.handler = handler
        self.form = sg.FlexForm(form_name, return_keyboard_events=True).layout(self.layout())
        self.tree = tree

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

    def validate(self, new_item_name, children_texts):
        error = None
        if new_item_name == '':
            error = self.EMPTY_NAME_ERROR
        elif all([v == '' for v in children_texts]):
            error = self.NO_EXAMPLES_ERROR
        elif new_item_name in self.handler.items:
            error = self.ITEM_WITH_KEY_EXISTS_ERROR
        elif any([v in self.handler.items for v in children_texts]):
            error = self.ITEM_WITH_KEY_EXISTS_ERROR
        elif new_item_name in children_texts:
            error = self.ITEM_NAME_IS_DUPLICATED_IN_EXAMPLES
        elif len(set(children_texts)) != len(children_texts):
            error = self.THERE_ARE_DUPLICATES_IN_EXAMPLES
        return error

    def process(self):
        self.return_to.Disable()
        while True:
            button, values = self.form.Read()
            new_item = values[self.INPUT_KEY_NAME]
            children_texts = [value for value in [v for k, v in values.items() if k != self.INPUT_KEY_NAME and v != '']]
            if button in DEFAULT_FORM_SUBMIT_ACTIONS:
                error = self.validate(new_item, children_texts)
                if not error:
                    self.handler.add_node_with_kids(values[self.INPUT_KEY_NAME], *children_texts)
                    self.tree.Update(self.handler.export_to_pysg_tree())
                    self.tree.see(new_item)
                    self.tree.selection_set([new_item])
                else:
                    sg.Popup(error, icon=sg.SYSTEM_TRAY_MESSAGE_ICON_CRITICAL, keep_on_top=True)
                self.form.close()
                break
            elif button in DEFAULT_FORM_CANCEL_ACTIONS:
                self.form.close()
                break
        self.return_to.bring_to_front()
        self.return_to.Enable()
        return new_item
