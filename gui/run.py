import os
from pathlib import Path
from time import time

import PySimpleGUI as sg

import gui.layout as lt
from common.constants import *
from forms.AddItemForm import AddItemForm
from forms.UpdateItemForm import UpdateItemForm
from forms.AddExampleForm import AddExampleForm
from forms.AddStoryItemForm import AddStoryItemForm
from forms.RemoveItemForm import RemoveItemForm
from handlers.Exporter import Exporter
from handlers.NLUHandler import NLUHandler
from handlers.ResponseHandler import ResponseHandler
from handlers.StoriesHandler import StoriesHandler


def launcher():
    import_window_layout = lt.generate_import_window_layout()
    import_window = sg.Window(LOCATE_FILES_WINDOW_NAME, import_window_layout, resizable=False)

    nlu = resp = stories = None
    while True:
        event, values = import_window.read()
        if event == ACTION_SUBMIT:
            try:
                nlu = NLUHandler(values[NLU_FILE_KEY])
                nlu.import_data()

                resp = ResponseHandler(values[DOMAIN_FILE_KEY])
                resp.import_data()

                stories = StoriesHandler(values[STORIES_FILE_KEY], nlu, resp)
                stories.import_data()
            except (FileNotFoundError, KeyError):
                sg.Popup(MSG_INVALID_OR_UNEXISTING_FILE, icon=sg.SYSTEM_TRAY_MESSAGE_ICON_WARNING, keep_on_top=True, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)

        if event in (None, ACTION_CLOSE_WINDOW):
            break
        import_window.close()

    if nlu and resp and stories:
        main_window_layout = lt.generate_main_window_layout(nlu.tree, resp.tree, stories.tree)
        main_window = sg.Window(APP_NAME, main_window_layout, resizable=False)
        main_window.read()
        nlu.sort_alphabetically()
        resp.sort_alphabetically()
        stories.sort_alphabetically()

        while True:
            event, values = main_window.read()
            if event == ACTION_ADD_INTENT:
                AddItemForm(return_to=main_window, form_name=FORM_NAME_ADD_INTENT, item_type=TYPE_INTENT, handler=nlu).process()

            if event == ACTION_ADD_RESPONSE:
                AddItemForm(return_to=main_window, form_name=FORM_NAME_ADD_RESPONSE, item_type=TYPE_RESPONSE, handler=resp).process()

            if event == ACTION_ADD_INTENT_EXAMPLE:
                AddExampleForm(return_to=main_window, parent_key=values[INTENT_TREE_KEY][0], parent_type=TYPE_INTENT, handler=nlu).process()

            if event == ACTION_ADD_RESPONSE_EXAMPLE:
                AddExampleForm(return_to=main_window, parent_key=values[RESPONSE_TREE_KEY][0], parent_type=TYPE_RESPONSE, handler=resp).process()

            if event == ACTION_UPDATE_INTENT and values[INTENT_TREE_KEY]:
                UpdateItemForm(return_to=main_window, form_name=FORM_NAME_EDIT_INTENT, updated_item_key=values[INTENT_TREE_KEY][0], updated_item_type=TYPE_INTENT, handler=nlu,
                               stories=stories).process()

            if event == ACTION_UPDATE_RESPONSE and values[RESPONSE_TREE_KEY]:
                UpdateItemForm(return_to=main_window, form_name=FORM_NAME_EDIT_ANSWER, updated_item_key=values[RESPONSE_TREE_KEY][0], updated_item_type=TYPE_RESPONSE, handler=resp,
                               stories=stories).process()

            if event == ACTION_ADD_CHILD and values[STORIES_TREE_KEY]:
                AddStoryItemForm(return_to=main_window, form_name=FORM_NAME_ADD_CHILD, parent_object_key=values[STORIES_TREE_KEY][0], stories=stories).process()

            if event == ACTION_ADD_SIBLING and values[STORIES_TREE_KEY]:
                AddStoryItemForm(return_to=main_window, form_name=FORM_NAME_ADD_SIBLING, parent_object_key=stories.tree.get_parent(values[STORIES_TREE_KEY][0]), stories=stories).process()

            if event == ACTION_MOVE_STORY_ITEM_UP and values[STORIES_TREE_KEY]:
                stories.tree.move_up(values[STORIES_TREE_KEY][0])

            if event == ACTION_MOVE_STORY_ITEM_DOWN and values[STORIES_TREE_KEY]:
                stories.tree.move_down(values[STORIES_TREE_KEY][0])

            if event == ACTION_REMOVE_RESPONSE and values[RESPONSE_TREE_KEY]:
                RemoveItemForm(item_key=values[RESPONSE_TREE_KEY][0], item_type=TYPE_RESPONSE, handler=resp, stories=stories).process()

            if event == ACTION_REMOVE_INTENT and values[INTENT_TREE_KEY]:
                RemoveItemForm(item_key=values[INTENT_TREE_KEY][0], item_type=TYPE_INTENT, handler=nlu, stories=stories).process()

            if event == ACTION_REMOVE_STORY_ITEM and values[STORIES_TREE_KEY]:
                stories.tree.remove_node_and_select_nearest(values[STORIES_TREE_KEY][0])
                stories.sort_alphabetically()

            if event == ACTION_ADD_NEW_ITEM_AS_A_CHILD and values[STORIES_TREE_KEY]:
                parent_key = values[STORIES_TREE_KEY][0]
                parent_type = stories.tree.TreeData.get_node_data_by_key(parent_key)['values'][0]
                handler = nlu if parent_type == TYPE_RESPONSE else resp
                item_type = TYPE_INTENT if parent_type == TYPE_RESPONSE else TYPE_RESPONSE
                new_item = AddItemForm(return_to=main_window, form_name=FORM_NAME_ADD_STORY_ITEM, item_type=item_type, handler=handler).process()
                if new_item:
                    stories.add_item(parent_key, parent_type, handler.tree_data.get_node_data_by_key(new_item)['text'])

            if event in (ACTION_UPDATE_RESPONSE, ACTION_REMOVE_RESPONSE, ACTION_ADD_RESPONSE_EXAMPLE) and not values[RESPONSE_TREE_KEY] \
                    or event in (ACTION_UPDATE_INTENT, ACTION_REMOVE_INTENT, ACTION_ADD_INTENT_EXAMPLE) and not values[INTENT_TREE_KEY] \
                    or event in (ACTION_ADD_CHILD, ACTION_ADD_SIBLING, ACTION_REMOVE_STORY_ITEM, ACTION_ADD_NEW_ITEM_AS_A_CHILD,
                                 ACTION_MOVE_STORY_ITEM_UP, ACTION_MOVE_STORY_ITEM_DOWN) and not values[STORIES_TREE_KEY]:
                sg.Popup(MSG_FIRST_SELECT_ITEM, icon=sg.SYSTEM_TRAY_MESSAGE_ICON_WARNING, keep_on_top=True, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)

            if event == ACTION_EXPORT_DATA:
                Path(f"{os.getcwd()}/export").mkdir(exist_ok=True, parents=False)
                ts_suffix = int(time())
                exporter = Exporter(nlu, resp, stories, f"export/nlu_{ts_suffix}.md", f"export/domain_{ts_suffix}.yml", f"export/stories_{ts_suffix}.md")
                exporter.export()
                sg.Popup(MSG_EXPORT_SUCCESSFUL, icon=sg.SYSTEM_TRAY_MESSAGE_ICON_INFORMATION, keep_on_top=True, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)

            if event in (None, ACTION_CLOSE_WINDOW):
                break
        main_window.close()


if __name__ == '__main__':
    launcher()
