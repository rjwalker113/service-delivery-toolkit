# uix/main_screen/script_details.py

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class ScriptDetails(BoxLayout, EventDispatcher):
    '''
    Collapsible right-side panel showing script description
    and an 'Additional Details' button.
    '''

    script = ObjectProperty(None)
    description = StringProperty("")
    collapsed = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.register_event_type("on_show_full_help")

        # Header
        self.header = BoxLayout(size_hint_y=None, height=40)
        self.script_name_label = Label(text="", bold=True)
        self.collapse_btn = Button(text="▼", size_hint_x=None, width=40)
        self.collapse_btn.bind(on_release=self.toggle_collapse)

        self.header.add_widget(self.script_name_label)
        self.header.add_widget(self.collapse_btn)
        self.add_widget(self.header)

        # Description area
        self.scroll = ScrollView()
        self.desc_label = Label(
            text="",
            markup=True,
            size_hint_y=None,
            halign="left",
            valign="top"
        )
        self.desc_label.bind(texture_size=self._update_label_height)
        self.scroll.add_widget(self.desc_label)
        self.add_widget(self.scroll)

        # Additional Details button
        self.details_btn = Button(
            text="Additional Details",
            size_hint_y=None,
            height=40
        )
        self.details_btn.bind(on_release=self._on_details_clicked)
        self.add_widget(self.details_btn)

    # ------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------

    def load_script(self, script, description):
        self.script = script
        self.script_name_label.text = script.get("name", "")
        self.description = description or "No description provided."
        self.desc_label.text = self.description
        self.expand()

    # ------------------------------------------------------------
    # Collapsing behavior
    # ------------------------------------------------------------

    def toggle_collapse(self, *args):
        if self.collapsed:
            self.expand()
        else:
            self.collapse()

    def collapse(self):
        self.collapsed = True
        self.scroll.height = 0
        self.details_btn.height = 0
        self.collapse_btn.text = "▲"

    def expand(self):
        self.collapsed = False
        self.scroll.height = None
        self.details_btn.height = 40
        self.collapse_btn.text = "▼"

    # ------------------------------------------------------------
    # Additional Details
    # ------------------------------------------------------------

    def _on_details_clicked(self, *args):
        self.dispatch("on_show_full_help", self.script)

    def on_show_full_help(self, script):
        pass

    # ------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------

    def _update_label_height(self, instance, size):
        instance.height = size[1]
