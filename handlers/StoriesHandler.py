from io import StringIO

from anytree import RenderTree
from anytree.resolver import Resolver
from anytree.search import find

from common.constants import *
from core.EditableTreeData import EditableTreeData
from handlers import NLUHandler
from handlers import ResponseHandler
from handlers.AbstractHandler import AbstractHandler
from models.BaseNode import BaseNode, BaseItem
from models.Intent import IntentStoryNode
from models.Response import ResponseStoryNode


class StoriesHandler(AbstractHandler):

    def __init__(self, filename, nlu: NLUHandler, resp: ResponseHandler):
        super().__init__(filename)
        self.filename = filename
        self.tree = BaseNode(BaseItem(name="root"))
        self.nlu = nlu
        self.resp = resp
        self.resolver = Resolver("name")

    def import_data(self):
        with open(self.filename, 'r', encoding='utf-8') as stories_file:
            stories = stories_file.readlines()
            for line in stories:
                if line.startswith("## "):
                    # new story should start from root
                    current_response = self.tree
                    current_intent = None

                elif line.startswith("* "):  # intent
                    intent_heading = line.split("* ")[-1].strip()
                    if find(current_response, lambda n: n.name == intent_heading and isinstance(n, IntentStoryNode), maxlevel=2):
                        current_intent = find(current_response, lambda n: n.name == intent_heading and isinstance(n, IntentStoryNode), maxlevel=2)
                    else:
                        nlu_node = find(self.nlu.tree, lambda n: n.name == intent_heading)
                        current_intent = IntentStoryNode(item=nlu_node.item, parent=current_response)

                elif line.strip().startswith("- "):  # response
                    response_heading = line.split("- ")[-1].split("utter_")[-1].strip()
                    if find(current_intent, lambda n: n.name == response_heading and isinstance(n, ResponseStoryNode), maxlevel=2):
                        current_response = find(current_intent, lambda n: n.name == response_heading and isinstance(n, ResponseStoryNode), maxlevel=2)
                    else:
                        resp_node = find(self.resp.tree, lambda n: n.name == response_heading)
                        current_response = ResponseStoryNode(item=resp_node.item, parent=current_intent)

    def export_to_pysg_tree(self):
        def insert_branch(branch, parent):
            values = " | ".join([kid.name for kid in branch.item.own_tree.children])
            branch_type = TYPE_INTENT if isinstance(branch, IntentStoryNode) else TYPE_RESPONSE
            new_parent = tree_data.Insert(parent=parent, key=branch.id, text=branch.item.name, values=[branch_type, values])
            for child in branch.children:
                insert_branch(child, new_parent)

        tree_data = EditableTreeData()
        for item in self.tree.children:
            insert_branch(item, '')

        self.export_data()
        return tree_data

    def export_data(self):
        result = StringIO()
        for leaf in self.tree.leaves:
            path = list(leaf.iter_path_reverse())[:-1][::-1]
            story_heading = "-".join([item.name for item in path if isinstance(item, IntentStoryNode)])
            result.write(f"\n\n## {story_heading}")
            for item in path:
                if isinstance(item, IntentStoryNode):
                    result.write(f"\n* {item}")
                elif isinstance(item, ResponseStoryNode):
                    result.write(f"\n    - utter_{item}")
        return result

    def get_parent_node_by_object_id(self, object_id):
        parent_node = find(self.tree, lambda n: n.id == object_id).parent
        return parent_node

    def get_available_children_by_parent_id(self, parent_object_id):
        parent_node = find(self.tree, lambda n: n.id == parent_object_id)
        available_values = None
        if isinstance(parent_node, ResponseStoryNode) or isinstance(parent_node, BaseNode):
            available_values = sorted([child.name for child in self.nlu.tree.children])
        elif isinstance(parent_node, IntentStoryNode):
            available_values = sorted([child.name for child in self.resp.tree.children])
        return available_values

    def add_item(self, parent_object_id, text):
        parent_node = find(self.tree, lambda n: n.id == parent_object_id)
        existing_node = find(parent_node, lambda n: n.name == text, maxlevel=2)
        if existing_node:
            new_item = existing_node
        elif isinstance(parent_node, ResponseStoryNode) or isinstance(parent_node, BaseNode):
            add_node = find(self.nlu.tree, lambda n: n.name == text)
            new_item = IntentStoryNode(item=add_node.item, parent=parent_node)
        elif isinstance(parent_node, IntentStoryNode):
            add_node = find(self.resp.tree, lambda n: n.name == text)
            new_item = ResponseStoryNode(item=add_node.item, parent=parent_node)
        return new_item

    def remove_item(self, node_id):
        node = find(self.tree, lambda n: n.id == node_id)
        print(node.item.story_tree)
        node.parent = None
        print(node.item.story_tree)

