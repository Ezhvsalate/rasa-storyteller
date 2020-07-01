from uuid import uuid4

from anytree import NodeMixin


class Response:
    def __init__(self, name):
        self.name = name
        self.own_tree = None
        self.story_tree = []

    def __repr__(self):
        return f"response_object_{self.name}"


class ResponseNode(NodeMixin):
    def __init__(self, item, parent=None):
        self.item = item
        self.parent = parent
        self.name = self.item.name

    def _pre_detach(self, parent):
        self.item.own_tree = None

    def _pre_attach(self, parent):
        self.item.own_tree = self

    def __repr__(self):
        return f"response_node_{self.name}"


class ResponseExample(NodeMixin):
    def __init__(self, name, parent: ResponseNode):
        super(ResponseExample, self).__init__()
        self.name = name
        self.parent = parent

    def __repr__(self):
        return f"response_example_{self.name}"


class ResponseStoryNode(NodeMixin):
    def __init__(self, item: Response, parent=None):
        self.item = item
        self.parent = parent
        self.name = self.item.name
        self.id = str(uuid4())

    def _pre_detach(self, parent):
        self.item.story_tree.remove(self)

    def _pre_attach(self, parent):
        self.item.story_tree.append(self)

    def __repr__(self):
        return f"story_response_node_{self.name}_{self.id}"
