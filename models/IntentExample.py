from anytree import NodeMixin

from models.Intent import IntentNode


class IntentExample(NodeMixin):

    def __init__(self, name, parent: IntentNode):
        super(IntentExample, self).__init__()
        self.name = name
        self.parent = parent

    def __repr__(self):
        return str(self.name)

