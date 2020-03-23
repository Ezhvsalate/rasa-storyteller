import PySimpleGUI as sg


class RemoveItemForm(object):
    USED_ITEM_ERROR = "This answer is used somewhere in stories, so can't remove it."

    def __init__(self, item_key, item_type, handler, stories):
        self.handler = handler
        self.item_key = item_key
        self.item_text = self.handler.tree_data.get_node_data_by_key(self.item_key)['text']
        self.item_type = item_type
        self.stories = stories

    def layout(self):
        return None

    def validate(self):
        error = None
        for item in self.stories.tree_data.tree_dict.keys():
            data = self.stories.tree_data.get_node_data_by_key(item)
            if data['values'] and data['values'][0] == self.item_type and data['text'] == self.item_text:
                error = self.USED_ITEM_ERROR
        return error

    def process(self):
        error = self.validate()
        if not error:
            self.handler.tree.remove_node_and_select_nearest(self.item_key)
            if self.item_text in self.handler.items:
                del self.handler.items[self.item_text]
            self.handler.sort_alphabetically()
        else:
            sg.Popup(error, icon=sg.SYSTEM_TRAY_MESSAGE_ICON_WARNING, keep_on_top=True,
                     button_type=sg.POPUP_BUTTONS_NO_BUTTONS)
