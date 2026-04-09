# uix/main_screen/category_list.py

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.event import EventDispatcher


class CategoryList(BoxLayout, EventDispatcher):
    categories = ListProperty([])

    def __init__(self, categories=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.register_event_type("on_category_selected")

        if categories:
            self.load_categories(categories)

    def load_categories(self, categories):
        self.clear_widgets()
        for cat in categories:
            btn = Button(text=cat, size_hint_y=None, height=40)
            btn.bind(on_release=lambda inst, c=cat: self.dispatch("on_category_selected", c))
            self.add_widget(btn)

    def on_category_selected(self, category):
        pass
