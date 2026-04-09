# uix/run_console/run_console.py

from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock


class RunConsole(ModalView):
    '''
    Modal window that shows branding and live script output.
    '''

    script = ObjectProperty(None)
    output_text = StringProperty("")

    def __init__(self, script=None, **kwargs):
        super().__init__(**kwargs)
        self.script = script
        self.size_hint = (0.9, 0.9)
        self.auto_dismiss = False

        root = BoxLayout(orientation="horizontal", spacing=10, padding=10)

        # ------------------------------------------------------------
        # Left Branding Panel
        # ------------------------------------------------------------
        branding = BoxLayout(orientation="vertical", size_hint_x=0.33, spacing=10)

        branding.add_widget(Label(
            text="[b]SDT[/b]",
            markup=True,
            font_size=24,
            size_hint_y=None,
            height=40
        ))

        branding.add_widget(Label(
            text=f"Script: {script.get('name')}",
            size_hint_y=None,
            height=30
        ))

        branding.add_widget(Label(
            text=f"Category: {script.get('category')}",
            size_hint_y=None,
            height=30
        ))

        # Animated indicator (simple pulsing text)
        self.running_label = Label(
            text="[i]Running...[/i]",
            markup=True,
            size_hint_y=None,
            height=30
        )
        branding.add_widget(self.running_label)

        root.add_widget(branding)

        # ------------------------------------------------------------
        # Right Output Console
        # ------------------------------------------------------------
        console_area = BoxLayout(orientation="vertical")

        scroll = ScrollView()
        self.output_label = Label(
            text="",
            font_name="RobotoMono",
            size_hint_y=None,
            halign="left",
            valign="top",
            text_size=(0, None)
        )
        self.output_label.bind(texture_size=self._update_label_height)
        scroll.add_widget(self.output_label)

        console_area.add_widget(scroll)

        # Buttons
        btn_row = BoxLayout(size_hint_y=None, height=40, spacing=10)

        copy_btn = Button(text="Copy Output")
        copy_btn.bind(on_release=self._copy_output)

        close_btn = Button(text="Close")
        close_btn.bind(on_release=self.dismiss)

        btn_row.add_widget(copy_btn)
        btn_row.add_widget(close_btn)

        console_area.add_widget(btn_row)

        root.add_widget(console_area)

        self.add_widget(root)

    # ------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------

    def append_output(self, text):
        '''Append new output to the console.'''
        self.output_text += text + "\n"
        self.output_label.text = self.output_text

        # Auto-scroll
        Clock.schedule_once(lambda dt: self._scroll_to_bottom())

    # ------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------

    def _update_label_height(self, instance, size):
        instance.height = size[1]

    def _scroll_to_bottom(self):
        try:
            scroll = self.output_label.parent
            scroll.scroll_y = 0
        except:
            pass

    def _copy_output(self, *args):
        from kivy.core.clipboard import Clipboard
        Clipboard.copy(self.output_text)
