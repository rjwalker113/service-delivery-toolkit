# uix/main_screen/main_layout.py

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from uix.main_screen.category_list import CategoryList
from uix.main_screen.script_list import ScriptList


class MainLayout(BoxLayout):
    '''
    Main SDT screen layout:
    - Left: CategoryList
    - Right: ScriptList
    '''

    script_repo = ObjectProperty(None)
    log_repo = ObjectProperty(None)
    script_list_data = ObjectProperty(None)
    categories = ObjectProperty(None)
    descriptions = ObjectProperty(None)
    tips = ObjectProperty(None)
    changelog = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        # Left sidebar
        self.category_list = CategoryList(categories=self.categories)
        self.category_list.bind(on_category_selected=self._on_category_selected)

        # Right content area
        self.script_list = ScriptList()
        self.script_list.bind(on_script_selected=self._on_script_selected)

        # Add widgets to layout
        self.add_widget(self.category_list)
        self.add_widget(self.script_list)

    # ------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------

    def _on_category_selected(self, instance, category):
        '''
        Called when the user selects a category.
        For now, just forward the event to ScriptList.
        '''
        self.script_list.load_scripts_for_category(category, self.script_list_data)

    def _on_script_selected(self, instance, script):
        '''
        Called when the user selects a script.
        Later this will open ScriptDetails or RunConsole.
        '''
        pass  # placeholder
