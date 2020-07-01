import PySimpleGUI as sg


class RemoveItemForm(object):
    USED_ITEM_ERROR = "This answer is used somewhere in stories, so can't remove it."

    def __init__(self, item_key, item_type, handler, stories, tree):
        self.handler = handler
        self.item_key = item_key
        self.item_type = item_type
        self.stories = stories
        self.tree = tree

    def layout(self):
        return None

    def process(self):
        try:
            prev_node = self.tree.get_previous_sibling(
                self.item_key, parent_if_none=True
            )
            self.handler.remove_node(self.item_key)
        except ValueError as e:
            sg.Popup(
                e,
                icon=sg.SYSTEM_TRAY_MESSAGE_ICON_WARNING,
                keep_on_top=True,
                button_type=sg.POPUP_BUTTONS_NO_BUTTONS,
            )
        else:
            self.tree.Update(self.handler.export_to_pysg_tree())
            self.tree.see(prev_node)
            self.tree.selection_set([prev_node])
