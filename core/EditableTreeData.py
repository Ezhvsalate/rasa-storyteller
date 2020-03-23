import json

import PySimpleGUI as sg


class EditableTreeData(sg.TreeData):
    def __init__(self):
        super().__init__()

    def _show_node(self, node, level):
        node_data = {
            "key": node.key,
            "text": node.text,
            "values": [value for value in node.values],
            "children": [self._show_node(child, level + 1) for child in node.children]
        }
        return node_data

    def get_node_data_by_key(self, key):
        node = self.tree_dict[key]
        return {"key": key,
                "text": node.text,
                "values": node.values,
                "icon": node.icon,
                "children": node.children}

    def Insert(self, parent, key, text, values, icon=None):
        node = self.Node(parent, key, text, values, icon)
        self.tree_dict[key] = node
        parent_node = self.tree_dict[parent]
        parent_node._Add(node)
        return node.key

    def update_node(self, key, text, values, icon=None):
        node = self.tree_dict[key]
        node.text = text
        node.values = values
        node.icon = icon
        return node

    def remove_node(self, key):
        node = self.tree_dict[key]
        self.tree_dict[node.parent].children.remove(node)
        self.tree_dict.pop(key)
        del node

    def dump(self):
        return self._show_node(self.root_node, 1)['children']

    def __repr__(self):
        return json.dumps(self._show_node(self.root_node, 1), indent=4, ensure_ascii=False)
