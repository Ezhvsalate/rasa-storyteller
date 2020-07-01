import json
from io import StringIO  # Python3

import markdown_generator as mg
from anytree.search import find

from backend.handlers.ItemsWithExamplesHandler import ItemsWithExamplesHandler
from backend.models.Intent import IntentNode, Intent, IntentExample


class NLUHandler(ItemsWithExamplesHandler):
    def __init__(self, filename, *args):
        super().__init__(filename, *args)
        self.parent_object_class = Intent
        self.parent_nodes_class = IntentNode
        self.child_nodes_class = IntentExample

    def import_data(self):
        current_intent = None
        try:
            with open(self.filename, "r", encoding="utf-8") as df:
                nlu = json.loads(df.read())
                for example in nlu["rasa_nlu_data"]["common_examples"]:
                    if example["intent"] not in self.items:
                        current_intent = IntentNode(
                            Intent(name=example["intent"]), parent=self.tree
                        )
                        self.add_to_items(example["intent"])
                    else:
                        current_intent = find(
                            self.tree,
                            lambda node: node.name == example["intent"],
                            maxlevel=2,
                        )
                    IntentExample(name=example["text"], parent=current_intent)
                    self.add_to_items(example["text"])

        except json.JSONDecodeError:  # suggest it's markdown
            with open(self.filename, "r", encoding="utf-8") as df:
                nlu = df.readlines()
                for line in nlu:
                    if line.startswith("## intent:"):
                        heading = line.split("## intent:")[1].strip()
                        current_intent = IntentNode(
                            Intent(name=heading), parent=self.tree
                        )
                        self.add_to_items(heading)
                    if line.startswith("- "):
                        text_example = line.split("- ")[1].strip()
                        IntentExample(name=text_example, parent=current_intent)
                        self.add_to_items(text_example)

    def export_data(self):
        result = StringIO()
        intents = []
        writer = mg.Writer(result)
        result_json = {
            "rasa_nlu_data": {
                "common_examples": [],
                "regex_features": [],
                "lookup_tables": [],
                "entity_synonyms": [],
            }
        }

        for intent in self.tree.children:
            intents.append(intent.item.name)
            writer.write_heading(f"intent:{intent.item.name}", 2)
            examples_list = [example.name.strip() for example in intent.children]
            examples_md = [f"- {example}" for example in examples_list]
            writer.writelines(examples_md)
            for example in examples_list:
                result_json["rasa_nlu_data"]["common_examples"].append(
                    {"intent": intent.item.name, "example": example}
                )

        return {"result": result, "result_json": result_json, "intents": intents}
