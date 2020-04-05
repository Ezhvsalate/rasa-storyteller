import yaml

from handlers.ItemsWithExamplesHandler import ItemsWithExamplesHandler
from models.Response import Response
from models.ResponseExample import ResponseExample


class ResponseHandler(ItemsWithExamplesHandler):

    def __init__(self, filename, *args):
        super().__init__(filename, *args)
        self.parent_nodes_class = Response
        self.child_nodes_class = ResponseExample

    def import_data(self):
        with open(self.filename, 'r', encoding='utf-8') as domain_file:
            domain_data = yaml.safe_load(domain_file.read())
            for response, texts in domain_data['responses'].items():
                response_name = response.split('utter_')[-1].strip()
                current_response = Response(name=response_name, parent=self.tree)
                self.add_to_items(response_name)
                for text in texts:
                    ResponseExample(name=text['text'], parent=current_response)
                    self.add_to_items(text['text'])

    def export_data(self):
        responses = []
        result = {}
        for response in self.tree.children:
            responses.append(f"utter_{response.text}")
            result[f"utter_{response.text}"] = []
            for kid in response.children:
                result[f"utter_{response.text}"].append({"text": str(kid.text.strip())})
        return {"responses": result,
                "actions": responses}
