# uix/main_screen/main_layout.py

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from uix.main_screen.category_list import CategoryList
from uix.main_screen.script_list import ScriptList
from uix.main_screen.script_details import ScriptDetails


class MainLayout(BoxLayout):
    '''
    Main SDT screen layout:
    - Left: CategoryList
    - Right: ScriptList + ScriptDetals (collapsible)
    '''

    script_repo = ObjectProperty(None)
    log_repo = ObjectProperty(None)
    script_list_data = ObjectProperty(None)
    categories = ObjectProperty(None)
    # tips = ObjectProperty(None)
    # changelog = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        # Left sidebar
        self.category_list = CategoryList(categories=self.categories)
        self.category_list.bind(on_category_selected=self._on_category_selected)

        # Middle content area
        self.script_list = ScriptList()
        self.script_list.bind(on_script_selected=self._on_script_selected)

        # Right details panel (starts collapsed)
        self.script_details = ScriptDetails()
        self.script_details.collapse()
        self.script_details.bind(on_show_full_help=self._on_show_full_help)

        # Add widgets to layout
        self.add_widget(self.category_list)
        self.add_widget(self.script_list)
        self.add_widget(self.script_details)

    # ------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------

    def _on_category_selected(self, instance, category):
        '''
        Called when the user selects a category; Loads that category's scripts.
        '''
        # Load category scripts
        self.script_list.load_scripts_for_category(category, self.script_list_data)

        # Collapse details when switching categories
        self.script_details.collapse()

    def _on_script_selected(self, instance, script):
        '''
        Called when the user selects a script; loads the script details panel.
        '''
        description = script.get("description") or script.get("synopsis")
        self.script_details.load_script(script, description)
    
    def _on_show_full_help(self, instance, script):
        '''
        User clicked 'Additional Details'.
        MainLayout will later open the modal here.
        '''
        # Placeholder — RunConsole or HelpModal will be triggered here.
        pass
