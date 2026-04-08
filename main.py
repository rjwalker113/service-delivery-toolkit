# main.py

import os, sys
from kivy.resources import resource_add_path

if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'minimum_width', '900')
Config.set('graphics', 'minimum_height', '600')

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from uix.utils import resource_path, register_all_fonts, cleanup
from uix.repo_api.factory import create_repo_service
from uix.main_screen.layout import MainLayout
from uix.views.announcements import Announcements
from uix.custom_widgets.flex_modal import FlexModal

from admin.config import config

register_all_fonts("fonts")

class SDT_App(App):
    def build(self):
        self.title = f"{config.app_name} v{config.app_version}"
        self.icon = resource_path(config.branding.icon)
        Window.icon = resource_path(config.branding.icon)
        Window.clearcolor = (1, 1, 1, 1)

        # Backend‑agnostic repo services
        self.script_repo = create_repo_service(
            config.connection.type,
            config.connection.script_repo_url,
            config.connection.pat,
            config.connection.branch
        )

        self.log_repo = create_repo_service(
            config.connection.type,
            config.connection.log_repo_url,
            config.connection.pat,
            config.connection.branch
        )

        # Preload metadata
        self.script_repo.fetch_tree("/")
        self.categories = self.script_repo.get_categories()
        self.script_list = self.script_repo.get_all_scripts()
        self.announcements = self.script_repo.get_announcements()
        self.changelog = self.script_repo.get_changelog()
        self.descriptions = self.script_repo.get_descriptions()
        self.tips = self.script_repo.get_tips()

        # Build UI
        self.screen_manager = ScreenManager()
        main_screen = Screen(name="tools")
        self.main_layout = MainLayout(
            script_repo=self.script_repo,
            log_repo=self.log_repo,
            script_list=self.script_list,
            changelog=self.changelog,
            categories=self.categories,
            descriptions=self.descriptions,
            tips=self.tips
        )
        main_screen.add_widget(self.main_layout)
        self.screen_manager.add_widget(main_screen)

        return self.screen_manager

    def on_start(self):
        try:
            import pyi_splash
            pyi_splash.close()
        except ImportError:
            pass

        # TODO: new update system
        self._show_announcements()

    def _show_announcements(self):
        modal = FlexModal(
            "LATEST UPDATES",
            Announcements(self.announcements),
            buttons=[("OK", None)]
        )
        modal.open()

    def on_stop(self):
        cleanup("m_file.psm1")
        return super().on_stop()

if __name__ == '__main__':
    SDT_App().run()