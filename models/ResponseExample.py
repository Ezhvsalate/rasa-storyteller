from anytree import NodeMixin

from models.Response import Response


class ResponseExample(NodeMixin):

    def __init__(self, name, parent: Response):
        super(ResponseExample, self).__init__()
        self.name = name
        self.parent = parent

    def __repr__(self):
        return str(self.name)

