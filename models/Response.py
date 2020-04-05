from anytree import NodeMixin


class Response(NodeMixin):

    def __init__(self, name, parent=None, children=None):
        super(Response, self).__init__()
        self.name = name
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return str(self.name)
