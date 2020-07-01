from backend.handlers import StoriesHandler


class RemoveStoryItemForm(object):
    def __init__(self, item_key, stories: StoriesHandler, tree):
        self.item_key = item_key
        self.stories = stories
        self.tree = tree

    def layout(self):
        pass

    def process(self):
        prev_node = self.tree.get_previous_sibling(self.item_key, parent_if_none=True)
        self.stories.remove_item(self.item_key)
        self.tree.Update(self.stories.export_to_pysg_tree())
        self.tree.see(prev_node)
        self.tree.selection_set([prev_node])
