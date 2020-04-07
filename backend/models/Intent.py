from uuid import uuid4

from anytree import NodeMixin


class Intent:
    def __init__(self, name):
        self.name = name
        self.own_tree = None
        self.story_tree = []

    def __repr__(self):
        return str(self.name)


class IntentNode(NodeMixin):
    def __init__(self, item: Intent, parent=None):
        self.item = item
        self.parent = parent
        self.name = self.item.name

    def _pre_detach(self, parent):
        self.item.own_tree = None

    def _pre_attach(self, parent):
        self.item.own_tree = self

    def __repr__(self):
        return str(self.name)


class IntentStoryNode(NodeMixin):
    def __init__(self, item: Intent, parent=None):
        self.item = item
        self.parent = parent
        self.name = self.item.name
        self.id = str(uuid4())

    def _pre_detach(self, parent):
        self.item.story_tree.remove(self)

    def _pre_attach(self, parent):
        self.item.story_tree.append(self)

    def __repr__(self):
        return str(self.name + '_' + self.id)


class IntentExample(NodeMixin):

    def __init__(self, name, parent: IntentNode):
        super(IntentExample, self).__init__()
        self.name = name
        self.parent = parent

    def __repr__(self):
        return str(self.name)
