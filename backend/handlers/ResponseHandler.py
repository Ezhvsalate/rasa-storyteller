import yaml

from backend.handlers.ItemsWithExamplesHandler import ItemsWithExamplesHandler
from backend.models.Response import Response, ResponseNode, ResponseExample


class ResponseHandler(ItemsWithExamplesHandler):
    def __init__(self, filename, *args):
        super().__init__(filename, *args)
        self.parent_object_class = Response
        self.parent_nodes_class = ResponseNode
        self.child_nodes_class = ResponseExample

    def import_data(self):
        with open(self.filename, "r", encoding="utf-8") as domain_file:
            domain_data = yaml.safe_load(domain_file.read())
            for response, texts in domain_data["responses"].items():
                response_name = response.split("utter_")[-1].strip()
                current_response = ResponseNode(
                    Response(name=response_name), parent=self.tree
                )
                self.add_to_items(response_name)
                for text in texts:
                    ResponseExample(name=text["text"], parent=current_response)
                    self.add_to_items(text["text"])

    def export_data(self):
        responses = []
        result = {}
        for response in self.tree.children:
            responses.append(f"utter_{response.item.name}")
            result[f"utter_{response.name}"] = []
            for kid in response.children:
                result[f"utter_{response.item.name}"].append(
                    {"text": str(kid.name.strip())}
                )
        return {"responses": result, "actions": responses}
