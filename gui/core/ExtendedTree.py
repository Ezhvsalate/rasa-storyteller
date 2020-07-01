import PySimpleGUI as sg


class ExtendedTree(sg.Tree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def see(self, item):
        id = self.KeyToID[item]
        self.TKTreeview.see(id)

    def get_selection(self):
        return [self.IdToKey[item] for item in self.TKTreeview.selection()]

    def get_parent(self, item):
        return self.IdToKey[self.TKTreeview.parent(self.KeyToID[item])]

    def get_previous_sibling(self, item, parent_if_none=False):
        prev = self.TKTreeview.prev(self.KeyToID[item])
        if prev == "":
            result = self.get_parent(item) if parent_if_none else None
        else:
            result = self.IdToKey[prev]
        return result

    def selection_set(self, items):
        ids = [self.KeyToID[item] for item in items]
        self.TKTreeview.selection_set(ids)
