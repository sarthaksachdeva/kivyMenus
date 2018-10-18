from distutils.command.install import install

from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.graphics import BorderImage
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import NoTransition
from kivy.app import App
import re

#todo refactor this function
def handleKeyBoardEvents(instance, keycode):
    # on keyboard enter key
    if (keycode[1] == 'enter'):
        #if screen transition is to be made
        if (instance.nextScreen != None):
            #check if a call back is to be made
            if(instance.functionCall is not None):
                ret = instance.functionCall()
            else:
                ret = True

            if(ret):
                #check if widget is a part of drop down. Handles only if it's a part of drop down list and not sub menu.
                if ((instance.parent is not None) and (instance.parent.parent is not None) and isinstance(
                        instance.parent.parent, DropDown)):
                    instance.parent.parent.dismiss()
                app = App.get_running_app()
                transition = NoTransition()
                if (instance.transition != None):
                    transition = instance.transition
                instance.focus = False
                app.switchScreen(instance.nextScreen, transition=transition)

        #if a drop down is attached open or close it
        elif(instance.attachedTo is not None):
            #only do this for if drop down
            if(isinstance(instance.attachedTo, DropDown)):
                #if drop down is open
                if (instance.attachedTo.get_parent_window()):
                    instance.attachedTo.dismiss()
                else:
                    instance.attachedTo.open(instance)

        # if it's a part of drop down list

        elif(isinstance(instance.parent.parent,DropDown)):
            #if it's a sub menu dismiss it's parent menu before selecting
            if((instance.parent.parent.attach_to.parent is not None) and
                   (isinstance(instance.parent.parent.attach_to.parent,GridLayout))):
                if((instance.parent.parent.attach_to.parent.parent is not None) and
                 (isinstance(instance.parent.parent.attach_to.parent.parent, DropDown))):
                    instance.parent.parent.attach_to.parent.parent.dismiss()

            instance.parent.parent.select(instance.text)

    # on keyboard down key
    elif(keycode[1] == 'down'):
        if(instance.attachedTo is not None and instance.attachedTo.get_parent_window()):
            # only do this for if drop down
            if (isinstance(instance.attachedTo, DropDown)):
                child = instance.attachedTo.children[0]
                numChilds = len((child.children))
                nextFocus = child.children[numChilds - 1]
                instance.focus = False
                nextFocus.focus = True
    # on keyboard down key
    elif (keycode[1] == 'up'):
        if(isinstance(instance.parent.parent, DropDown)):
            instance.focus = False
            instance.parent.parent.attach_to.focus = True
        #in case sub menu is still open
        if(instance.attachedTo is not None):
            if (instance.attachedTo.get_parent_window()):
                instance.attachedTo.dismiss()
    #if list is open on change of focus close it
    elif (keycode[1] == 'tab'):
        # if drop down is open
        if (instance.attachedTo != None):
            if(instance.attachedTo.get_parent_window()):
                # only do this for if drop down
                if (isinstance(instance.attachedTo, DropDown)):
                    instance.attachedTo.dismiss()




class FocusWithColor(FocusBehavior):


    attachedGif = ObjectProperty(None)
    animDelay = NumericProperty(-1)
    def __init__(self, **kwargs):
        super(FocusWithColor, self).__init__(**kwargs)
        self.background_normal = ''
        self.font_size = 12
        self.markup = True
        self.background_disabled_normal = "./images/disabledButton5.jpg"

    def on_focused(self, instance, value, *largs):
        if(value):
            if(self.attachedGif is not None and self.attachedGif._coreimage is not None):
                self.attachedGif.anim_loop = 1
                self.attachedGif.anim_delay = self.animDelay
                self.attachedGif._coreimage.anim_reset(True)

            with instance.canvas.before:
                BorderImage(
                    size=(instance.width + 2, instance.height + 2),
                    pos=(instance.x - 1, instance.y - 1),
                    source='./images/borderImage3.jpg',
                    auto_scale='both',
                    group='borderImage')

        else:
            if (self.attachedGif is not None and self.attachedGif._coreimage is not None):
                self.attachedGif._coreimage._anim_index = 0
                self.attachedGif._coreimage.anim_reset(True)
                self.attachedGif._coreimage.anim_reset(False)
            instance.canvas.before.remove_group('borderImage')

# to create dark effect on focus
class FocusWithColorForTransparentWidgets(FocusBehavior):

    def __init__(self, **kwargs):
        super(FocusWithColorForTransparentWidgets   , self).__init__(**kwargs)
        self.background_normal = ''
        self.font_size = 12
        self.markup = True

    def on_focused(self, instance, value, *largs):
        if(value):
            with instance.canvas.before:
                Color(rgba=(0,0,0,0.35))
                Rectangle(pos=instance.pos,size=instance.size,
                          group='borderImage')
        else:
            instance.canvas.before.remove_group('borderImage')

class FocusWithColorNavBar(FocusBehavior):
    attachedGif = ObjectProperty(None)
    animDelay = NumericProperty(-1)

    def __init__(self, **kwargs):
        super(FocusWithColorNavBar, self).__init__(**kwargs)
        self.background_normal = ''
        self.font_size = 12
        self.markup = True
        self.color = (0.1044, 0.4659, 0.4297, 0.8)
        self.font_name= 'Helsinki'

    def on_focused(self, instance, value, *largs):
        if(value):
            if(self.attachedGif is not None and self.attachedGif._coreimage is not None):
                self.attachedGif.anim_loop = 1
                self.attachedGif.anim_delay = self.animDelay
                self.attachedGif._coreimage.anim_reset(True)

            self.color = (1, 1, 1, 0.9)
            with instance.canvas.before:
                Color(rgba=(0.1044,0.4659,0.4297, 0.8))
                Rectangle(pos=instance.pos,size=instance.size,
                          group='borderImage')
        else:
            if (self.attachedGif is not None and self.attachedGif._coreimage is not None):
                self.attachedGif._coreimage._anim_index = 0
                self.attachedGif._coreimage.anim_reset(True)
                self.attachedGif._coreimage.anim_reset(False)
            self.color = (0.1044,0.4659,0.4297, 0.8)

            instance.canvas.before.remove_group('borderImage')


class FocusButton(FocusWithColor, Button):

    nextScreen = StringProperty(None)
    transition = ObjectProperty(None)
    attachedTo = ObjectProperty(None)
    functionCall = ObjectProperty(None)
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super(FocusButton, self).keyboard_on_key_down(window, keycode,
                                                          text, modifiers):
            if (keycode[1] != 'tab'):
                return True

        handleKeyBoardEvents(self, keycode)

        return True

    #TO propogate event to drop downs as well
    def on_create(self):
        if(self.attachedTo is not None):
            self.attachedTo.dispatch('on_create')

class FocusButton2(FocusWithColorForTransparentWidgets, Button):

    nextScreen = StringProperty(None)
    transition = ObjectProperty(None)
    attachedTo = ObjectProperty(None)
    functionCall = ObjectProperty(None)
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super(FocusButton2, self).keyboard_on_key_down(window, keycode,
                                                          text, modifiers):
            if(keycode[1] != 'tab'):
                return True

        handleKeyBoardEvents(self, keycode)

        return True

    #TO propogate event to drop downs as well
    def on_create(self):
        if(self.attachedTo is not None):
            self.attachedTo.dispatch('on_create')

class FocusButton3(FocusWithColorNavBar, Button):

    nextScreen = StringProperty(None)
    transition = ObjectProperty(None)
    attachedTo = ObjectProperty(None)
    functionCall = ObjectProperty(None)
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super(FocusButton3, self).keyboard_on_key_down(window, keycode,
                                                          text, modifiers):
            if (keycode[1] != 'tab'):
                return True

        handleKeyBoardEvents(self,keycode)
        return True


    #TO propogate event to drop downs as well
    def on_create(self):
        if(self.attachedTo is not None):
            self.attachedTo.dispatch('on_create')

    def on_disabled(self, instance, value):
        if (value):
            with instance.canvas.before:
                Color(rgba=(0.6, 0.6, 0.6, 0.6))
                Rectangle(pos=instance.pos, size=instance.size,
                          group='disabledButton')
        else:
            instance.canvas.before.remove_group('disabledButton')



class FocusButton4(FocusWithColorNavBar, Button):
    def __init__(self, **kwargs):
        super(FocusButton4, self).__init__(**kwargs)
        #TODO temporary fix for text wrapping
        self.size_hint_y = None
        self.text_size= self.width, None
        self.height= self.texture_size[1]
    def on_focused(self, instance, value, *largs):
        super(FocusButton4, self).on_focused(instance, value, *largs)
        if(value):
            self.color = (0, 0, 0, 0.9)

# focus text input focus behaviour for text input
class FocusWithColorForText(FocusBehavior):

    pass



# focus text input to handle tab and focus
class FocusTextInput(FocusWithColorForText, TextInput):
    def __init__(self, **kwargs):
        #custom event raised on edit text
        self.register_event_type('on_text_edit')
        self.bind(text=self.textCallback)
        super(FocusTextInput   , self).__init__(**kwargs)
        self.write_tab = False
    def on_text_edit(self):
        pass

    def textCallback(self, instance, value):
        self.dispatch('on_text_edit')

#only numbers and decimals text inp8ut
class FloatTextInput(FocusTextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatTextInput, self).insert_text(s, from_undo=from_undo)