from kivy.uix.button import Button
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.app import App
from kivyDemos.kivyHomeMenuGit.kivyMenus.focusWidgets import FocusButton4,FocusWithColor
from kivyDemos.kivyHomeMenuGit.kivyMenus.tableToStringIdMapper import stringIdToDbMapper


class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")
    firstWidget = ObjectProperty(None)

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text

class FocusPopUpButton(FocusWithColor, Button):

    buttonId = StringProperty(None)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):

        if super(FocusPopUpButton, self).keyboard_on_key_down(window, keycode,
                                                         text, modifiers):
            return True
        if(keycode[1] == 'enter'):
            popup = self.parent.parent.parent.parent
            if(self.buttonId == "Save"):
                popup.obj.update_changes(popup.ids.txtinput.text)
                popup.dismiss()

            elif (self. buttonId == "cancel"):
                popup.dismiss()


class SelectableRecycleGridLayout(LayoutSelectionBehavior,
                                  RecycleGridLayout):

# @Description
#     list of cols not editable
    nonSelectable = ListProperty([])
    tableId = StringProperty("")
''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, FocusButton4):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(False)

    # @Description
    #     Every time the view is refresehd this is called
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index

        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    # @Description
    #     if not selectable don't select it
    def on_press(self):
        if (self.isIndexEditable(self.index)):
            popup = TextInputPopup(self)
            popup.firstWidget.focus = True
            popup.open()

    # @Description
    #     if enter key is pressed and check if editable, if yes open pop up else super
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if (keycode[1] == 'enter'):
            if (self.isIndexEditable(self.index)):
                popup = TextInputPopup(self)
                popup.firstWidget.focus = True
                popup.open()

        elif(keycode[1] == 'tab'):
            #if shift + tab
            if ['shift'] == modifiers:
                #get previous focused
                next = self.get_focus_previous()
                editable = False
                while(editable == False):
                    # keep going to previous until you find an editable button
                    if (isinstance(next, SelectableButton)):
                        editable = self.isIndexEditable(next.index)
                        # if not editable get previous of that
                        if(editable == False):
                            next = next.get_focus_previous()
                    # or not a part of db
                    else:
                        break


            else:
                # get next focussed
                next = self.get_focus_next()
                editable = False
                while (editable == False):
                    # keep going to next until you find an editable button
                    if (isinstance(next, SelectableButton)):
                        editable = self.isIndexEditable(next.index)
                        # if not editable get next of that
                        if (editable == False):
                            next = next.get_focus_next()
                    # or not a part of db
                    else:
                        break

            if next:
                self.focus = False

                next.focus = True
#TODO FIX THIS
        # elif (keycode[1] in ['up', 'down']):
        #     rv = self.parent
        #     direction = 'focus_next' if keycode[1] == 'down' else 'focus_previous'
        #
        #     if rv.selected_nodes:
        #         next_row = rv.selected_nodes[0]._get_focus_next(direction)
        #     else:
        #         next_row = rv.children[-1]
        #         rv.clear_selection()
        #         rv.select_node(next_row)
        #     if next_row:
        #         next_row.focus = True
        #         next = next_row.children[-1]
        #         if next and not isinstance(next, SelectableRecycleGridLayout):
        #             print("moving to {0}".format(next))
        #             next.focus = True
        #             next_row.clear_selection()
        #             next_row.select_node(next)


        else:
            return super(SelectableButton, self).keyboard_on_key_down(window, keycode,
                                                                 text, modifiers)




    def update_changes(self, txt):
        if(isinstance(self.parent, SelectableRecycleGridLayout)):
            tableId = self.parent.tableId
            if(tableId != ""):
                #get string id/table id to property mapper
                indexToPropertyMapper = stringIdToDbMapper[tableId]
                #get property index from button index
                propertyIndex = self.index % self.parent.cols
                # get actual value of property eg name, address etc.
                property = indexToPropertyMapper[propertyIndex]
                app = App.get_running_app()

                #ADD CALL TO THE SPECIFIC TABLE HERE

                if(tableId == "CustomerDb"):
                    idIndex = self.index - propertyIndex
                    val = self.parent.parent.data[idIndex]
                    id = val['text']
                    app.updateCustomerDbProperty(id, property, txt)


        self.text = txt

    def isIndexEditable(self, index):

        isEditable = True

        for i in range(len(self.parent.nonSelectable)):
            isEditable = isEditable and (((index - self.parent.nonSelectable[i]) % self.parent.cols) != 0)

        return isEditable


