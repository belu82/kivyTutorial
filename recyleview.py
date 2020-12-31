from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView


class EmberViewmer(RecycleView):
    def __init__(self):
        super(EmberViewmer, self).__init__()

class RVItem(Button):
    def get_data_index(self):
        return self.parent.get_view_index_at(self.center)

    def on_press(self):
        print(self.get_data_index())

Builder.load.string(...

...)