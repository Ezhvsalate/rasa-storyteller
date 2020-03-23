from uuid import uuid4

import PySimpleGUI as sg

from common.constants import *


class ExtendedTree(sg.Tree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def see(self, item):
        id = self.KeyToID[item]
        self.TKTreeview.see(id)

    def get_selection(self):
        return [self.IdToKey[item] for item in self.TKTreeview.selection()]

    def get_parent(self, item):
        return self.IdToKey[self.TKTreeview.parent(self.KeyToID[item])]

    def get_family_tree(self, item, tree=''):
        if item == '':
            return ''
        if tree == '':
            tree += self.TreeData.get_node_data_by_key(item)['text']
        parent = self.get_parent(item)
        parent_heading = self.TreeData.get_node_data_by_key(self.get_parent(item))['text']
        if parent_heading != 'root':
            tree = parent_heading + '-' + tree
            return self.get_family_tree(parent, tree).strip('-')
        else:
            return tree.strip('-')

    def get_family_tree_in_story_format(self, item, tree=None):
        if tree is None:
            tree = []

        node = self.TreeData.get_node_data_by_key(item)
        if not tree:
            tree.append((node['text'], node['values'][0]))

        parent = self.TreeData.get_node_data_by_key(self.get_parent(item))
        if parent['text'] != 'root':
            if node['values'][0] == TYPE_RESPONSE:
                for sibling_key in self.get_older_siblings(item):
                    sibling = self.TreeData.get_node_data_by_key(sibling_key)
                    tree.append((sibling['text'], sibling['values'][0]))
            tree.append((parent['text'], parent['values'][0]))
            return self.get_family_tree_in_story_format(self.get_parent(item), tree)
        else:
            return tree

    def get_previous_sibling(self, item, parent_if_none=False):
        prev = self.TKTreeview.prev(self.KeyToID[item])
        if prev == '':
            result = self.get_parent(item) if parent_if_none else None
        else:
            result = self.IdToKey[prev]
        return result

    def get_older_siblings(self, item, older_siblings=None):
        if older_siblings is None:
            older_siblings = []
        if self.get_previous_sibling(item):
            older_siblings.append(self.get_previous_sibling(item))
            self.get_older_siblings(self.get_previous_sibling(item), older_siblings)
        return older_siblings

    def get_next_sibling(self, item):
        next_node = self.TKTreeview.next(self.KeyToID[item])
        return self.IdToKey[next_node] if next_node != '' else None

    def get_index(self, item):
        return self.TKTreeview.index(self.KeyToID[item])

    def move_up(self, item):
        index = self.get_index(item)
        if index > 0:
            index -= 1
        parent = self.TKTreeview.parent(self.KeyToID[item])
        self.TKTreeview.move(self.KeyToID[item], parent, index)

    def move_down(self, item):
        index = self.get_index(item) + 1
        parent = self.TKTreeview.parent(self.KeyToID[item])
        self.TKTreeview.move(self.KeyToID[item], parent, index)

    def selection_set(self, items):
        ids = [self.KeyToID[item] for item in items]
        self.TKTreeview.selection_set(ids)

    def sort_alphabetically(self):
        nodes_list = self.TreeData.get_node_data_by_key('')['children']
        nodes = [(node.key, node.text) for node in nodes_list]
        nodes.sort(key=lambda tup: tup[1])
        for idx, item in enumerate(nodes):
            self.TKTreeview.move(self.KeyToID[item[0]], '', idx)

    def remove_node_and_select_nearest(self, node):
        self.TreeData.remove_node(node)
        prev_node = self.get_previous_sibling(node, parent_if_none=True)
        self.Update(values=self.TreeData)
        self.see(prev_node)
        self.selection_set([prev_node])

    def add_node_to_root_with_children(self, node, children=None):
        if children is None:
            children = []
        parent_node = self.TreeData.Insert('', key=str(uuid4()), text=node.text, values=node.values, icon=node.icon)
        for kid in children:
            self.TreeData.Insert(parent_node, key=str(uuid4()), text=kid.text, values=kid.values, icon=kid.icon)
        self.Update(values=self.TreeData)
        self.see(parent_node)
        return parent_node

    def update_node(self, key, text, values=None, icon=None):
        node_data = self.TreeData.get_node_data_by_key(key)
        if not values:
            values = node_data['values']
        if not icon:
            icon = node_data['icon']
        self.TreeData.update_node(key, text, values, icon)
        selection_before_update = self.get_selection()
        self.Update(values=self.TreeData)
        self.see(key)
        self.selection_set(selection_before_update)

    def get_last_of_family_nodes(self):
        last_of_family = []
        for key in self.TreeData.tree_dict.keys():
            node = self.TreeData.get_node_data_by_key(key)
            if not node['children'] and not self.get_next_sibling(key):
                last_of_family.append(key)
        return last_of_family
