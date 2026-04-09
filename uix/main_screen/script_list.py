# uix/main_screen/script_list.py

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.event import EventDispatcher


class ScriptList(BoxLayout, EventDispatcher):
    scripts = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.register_event_type("on_script_selected")

    def load_scripts_for_category(self, category, script_list_data):
        '''
        script_list_data is the full list of scripts from the repo.
        Filter by category and display.
        '''
        self.clear_widgets()

        if not script_list_data:
            return

        filtered = [s for s in script_list_data if s.get("category") == category]

        for script in filtered:
            btn = Button(text=script.get("name"), size_hint_y=None, height=40)
            btn.bind(on_release=lambda inst, s=script: self.dispatch("on_script_selected", s))
            self.add_widget(btn)

    def on_script_selected(self, script):
        pass
