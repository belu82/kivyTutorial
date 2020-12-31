from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, NoTransition, CardTransition, RiseInTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

lista = []
class DetailsScreen(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        layout = FloatLayout(size=Window.size)
        print(Window.size)
        layout.add_widget(Label(text="Hey"))
        button = Button(text="Back", size_hint=(0.6, 0.2))
        button.pos_hint = {"center_x":0.5,'y': 0.1} #gomb pozícionálása
        button.bind(on_press=self.backToForm)
        layout.add_widget(button)
        self.add_widget(layout)

    def backToForm(self,instance):
        # sm.transition.direction = "left" #az ablakok közti váltások iránya
        # sm.transition = NoTransition()
        print(sm.previous())

        sm.current = "Form"

class PlusScreen(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        layout = FloatLayout(size=Window.size)
        print(Window.size)
        layout.add_widget(Label(text="Plus"))
        button = Button(text="Back", size_hint=(0.6, 0.2))
        button.pos_hint = {"center_x":0.5,'y': 0.1} #gomb pozícionálása
        button.bind(on_press=self.backToForm)
        layout.add_widget(button)
        self.add_widget(layout)

    def backToForm(self,instance):
        print(sm.next())
        sm.current = "Form"

class FormScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout() #azért kell, h úgy nézzen ki mint az eredeti kódo (event)
        layout.orientation = 'vertical'
        layout.opacity = 0.4
        layout.padding = 20
        layout.spacing = 30
        grid = GridLayout()
        grid.spacing = 10
        grid.cols = 2
        nev = Label(text="Nev")
        nev.bind(pos=self.redraw, size=self.redraw)
        with nev.canvas.before:
            Color(0.6, 0.4, 0.8, 1)
            self.bg_rec = Rectangle(size=nev.size, pos=nev.pos)
        grid.add_widget(nev)
        nevmezo = TextInput(multiline=False)
        nevmezo.foreground_color = (0.6, 0.4, 0.8, 1)
        nevmezo.font_size = 20
        layout.nevmezo = nevmezo
        grid.add_widget(nevmezo)
        kor = Label(text="kor")
        kor.bind(pos=self.redrawKor, size=self.redrawKor)
        with kor.canvas.before:
            Color(0.6, 0.4, 0.8, 1)
            self.bg_rec_kor = Rectangle(size=kor.size, pos=kor.pos)
        grid.add_widget(kor)
        layout.add_widget(grid)
        kormezo = TextInput(multiline=False)
        kormezo.foreground_color = (0.6, 0.4, 0.8, 1)
        kormezo.font_size = 30
        layout.kormezo = kormezo
        grid.add_widget(kormezo)

        button = Button(text="Button")
        button.bind(on_press=self.checkFieldsAndPrintData)
        button.background_normal = "Front.jpg"
        button.bind(on_touch_down=self.clearInputs)
        layout.add_widget(button)

        nextButton = Button(text="Next")
        nextButton.bind(on_press=self.showDetails)
        layout.add_widget(nextButton)

        float = FloatLayout(size=(300, 300))
        layout.add_widget(float)

        btn = Button(text="Még 1", size_hint=(.5, .2))
        btn.bind(on_touch_down=self.removeIfDoubleTap)
        btn.pos_hint = {'center_x': 0.5, 'y': 0.2}
        btn2 = Button(text="Még 1", size_hint=(.5, .2))
        btn2.pos_hint = {'center_y': 0.4, 'x': 0.2}
        btn2.bind(on_touch_down=self.removeIfDoubleTap)

        float.add_widget(btn)
        float.add_widget(btn2)
        self.layout = layout #a layout elérése)
        self.add_widget(layout)
        self.bind(on_leave=self.clearOnLeave)     #törli a mezők tartalmát visszetéréskor


    #törli a mezők tartalmát visszetéréskor
    def clearOnLeave(self, instance):
        self.layout.kormezo.text = ""
        self.layout.nevmezo.text = ""

    def showDetails(self, instance):
        sm.transition.direction = "right"
        # sm.current="Details"
        print(sm.screen_names)
        sm.current = sm.next()

    def clearInputs(self, instance, touch):
        if touch.is_double_tap:
            self.layout.kormezo.text = ""
            self.layout.nevmezo.text = ""
            layout = BoxLayout(orientation="vertical")
            layout.add_widget(Label(text="Kitörölve"))
            closeButton = Button(text="Close")
            layout.add_widget(closeButton)
            popup= Popup(title="Demo", content=layout)
            popup.open()
            closeButton.bind(on_press = popup.dismiss)
        else:
            self.checkFieldsAndPrintData(instance)

    def removeIfDoubleTap(self, instance, touch):
        if touch.is_double_tap:
            parent = instance.parent
            parent.remove_widget(instance)

    def redraw(self, instance, value):
        self.bg_rec.size = instance.size
        self.bg_rec.pos = instance.pos

    def redrawKor(self, instance, value):
        self.bg_rec_kor.size = instance.size
        self.bg_rec_kor.pos = instance.pos

    def checkFieldsAndPrintData(self, instance):
        nevmezo = self.layout.nevmezo
        kormezo = self.layout.kormezo
        if len(nevmezo.text) <= 0 or len(kormezo.text) <= 0:
            if not hasattr(self.layout, "errorMessage"):
                self.layout.errorMessage = Label(text="Nem lehet egyik mező sem üres")
                self.add_widget(self.layout.errorMessage, len(self.layout.children) - 4)
        elif not kormezo.text.isdigit():
            if not hasattr(self.layout, "errorMessage"):
                self.layout.errorMessage = Label(text="A kor nem lehet negatív")
                self.add_widget(self.layout.errorMessage, len(self.layout.children) - 4)
            else:
                self.layout.errorMessage.text = " A kor egy szám"
        else:
            self.remove_widget(self.layout.errorMessage)
            lista.append({"text":nevmezo.text, "kor":kormezo.text})
            print("A " + nevmezo.text + "nevű fasz " + kormezo.text)
            print(len(lista))

#screenmanager példányosítása
sm = ScreenManager()

class MyApp(App):
    def build(self):
        formScreen = FormScreen(name="Form")
        sm.add_widget(formScreen)
        detailsScreen = DetailsScreen(name="Details")
        sm.add_widget(detailsScreen)
        plusScreen = PlusScreen(name="Plus")
        sm.add_widget(plusScreen)
        sm.transition = RiseInTransition()
        sm.current = "Form"
        return sm


myapp = MyApp()
myapp.run()

# az eventekig lévő kódok
# class FormScreen(BoxLayout):
#     def __init__(self, **kw):
#         super().__init__(**kw)
#         self.orientation = 'vertical'
#         self.opacity = 0.4
#         self.padding = 20
#         self.spacing = 30
#         grid = GridLayout()
#         grid.spacing = 10
#         grid.cols = 2
#         nev = Label(text="Nev")
#         nev.bind(pos=self.redraw, size=self.redraw)
#         with nev.canvas.before:
#             Color(0.6, 0.4, 0.8, 1)
#             self.bg_rec = Rectangle(size=nev.size, pos=nev.pos)
#         grid.add_widget(nev)
#         nevmezo = TextInput(multiline=False)
#         nevmezo.foreground_color = (0.6, 0.4, 0.8, 1)
#         nevmezo.font_size = 20
#         self.nevmezo = nevmezo
#         grid.add_widget(nevmezo)
#         kor = Label(text="kor")
#         kor.bind(pos=self.redrawKor, size=self.redrawKor)
#         with kor.canvas.before:
#             Color(0.6, 0.4, 0.8, 1)
#             self.bg_rec_kor = Rectangle(size=kor.size, pos=kor.pos)
#         grid.add_widget(kor)
#         self.add_widget(grid)
#         kormezo = TextInput(multiline=False)
#         kormezo.foreground_color = (0.6, 0.4, 0.8, 1)
#         kormezo.font_size = 30
#         self.kormezo = kormezo
#         grid.add_widget(kormezo)
#
#         button = Button(text="Button")
#         button.bind(on_press=self.checkFieldsAndPrintData)
#         button.background_normal = "Front.jpg"
#         button.bind(on_touch_down=self.clearInputs)
#
#
#         self.add_widget(button)
#         float = FloatLayout(size=(300, 300))
#         self.add_widget(float)
#
#         btn = Button(text="Még 1", size_hint=(.5, .2))
#         btn.bind(on_touch_down=self.removeIfDoubleTap)
#         btn.pos_hint = {'center_x': 0.5, 'y': 0.2}
#         btn2 = Button(text="Még 1", size_hint=(.5, .2))
#         btn2.pos_hint = {'center_y': 0.4, 'x': 0.2}
#         btn2.bind(on_touch_down=self.removeIfDoubleTap)
#
#         float.add_widget(btn)
#         float.add_widget(btn2)
#
#     def clearInputs(self, instance, touch):
#         if touch.is_double_tap:
#             self.kormezo.text = ""
#             self.nevmezo.text = ""
#         else:
#             self.checkFieldsAndPrintData(instance)
#
#     def removeIfDoubleTap(self, instance, touch):
#         if touch.is_double_tap:
#             parent = instance.parent
#             parent.remove_widget(instance)
#
#     def redraw(self, instance, value):
#         self.bg_rec.size = instance.size
#         self.bg_rec.pos = instance.pos
#
#     def redrawKor(self, instance, value):
#         self.bg_rec_kor.size = instance.size
#         self.bg_rec_kor.pos = instance.pos
#
#     def checkFieldsAndPrintData(self, instance):
#         nevmezo = self.nevmezo
#         kormezo = self.kormezo
#         if len(nevmezo.text) <= 0 or len(kormezo.text) <= 0:
#             if not hasattr(self, "errorMessage"):
#                 self.errorMessage = Label(text="Nem lehet egyik mező sem üres")
#                 self.add_widget(self.errorMessage, len(self.children) - 4)
#         elif not kormezo.text.isdigit():
#             if not hasattr(self, "errorMessage"):
#                 self.errorMessage = Label(text="A kor nem lehet negatív")
#                 self.add_widget(self.errorMessage, len(self.children) - 4)
#             else:
#                 self.errorMessage.text = " A kor egy szám"
#         else:
#             self.remove_widget(self.errorMessage)
#             print("A " + nevmezo.text + "nevű fasz " + kormezo.text)
