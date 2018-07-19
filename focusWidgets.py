from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.graphics import BorderImage
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
import re

def handleKeyBoardEvents(instance, keycode):
    # on keyboard enter key
    if (keycode[1] == 'enter'):
        #if screen transition is to be made
        if (instance.nextScreen != None):
            app = App.get_running_app()
            if (instance.transition != None):
                app.root.transition = instance.transition
            app.root.current = instance.nextScreen

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

    #if list is open on change of focus close it
    elif (keycode[1] == 'tab'):
        # if drop down is open
        if (instance.attachedTo is not None and instance.attachedTo.get_parent_window()):
            # only do this for if drop down
            if (isinstance(instance.attachedTo, DropDown)):
                instance.attachedTo.dismiss()




class FocusWithColor(FocusBehavior):

    def __init__(self, **kwargs):
        super(FocusWithColor, self).__init__(**kwargs)
        self.background_normal = ''
        self.font_size = 12
        self.markup = True

    def on_focused(self, instance, value, *largs):
        if(value):
            with instance.canvas.before:
                BorderImage(
                    size=(instance.width + 2, instance.height + 2),
                    pos=(instance.x - 1, instance.y - 1),
                    source='./images/borderImage3.jpg',
                    auto_scale='both',
                    group='borderImage')
        else:
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

    def __init__(self, **kwargs):
        super(FocusWithColorNavBar, self).__init__(**kwargs)
        self.background_normal = ''
        self.font_size = 12
        self.markup = True
        self.color = (0.1044, 0.4659, 0.4297, 0.8)
        self.font_name= 'Helsinki'

    def on_focused(self, instance, value, *largs):
        if(value):
            self.color = (1, 1, 1, 0.9)
            with instance.canvas.before:
                Color(rgba=(0.1044,0.4659,0.4297, 0.8))
                Rectangle(pos=instance.pos,size=instance.size,
                          group='borderImage')
        else:
            self.color = (0.1044,0.4659,0.4297, 0.8)

            instance.canvas.before.remove_group('borderImage')


class FocusButton(FocusWithColor, Button):

    nextScreen = StringProperty(None)
    transition = ObjectProperty(None)
    attachedTo = ObjectProperty(None)
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super(FocusButton, self).keyboard_on_key_down(window, keycode,
                                                          text, modifiers):
            if (keycode[1] != 'tab'):
                return True

        handleKeyBoardEvents(self, keycode)

        return True

class FocusButton2(FocusWithColorForTransparentWidgets, Button):

    nextScreen = StringProperty(None)
    transition = ObjectProperty(None)
    attachedTo = ObjectProperty(None)
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super(FocusButton2, self).keyboard_on_key_down(window, keycode,
                                                          text, modifiers):
            if(keycode[1] != 'tab'):
                return True

        handleKeyBoardEvents(self, keycode)

        return True

class FocusButton3(FocusWithColorNavBar, Button):

    nextScreen = StringProperty(None)
    transition = ObjectProperty(None)
    attachedTo = ObjectProperty(None)
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super(FocusButton3, self).keyboard_on_key_down(window, keycode,
                                                          text, modifiers):
            if (keycode[1] != 'tab'):
                return True

        handleKeyBoardEvents(self,keycode)
        return True


#handle rounded button type objects
class ImageButton(FocusButton2,FocusBehavior):

    def on_press(self):
        #todo correct this logic
        if(self.text == 'Discard'):
            with self.canvas.after:
                Color(rgba=(1, 0, 0, 0.3))
                Rectangle(pos=self.pos, size=self.size)

        elif(self.text == 'Save'):
                with self.canvas.after:
                    Color(rgba=(0, 0, 1, 0.3))
                    Rectangle(pos=self.pos, size=self.size)

        elif(self.text == 'Print'):
                with self.canvas.after:
                    Color(rgba=(0, 1, 0, 0.3))
                    Rectangle(pos=self.pos, size=self.size)

    def on_release(self):
        self.canvas.after.clear()





# focus text input focus behaviour for text input
class FocusWithColorForText(FocusBehavior):

    pass



# focus text input to handle tab and focus
class FocusTextInput(FocusWithColorForText, TextInput):
    def __init__(self, **kwargs):
        super(FocusTextInput   , self).__init__(**kwargs)
        self.write_tab = False

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