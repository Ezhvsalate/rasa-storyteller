from io import StringIO
from uuid import uuid4

from common.constants import *
from core.EditableTreeData import EditableTreeData
from core.ExtendedTree import ExtendedTree
from handlers.AbstractHandler import AbstractHandler


class StoriesHandler(AbstractHandler):

    def __init__(self, filename, nlu, resp):
        super().__init__(filename, nlu, resp)
        self.filename = filename
        self.response_list = []
        self.tree_data = EditableTreeData()
        self.nlu = nlu
        self.resp = resp
        self.chains = {}
        self.tree = ExtendedTree(data=self.tree_data,
                                 headings=['Type', 'Text'],
                                 col0_width=23,
                                 col_widths=[7, 50],
                                 key=STORIES_TREE_KEY,
                                 right_click_menu=['Right', ['!Fast actions',
                                                             ACTION_ADD_CHILD,
                                                             ACTION_ADD_SIBLING,
                                                             ACTION_MOVE_STORY_ITEM_UP,
                                                             ACTION_MOVE_STORY_ITEM_DOWN,
                                                             ACTION_REMOVE_STORY_ITEM,
                                                             ACTION_ADD_NEW_ITEM_AS_A_CHILD]],
                                 **TREE_LAYOUT_COMMON_PARAMS)

    def import_data(self):

        with open(self.filename, 'r', encoding='utf-8') as stories_file:
            stories = stories_file.readlines()
            for line in stories:
                if line.startswith("## "):
                    current_answer = ''
                    current_intent = None
                    last_chain_indent = ''
                    last_chain_response = ''

                elif line.startswith("* "):
                    heading = line.split("* ")[-1].strip()
                    current_chain = str(last_chain_response + '-' + heading).strip("-")
                    if current_chain not in self.chains:
                        texts = " | ".join([child.text for child in self.nlu.tree_data.get_node_data_by_key(self.nlu.items[heading])['children']])
                        current_intent = self.tree_data.Insert(current_answer, key=str(uuid4()), text=heading, values=[TYPE_INTENT, texts], icon=QUESTION_ICON)
                        self.chains[current_chain] = current_intent
                    else:
                        current_intent = self.chains[current_chain]
                    last_chain_indent = current_chain

                elif line.strip().startswith("- "):
                    heading = line.split("- ")[-1].strip()
                    current_chain = (last_chain_indent + '-' + heading).strip("-")
                    if current_chain not in self.chains:
                        texts = " | ".join([child.text for child in self.resp.tree_data.get_node_data_by_key(self.resp.items[heading.split("utter_")[-1]])['children']])
                        current_answer = self.tree_data.Insert(current_intent, key=str(uuid4()), text=heading.split("utter_")[-1], values=[TYPE_RESPONSE, texts], icon=ANSWER_ICON)
                        self.chains[current_chain] = current_answer
                    else:
                        current_answer = self.chains[current_chain]
                    last_chain_response = current_chain

    def export_data(self):
        result = StringIO()
        for key in self.tree.get_last_of_family_nodes():
            story = self.tree.get_family_tree_in_story_format(key)[::-1]
            story_heading = "-".join([item[0] for item in story if item[1] == TYPE_INTENT])
            result.write(f"\n\n## {story_heading}")
            for item in story:
                if item[1] == TYPE_INTENT:
                    result.write(f"\n* {item[0]}")
                elif item[1] == TYPE_RESPONSE:
                    result.write(f"\n    - utter_{item[0]}")
        return result

    def add_item(self, parent_key, parent_type, text):
        chain_value = (self.tree.get_family_tree(parent_key) + '-' + text).strip("-")
        current_obj = ''
        object_type = TYPE_INTENT if parent_type in (TYPE_RESPONSE, 'root') else TYPE_RESPONSE
        handler = self.nlu if object_type == TYPE_INTENT else self.resp
        icon = QUESTION_ICON if object_type == TYPE_INTENT else ANSWER_ICON
        if chain_value in self.chains:
            current_obj = self.chains[chain_value]
        else:
            object_texts = " | ".join([child.text for child in handler.tree_data.get_node_data_by_key(handler.items[text])['children']])
            current_obj = self.tree_data.Insert(parent_key, key=str(uuid4()), text=text, values=[object_type, object_texts], icon=QUESTION_ICON)
            self.chains['chain_value'] = current_obj
            self.tree.Update(values=self.tree_data)
        self.tree.see(current_obj)
        self.tree.selection_set([current_obj])
        return current_obj

    def sort_alphabetically(self):
        self.tree.sort_alphabetically()
