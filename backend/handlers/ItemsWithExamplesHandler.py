from abc import ABC

from PySimpleGUI import TreeData
from anytree import Node
from anytree.search import find

from backend.handlers.AbstractHandler import AbstractHandler
from backend.models.BaseNode import BaseNode, BaseItem
from backend.models.Intent import IntentNode
from common.constants import QUESTION_ICON, ANSWER_ICON


class ItemsWithExamplesHandler(AbstractHandler, ABC):
    def __init__(self, filename, *args):
        super().__init__(filename, *args)
        self.filename = filename
        self.items = []
        self.tree = Node("root", text="")
        self.parent_nodes_class = BaseNode
        self.parent_object_class = BaseItem
        self.child_nodes_class = Node

    def add_to_items(self, key):
        if key in self.items:
            raise ValueError(f"There is already item with key {key} in this list.")
        else:
            self.items.append(key)

    def export_to_pysg_tree(self):
        parent_icon = (
            QUESTION_ICON if self.parent_nodes_class == IntentNode else ANSWER_ICON
        )
        tree_data = TreeData()
        for item in self.tree.children:
            tree_data.Insert(
                parent="",
                key=item.item.name,
                text=item.item.name,
                values=[],
                icon=parent_icon,
            )
            for example in item.children:
                tree_data.Insert(
                    parent=item.item.name,
                    key=example.name,
                    text=example.name,
                    values=[],
                    icon=ANSWER_ICON,
                )
        return tree_data

    def add_node_with_kids(self, parent_name, *kids):
        item = self.parent_object_class(name=parent_name)
        current_parent = self.parent_nodes_class(item, parent=self.tree)
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
        if isinstance(node, self.parent_nodes_class):
            node.item.name = new_value
            for story_item in node.item.story_tree:
                story_item.name = new_value

    def remove_node(self, node):
        node = find(self.tree, lambda n: n.name == node, maxlevel=3)
        if not hasattr(node, "item") or not node.item.story_tree:
            node.parent = None
            self.items.remove(node.name)
            for kid in node.children:
                self.items.remove(kid.name)
        else:
            raise ValueError("Item is used in stories and can't be removed.")
