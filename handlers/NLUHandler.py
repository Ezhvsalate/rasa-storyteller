from io import StringIO  # Python3

import markdown_generator as mg

from handlers.ItemsWithExamplesHandler import ItemsWithExamplesHandler
from models.Intent import Intent
from models.IntentExample import IntentExample


class NLUHandler(ItemsWithExamplesHandler):

    def __init__(self, filename, *args):
        super().__init__(filename, *args)
        self.parent_nodes_class = Intent
        self.child_nodes_class = IntentExample

    def import_data(self):
        with open(self.filename, 'r', encoding='utf-8') as df:
            nlu = df.readlines()
            current_intent = None
            for line in nlu:
                if line.startswith("## intent:"):
                    heading = line.split("## intent:")[1].strip()
                    current_intent = Intent(name=heading, parent=self.tree)
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
            intents.append(intent.text)
            writer.write_heading(f"intent:{intent.text}", 2)
            examples = [f"- {example.text}".strip() for example in intent.children]
            writer.writelines(examples)
        return {"result": result,
                "intents": intents}
