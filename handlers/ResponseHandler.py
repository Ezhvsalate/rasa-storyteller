from uuid import uuid4

import yaml


from common.constants import *
from core.EditableTreeData import EditableTreeData
from core.ExtendedTree import ExtendedTree
from handlers.Handler import Handler


class ResponseHandler(Handler):

    def __init__(self, filename, *args):
        super().__init__(filename, *args)
        self.filename = filename
        self.tree_data = EditableTreeData()
        self.items = {}

        self.tree = ExtendedTree(data=self.tree_data,
                                 headings=[],
                                 col0_width=80,
                                 key=RESPONSE_TREE_KEY,
                                 right_click_menu=['Right', ['!Fast actions',
                                                             ACTION_ADD_RESPONSE,
                                                             ACTION_ADD_RESPONSE_EXAMPLE,
                                                             ACTION_UPDATE_RESPONSE,
                                                             ACTION_REMOVE_RESPONSE]],
                                 **TREE_LAYOUT_COMMON_PARAMS
                                 )

    def import_data(self):
        with open(self.filename, 'r', encoding='utf-8') as domain_file:
            domain_data = yaml.safe_load(domain_file.read())
            for response, texts in domain_data['responses'].items():
                response_name = response.split('utter_')[-1].strip()
                current_response = self.tree_data.Insert('', key=str(uuid4()), text=response_name, values=[], icon=ANSWER_ICON)
                self.items[response_name] = current_response
                for text in texts:
                    self.tree_data.Insert(current_response, key=str(uuid4()), text=text['text'], values=[], icon=ANSWER_ICON)

    def export_data(self):
        responses = []
        result = {}
        for item in self.tree_data.dump():
            responses.append(f"utter_{item['text']}")
            result[f"utter_{item['text']}"] = []
            for kid in item['children']:
                result[f"utter_{item['text']}"].append({"text": str(kid['text'].strip())})
        return {"responses": result,
                "actions": responses}

    def sort_alphabetically(self):
        self.tree.sort_alphabetically()
