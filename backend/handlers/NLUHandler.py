from io import StringIO  # Python3

import markdown_generator as mg

from backend.handlers.ItemsWithExamplesHandler import ItemsWithExamplesHandler
from backend.models.Intent import IntentNode, Intent, IntentExample


class NLUHandler(ItemsWithExamplesHandler):

    def __init__(self, filename, *args):
        super().__init__(filename, *args)
        self.parent_object_class = Intent
        self.parent_nodes_class = IntentNode
        self.child_nodes_class = IntentExample

    def import_data(self):
        with open(self.filename, 'r', encoding='utf-8') as df:
            nlu = df.readlines()
            current_intent = None
            for line in nlu:
                if line.startswith("## intent:"):
                    heading = line.split("## intent:")[1].strip()
                    current_intent = IntentNode(Intent(name=heading), parent=self.tree)
                    self.add_to_items(heading)
                if line.startswith("- "):
                    text_example = line.split("- ")[1].strip()
                    IntentExample(name=text_example, parent=current_intent)
                    self.add_to_items(text_example)

    def export_data(self):
        result = StringIO()
        intents = []
        writer = mg.Writer(result)
        for intent in self.tree.children:
            intents.append(intent.item.name)
            writer.write_heading(f"intent:{intent.item.name}", 2)
            examples = [f"- {example.name}".strip() for example in intent.children]
            writer.writelines(examples)
        return {"result": result,
                "intents": intents}
