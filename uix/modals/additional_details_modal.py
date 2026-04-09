# uix/modals/additional_details_modal.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.modalview import ModalView


class AdditionalDetailsModal(ModalView):
    '''
    Simple popup window that displays Get-Help <selected script> -Full | Out-String
    '''

    help_text = StringProperty("")

    def __init__(self, script_name="", help_text="", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = False
        self.help_text = help_text

        root = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Header
        header = Label(
            text=f"Additional Details for {script_name}",
            size_hint_y=None,
            height=40,
            bold=True
        )
        root.add_widget(header)

        # Scrollable help text
        scroll = ScrollView()
        self.text_label = Label(
            text=self.help_text,
            size_hint_y=None,
            halign="left",
            valign="top",
            text_size=(self.width * 0.75, None)
        )
        self.text_label.bind(texture_size=self._update_label_height)
        scroll.add_widget(self.text_label)
        root.add_widget(scroll)

        # Buttons
        btn_row = BoxLayout(size_hint_y=None, height=40, spacing=10)

        copy_btn = Button(text="Copy")
        copy_btn.bind(on_release=self._copy_to_clipboard)

        close_btn = Button(text="Close")
        close_btn.bind(on_release=self.dismiss)

        btn_row.add_widget(copy_btn)
        btn_row.add_widget(close_btn)

        root.add_widget(btn_row)

        self.add_widget(root)

    # ------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------

    def _update_label_height(self, instance, size):
        instance.height = size[1]

    def _copy_to_clipboard(self, *args):
        from kivy.core.clipboard import Clipboard
        Clipboard.copy(self.help_text)
