from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty,StringProperty,ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivyDemos.kivyHomeMenuGit.kivyMenus.texts import textArray, widgetDict
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import WipeTransition
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.spinner import Spinner
from functools import partial
from kivyDemos.kivyHomeMenuGit.kivyMenus import focusWidgets

LabelBase.register('Acme',fn_regular='./fonts/Acme-Regular.ttf')
LabelBase.register('Helsinki',fn_regular='./fonts/helsinki.ttf')
LabelBase.register('Jellee-Roman',fn_regular='./fonts/Jellee-Roman.otf')


class rootWidget(FloatLayout):

    boxes = ObjectProperty(None)
    navBar = ObjectProperty(None)
    # widget which will be focused if 'tab is pressed'
    firstFocusWidget = ObjectProperty(None)

    def getText(self, id):
        return textArray[widgetDict[id]]

class navBar(BoxLayout):
    MenuName = StringProperty('')
    Icon = StringProperty('')
    ColorMenuIcon = ColorProperty([0,0,0,0])
    def getText(self, id):
        return textArray[widgetDict[id]]

class firstCollectionMenu(FloatLayout):

    #widget which will be focused if 'tab is pressed'
    navBar = ObjectProperty(None)
    firstFocusWidget = ObjectProperty(None)

    def getText(self, id):
        return textArray[widgetDict[id]]

class bxL(BoxLayout):
    def getText(self, id):
        return textArray[widgetDict[id]]


class CustomDropDown(DropDown):
    def getText(self, id):
        return textArray[widgetDict[id]]


class HomePage(FloatLayout):
    # widget which will be focused if 'tab is pressed'
    firstFocusWidget = ObjectProperty(None)
    def getText(self,id):
        return textArray[widgetDict[id]]



class DemoApp(App):
    def build(self):


        navbar = Builder.load_file('navBarMain.kv')
        navbar2 = Builder.load_file('navBarSubMenu.kv')
        navbar2.MenuName = 'Collection Menu'
        navbar2.Icon = './images/operationsOutbound.png'
        navbar2.ColorMenuIcon = [0,1,0,0.8]

        root = Builder.load_file('root.kv')
        root.navBar.add_widget(navbar)
        layout1 = Builder.load_file('layout.kv')
        layout2 = Builder.load_file('layout2.kv')

        root.boxes.add_widget(layout1)
        root.boxes.add_widget(layout2)

        home = Builder.load_file('HomePage.kv')
        homeScreen = Screen(name='home')
        homeScreen.add_widget(home)

        mainMenuScreen = Screen(name='mainMenu')
        mainMenuScreen.add_widget(root)

        firstCollectWidget = Builder.load_file('firstCollectionMenu.kv')
        firstCollectWidget.navBar.add_widget(navbar2)
        firstCollectionScreen = Screen(name='firstCollectionMenu')
        firstCollectionScreen.add_widget(firstCollectWidget)

        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(homeScreen)
        sm.add_widget(mainMenuScreen)
        sm.add_widget(firstCollectionScreen)
        Window.bind(on_key_down=self.key_action)
        return sm

    def key_action(self, *args):
        # app.root.
        print("got a key event: " ,args[2],args[3])
        if(args[2] == 53):
            app = App.get_running_app()

            if(app.root.current_screen.children[0].firstFocusWidget is not None):
                app.root.current_screen.children[0].firstFocusWidget.focus = True
            else:
                navbar = app.root.current_screen.children[0].navBar
                if (navbar is not None and navbar.children[0] is not None):
                    numChildren = len(navbar.children[0].children)
                    navbar.children[0].children[numChildren - 1].focus = True

if __name__ == '__main__':
    DemoApp().run()