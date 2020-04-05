from abc import ABC

from anytree import Node
from anytree.search import find

from core.EditableTreeData import EditableTreeData
from handlers.AbstractHandler import AbstractHandler


class ItemsWithExamplesHandler(AbstractHandler, ABC):

    def __init__(self, filename, *args):
        super().__init__(filename, *args)
        self.filename = filename
        self.items = []
        self.tree = Node("root", text='')
        self.parent_nodes_class = Node
        self.child_nodes_class = Node

    def add_to_items(self, key):
        if key in self.items:
            raise ValueError(f"There is already item with key {key} in this list.")
        else:
            self.items.append(key)

    def export_to_pysg_tree(self):
        tree_data = EditableTreeData()
        for item in self.tree.children:
            tree_data.Insert(parent='', key=item.name, text=item.name, values=[])
            for example in item.children:
                tree_data.Insert(parent=item.name, key=example.name, text=example.name, values=[])
        return tree_data

    def add_node_with_kids(self, parent_name, *kids):
        current_parent = self.parent_nodes_class(name=parent_name, parent=self.tree)
        self.add_to_items(parent_name)
        for kid in kids:
            self.child_nodes_class(name=kid, parent=current_parent)
            self.add_to_items(kid)

    def add_example_to_node(self, parent, text):
        selected_node = find(self.tree, lambda node: node.name == parent, maxlevel=3)
        if isinstance(selected_node, self.parent_nodes_class):
            parent = selected_node
        elif isinstance(selected_node, self.child_nodes_class):
            parent = selected_node.parent
        else:
            raise ValueError("Can't find item to add example.")
        self.child_nodes_class(name=text, parent=parent)
        self.add_to_items(text)

    def update_node_value(self, node, new_value):
        node = find(self.tree, lambda n: n.name == node, maxlevel=3)
        self.items.remove(node.name)
        self.add_to_items(new_value)
        node.name = new_value

    def remove_node(self, node):
        node = find(self.tree, lambda n: n.name == node, maxlevel=3)
        node.parent = None
        self.items.remove(node.name)
