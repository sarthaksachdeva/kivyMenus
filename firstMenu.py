from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.carousel import Carousel
from kivy.uix.boxlayout import BoxLayout
from texts import textArray, widgetDict
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


class rootWidget(FloatLayout):
    boxes = ObjectProperty(None)
    navBar = ObjectProperty(None)

    def getText(self,id):
        return textArray[widgetDict[id]]

class bxL(BoxLayout):
    def getText(self,id):
        return textArray[widgetDict[id]]


class CustomDropDown(DropDown):
    pass

class DemoApp(App):
    def build(self):
        root = Builder.load_file('root.kv')
        layout1 = Builder.load_file('layout.kv')
        layout2 = Builder.load_file('layout2.kv')
        aboutMenu = Builder.load_file('about.kv')

        mainbutton = Button(text=root.getText('about'))
        mainbutton.bind(on_release=aboutMenu.open)
        aboutMenu.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        # print(len(root.navBar.children))
        root.navBar.add_widget(mainbutton)
        root.boxes.add_widget(layout1)
        root.boxes.add_widget(layout2)
        return root


if __name__ == '__main__':
    DemoApp().run()