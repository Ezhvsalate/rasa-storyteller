from anytree import NodeMixin


class Intent(NodeMixin):

    def __init__(self, name, parent=None, children=None):
        super(Intent, self).__init__()
        self.name = name
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return str(self.name)
