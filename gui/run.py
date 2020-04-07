import PySimpleGUI as sg

import gui.layout as lt
from backend.handlers.NLUHandler import NLUHandler
from backend.handlers.ResponseHandler import ResponseHandler
from backend.handlers.StoriesHandler import StoriesHandler
from common.constants import *
from gui.core.ExtendedTree import ExtendedTree
from gui.forms.AddExampleForm import AddExampleForm
from gui.forms.AddItemForm import AddItemForm
from gui.forms.AddStoryItemForm import AddStoryItemForm
from gui.forms.RemoveItemForm import RemoveItemForm
from gui.forms.RemoveStoryItemForm import RemoveStoryItemForm
from gui.forms.UpdateItemForm import UpdateItemForm


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

    if nlu:  # and resp and stories:
        nlu_tree = ExtendedTree(data=nlu.export_to_pysg_tree(),
                                headings=[],
                                col0_width=80,
                                key=INTENT_TREE_KEY,
                                right_click_menu=['Right', ['!Fast actions',
                                                            ACTION_ADD_INTENT,
                                                            ACTION_ADD_INTENT_EXAMPLE,
                                                            ACTION_UPDATE_INTENT,
                                                            ACTION_REMOVE_INTENT]],
                                **TREE_LAYOUT_COMMON_PARAMS
                                )
        resp_tree = ExtendedTree(data=resp.export_to_pysg_tree(),
                                 headings=[],
                                 col0_width=80,
                                 key=RESPONSE_TREE_KEY,
                                 right_click_menu=['Right', ['!Fast actions',
                                                             ACTION_ADD_RESPONSE,
                                                             ACTION_ADD_RESPONSE_EXAMPLE,
                                                             ACTION_UPDATE_RESPONSE,
                                                             ACTION_REMOVE_RESPONSE]],
                                 **TREE_LAYOUT_COMMON_PARAMS
                                 )

        stories_tree = ExtendedTree(data=stories.export_to_pysg_tree(),
                                    headings=['Type', 'Text'],
                                    col0_width=23,
                                    col_widths=[7, 50],
                                    key=STORIES_TREE_KEY,
                                    right_click_menu=['Right', ['!Fast actions',
                                                                ACTION_ADD_CHILD,
                                                                ACTION_ADD_SIBLING,
                                                                ACTION_REMOVE_STORY_ITEM,
                                                                ACTION_ADD_NEW_ITEM_AS_A_CHILD]],
                                    **TREE_LAYOUT_COMMON_PARAMS)

        main_window_layout = lt.generate_main_window_layout(nlu_tree, resp_tree, stories_tree)
        main_window = sg.Window(APP_NAME, main_window_layout, resizable=False)
        main_window.read()

        while True:
            event, values = main_window.read()
            print(event, values)
            if event == ACTION_ADD_INTENT:
                AddItemForm(return_to=main_window, form_name=FORM_NAME_ADD_INTENT, item_type=TYPE_INTENT, handler=nlu, tree=nlu_tree).process()

            if event == ACTION_ADD_RESPONSE:
                AddItemForm(return_to=main_window, form_name=FORM_NAME_ADD_RESPONSE, item_type=TYPE_RESPONSE, handler=resp, tree=resp_tree).process()

            if event == ACTION_ADD_INTENT_EXAMPLE:
                AddExampleForm(return_to=main_window, parent_name=values[INTENT_TREE_KEY][0], handler=nlu, tree=nlu_tree).process()

            if event == ACTION_ADD_RESPONSE_EXAMPLE:
                AddExampleForm(return_to=main_window, parent_name=values[RESPONSE_TREE_KEY][0], handler=resp, tree=resp_tree).process()

            if event == ACTION_UPDATE_INTENT and values[INTENT_TREE_KEY]:
                UpdateItemForm(return_to=main_window, form_name=FORM_NAME_EDIT_INTENT, updated_item_key=values[INTENT_TREE_KEY][0], updated_item_type=TYPE_INTENT, handler=nlu,
                               tree=nlu_tree, stories=stories, stories_tree=stories_tree).process()

            if event == ACTION_UPDATE_RESPONSE and values[RESPONSE_TREE_KEY]:
                UpdateItemForm(return_to=main_window, form_name=FORM_NAME_EDIT_ANSWER, updated_item_key=values[RESPONSE_TREE_KEY][0], updated_item_type=TYPE_RESPONSE, handler=resp,
                               tree=resp_tree, stories=stories, stories_tree=stories_tree).process()

            if event == ACTION_REMOVE_INTENT and values[INTENT_TREE_KEY]:
                RemoveItemForm(item_key=values[INTENT_TREE_KEY][0], item_type=TYPE_INTENT, handler=nlu, stories=stories, tree=nlu_tree).process()

            if event == ACTION_REMOVE_RESPONSE and values[RESPONSE_TREE_KEY]:
                RemoveItemForm(item_key=values[RESPONSE_TREE_KEY][0], item_type=TYPE_RESPONSE, handler=resp, stories=stories, tree=resp_tree).process()

            if event == ACTION_ADD_CHILD and values[STORIES_TREE_KEY]:
                AddStoryItemForm(return_to=main_window, form_name=FORM_NAME_ADD_CHILD, parent_object_key=values[STORIES_TREE_KEY][0], stories=stories, tree=stories_tree).process()

            if event == ACTION_ADD_SIBLING and values[STORIES_TREE_KEY]:
                parent_item = stories.get_parent_node_by_object_id(values[STORIES_TREE_KEY][0])
                AddStoryItemForm(return_to=main_window, form_name=FORM_NAME_ADD_SIBLING, parent_object_key=parent_item.id, stories=stories, tree=stories_tree).process()

            if event == ACTION_REMOVE_STORY_ITEM and values[STORIES_TREE_KEY]:
                RemoveStoryItemForm(item_key=values[STORIES_TREE_KEY][0], stories=stories, tree=stories_tree).process()

            # if event == ACTION_ADD_NEW_ITEM_AS_A_CHILD and values[STORIES_TREE_KEY]:
            #     parent_key = values[STORIES_TREE_KEY][0]
            #     parent_type = stories.tree.TreeData.get_node_data_by_key(parent_key)['values'][0]
            #     handler = nlu if parent_type == TYPE_RESPONSE else resp
            #     item_type = TYPE_INTENT if parent_type == TYPE_RESPONSE else TYPE_RESPONSE
            #     new_item = AddItemForm(return_to=main_window, form_name=FORM_NAME_ADD_STORY_ITEM, item_type=item_type, handler=handler).process()
            #     if new_item:
            #         stories.add_item(parent_key, parent_type, handler.tree_data.get_node_data_by_key(new_item)['text'])

            if event in (ACTION_UPDATE_RESPONSE, ACTION_REMOVE_RESPONSE, ACTION_ADD_RESPONSE_EXAMPLE) and not values[RESPONSE_TREE_KEY] \
                    or event in (ACTION_UPDATE_INTENT, ACTION_REMOVE_INTENT, ACTION_ADD_INTENT_EXAMPLE) and not values[INTENT_TREE_KEY] \
                    or event in (ACTION_ADD_CHILD, ACTION_ADD_SIBLING, ACTION_REMOVE_STORY_ITEM, ACTION_ADD_NEW_ITEM_AS_A_CHILD,
                                 ) and not values[STORIES_TREE_KEY]:
                sg.Popup(MSG_FIRST_SELECT_ITEM, icon=sg.SYSTEM_TRAY_MESSAGE_ICON_WARNING, keep_on_top=True, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)

            # if event == ACTION_EXPORT_DATA:
            #     Path(f"{os.getcwd()}/export").mkdir(exist_ok=True, parents=False)
            #     ts_suffix = int(time())
            #     exporter = Exporter(nlu, resp, stories, f"export/nlu_{ts_suffix}.md", f"export/domain_{ts_suffix}.yml", f"export/stories_{ts_suffix}.md")
            #     exporter.export()
            #     sg.Popup(MSG_EXPORT_SUCCESSFUL, icon=sg.SYSTEM_TRAY_MESSAGE_ICON_INFORMATION, keep_on_top=True, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)

            if event in (None, ACTION_CLOSE_WINDOW):
                break
        main_window.close()


if __name__ == '__main__':
    launcher()
