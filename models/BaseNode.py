from uuid import uuid4

from anytree import NodeMixin


class BaseItem:
    def __init__(self, name):
        self.name = name
        self.node_tree = None
        self.story_tree = None

    def __repr__(self):
        return str(self.name)


class BaseNode(NodeMixin):
    def __init__(self, item, parent=None):
        self.item = item
        self.parent = parent
        self.name = self.item.name
        self.id = str(uuid4())

    def _pre_detach(self, parent):
        self.item.node_tree = None

    def _pre_attach(self, parent):
        self.item.intent_tree = self

    def __repr__(self):
        return str(self.name)