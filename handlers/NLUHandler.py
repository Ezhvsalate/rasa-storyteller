from io import StringIO  # Python3
from uuid import uuid4

import markdown_generator as mg

from common.constants import *
from core.EditableTreeData import EditableTreeData
from core.ExtendedTree import ExtendedTree
from handlers.Handler import Handler


class NLUHandler(Handler):

    def __init__(self, filename, *args):
        super().__init__(filename, *args)
        self.filename = filename
        self.items = {}
        self.tree_data = EditableTreeData()
        self.tree = ExtendedTree(data=self.tree_data,
                                 headings=[],
                                 col0_width=80,
                                 key=INTENT_TREE_KEY,
                                 right_click_menu=['Right', ['!Fast actions',
                                                             ACTION_ADD_INTENT,
                                                             ACTION_ADD_INTENT_EXAMPLE,
                                                             ACTION_UPDATE_INTENT,
                                                             ACTION_REMOVE_INTENT]],
                                 **TREE_LAYOUT_COMMON_PARAMS)

    def import_data(self):
        with open(self.filename, 'r', encoding='utf-8') as df:
            nlu = df.readlines()
            current_intent = None
            for line in nlu:
                if line.startswith("## intent:"):
                    heading = line.split("## intent:")[1].strip()
                    current_intent = self.tree_data.Insert('', key=str(uuid4()), text=heading, values=[], icon=ANSWER_ICON)
                    self.items[heading] = current_intent
                if line.startswith("- "):
                    answer = line.split("- ")[1].strip()
                    self.tree_data.insert(current_intent, key=str(uuid4()), text=answer, values=[], icon=QUESTION_ICON)

    def export_data(self):
        result = StringIO()
        intents = []
        writer = mg.Writer(result)
        for item in self.tree_data.dump():
            intents.append(item['text'])
            writer.write_heading(f"intent:{item['text']}", 2)
            examples = [f"- {str(kid['text'])}".strip() for kid in item['children']]
            writer.writelines(examples)
        return {"result": result,
                "intents": intents}

    def sort_alphabetically(self):
        self.tree.sort_alphabetically()
