from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty, ColorProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from texts import textArray, widgetDict
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import WipeTransition
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.popup import Popup


from CustomerDataUtility import CustomerDataUtility

from functools import partial
import focusWidgets
import recycleViewWidgets

LabelBase.register('Acme', fn_regular='./fonts/Acme-Regular.ttf')
LabelBase.register('Helsinki', fn_regular='./fonts/helsinki.ttf')
LabelBase.register('Jellee-Roman', fn_regular='./fonts/Jellee-Roman.otf')


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
    ColorMenuIcon = ColorProperty([0, 0, 0, 0])

    def getText(self, id):
        return textArray[widgetDict[id]]


class firstCollectionMenu(FloatLayout):
    # widget which will be focused if 'tab is pressed'
    navBar = ObjectProperty(None)
    firstFocusWidget = ObjectProperty(None)

    def getText(self, id):
        return textArray[widgetDict[id]]


class bxL(BoxLayout):
    def getText(self, id):
        return textArray[widgetDict[id]]


class CustomDropDown(DropDown):
    onSide = BooleanProperty(False)

    def open(self, widget):
        super(CustomDropDown, self).open(widget)
        if (self.onSide):
            if (self.attach_to.width + self.width < self._win.width):
                self.x = self.attach_to.width + self.x
            else:
                self.x = self.x - self.attach_to.width
            self.y = self.y + self.attach_to.height

    def getText(self, id):
        return textArray[widgetDict[id]]


class HomePage(FloatLayout):
    # widget which will be focused if 'tab is pressed'
    firstFocusWidget = ObjectProperty(None)

    def getText(self, id):
        return textArray[widgetDict[id]]


class customerDatabase(FloatLayout):
    # widget which will be focused if 'tab is pressed'
    firstFocusWidget = ObjectProperty(None)

    def getText(self, id):
        return textArray[widgetDict[id]]

    data_items = ListProperty([])
    table = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(customerDatabase, self).__init__(**kwargs)
        self.get_users()

    def get_users(self):
        self.data_items = []
        data = [[]]
        app = App.get_running_app()
        customers = app.getAllCustomers()
        for customer in customers:
            y = [customer["id"], customer["name"], customer["localName"], customer["address"], customer["telephone"],
                 customer["telephone"]]
            data.append(y)
        # create data_items
        for row in data:
            for col in row:
                self.data_items.append(col)

    def on_create(self):
        self.get_users()
        super(customerDatabase, self).on_create()


class CustomScreen(Screen):
    def on_pre_enter(self, *args):
        self.dispatch('on_create')


class DemoApp(App, CustomerDataUtility):
    def __init__(self, eventGroup, queue, **kwargs):
        super(DemoApp, self).__init__(**kwargs)
        self.m_event = eventGroup
        self.m_queue = queue

    def sendDataEventToPrinter(self, dbtype, params):
        self.m_queue.put(dbtype)
        self.m_queue.put(params)
        self.m_event.set()
        return True

    def build(self):

        navbar = Builder.load_file('navBarMain.kv')
        navbar2 = Builder.load_file('navBarSubMenu.kv')
        navbar3 = Builder.load_file('navBarSubMenu.kv')
        navbar4 = Builder.load_file('navBarSubMenu.kv')

        navbar2.MenuName = 'Collection Menu'
        navbar3.MenuName = 'Operation Inbound'
        navbar4.MenuName = 'Inbound-Customer'

        navbar2.Icon = './images/operationsOutbound.png'
        navbar3.Icon = './images/union.png'
        navbar4.Icon = './images/reports6.png'

        navbar2.ColorMenuIcon = [0, 1, 0, 0.8]
        navbar3.ColorMenuIcon = [0, 1, 0, 0.8]

        root = Builder.load_file('root.kv')
        root.navBar.add_widget(navbar)
        layout1 = Builder.load_file('layout.kv')
        layout2 = Builder.load_file('layout2.kv')

        root.boxes.add_widget(layout1)
        root.boxes.add_widget(layout2)

        home = Builder.load_file('HomePage.kv')
        homeScreen = CustomScreen(name='home')
        homeScreen.add_widget(home)

        mainMenuScreen = CustomScreen(name='mainMenu')
        mainMenuScreen.add_widget(root)

        firstCollectWidget = Builder.load_file('firstCollectionMenu.kv')
        firstCollectWidget.navBar.add_widget(navbar2)
        firstCollectionScreen = CustomScreen(name='firstCollectionMenu')
        firstCollectionScreen.add_widget(firstCollectWidget)

        CustomerWidget = Builder.load_file('Customer.kv')
        CustomerWidget.navBar.add_widget(navbar3)
        CustomerWidgetScreen = CustomScreen(name='CustomerMenu')
        CustomerWidgetScreen.add_widget(CustomerWidget)

        CustomerDbWidget = Builder.load_file('CustomerDatabaseScreen.kv')
        CustomerDbWidget.navBar.add_widget(navbar4)
        CustomerDbWidgetScreen = CustomScreen(name='CustomerDb')
        CustomerDbWidgetScreen.add_widget(CustomerDbWidget)

        SignUpWidget = Builder.load_file('SignUp.kv')
        SignUpScreen = Screen(name='SignUp')
        SignUpScreen.add_widget(SignUpWidget)

        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(homeScreen)
        sm.add_widget(mainMenuScreen)
        sm.add_widget(firstCollectionScreen)
        sm.add_widget(CustomerWidgetScreen)
        sm.add_widget(CustomerDbWidgetScreen)
        sm.add_widget(SignUpScreen)
        Window.bind(on_key_down=self.key_action)
        return sm

    def key_action(self, *args):
        # app.root.
        print("got a key event: ", args[2], args[3])
        app = App.get_running_app()
        isPopupOpen = False
        for widget in app.root_window.children:
            if isinstance(widget, Popup):
                isPopupOpen = True

        if (args[2] == 53 and (isPopupOpen == False)):
            if (app.root.current_screen.children[0].firstFocusWidget is not None):
                app.root.current_screen.children[0].firstFocusWidget.focus = True
            else:
                navbar = app.root.current_screen.children[0].navBar
                if (navbar is not None and navbar.children[0] is not None):
                    numChildren = len(navbar.children[0].children)
                    navbar.children[0].children[numChildren - 1].focus = True



