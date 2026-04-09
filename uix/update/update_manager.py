# uix/update/update_manager.py

import json
import os
import tempfile
from packaging import version

from kivy.clock import Clock
from uix.custom_widgets.flex_modal import FlexModal
from uix.views.announcements import Announcements


class UpdateManager:
    '''
    Backend-agnostic update manager for SDT.
    Checks update.json, compares versions, downloads new EXE, and launches it.
    '''

    MANIFEST_PATH = "/releases/update.json"

    def __init__(self, repo_service, config):
        self.repo = repo_service
        self.config = config

    # ------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------
    def check_for_updates(self):
        '''
        Called by main.py on startup.
        Fetches update.json and compares versions.
        '''
        manifest = self._fetch_manifest()
        if not manifest:
            return  # No update.json or repo unreachable

        latest = manifest.get("latest_version")
        download_path = manifest.get("download_path")
        notes_path = manifest.get("release_notes")

        if not latest or not download_path:
            return  # Malformed manifest

        if self._is_newer_version(latest):
            self._prompt_update(latest, download_path, notes_path)
        else:
            # No update → show announcements instead
            self._show_announcements()

    # ------------------------------------------------------------
    # Manifest handling
    # ------------------------------------------------------------
    def _fetch_manifest(self):
        text = self.repo.download_file(self.MANIFEST_PATH)
        if not text:
            return None

        try:
            return json.loads(text)
        except Exception:
            return None

    def _is_newer_version(self, latest):
        try:
            return version.parse(latest) > version.parse(self.config.app_version)
        except Exception:
            return False

    # ------------------------------------------------------------
    # UI prompts
    # ------------------------------------------------------------
    def _prompt_update(self, latest, download_path, notes_path):
        '''
        Show modal asking user if they want to update.
        '''
        body = (
            f"A new version of {self.config.app_name} is available.\n\n"
            f"Current version: {self.config.app_version}\n"
            f"Latest version: {latest}\n\n"
            "Would you like to update now?"
        )

        modal = FlexModal(
            title="Update Available",
            content=body,
            buttons=[
                ("Update Now", lambda *_: self._begin_update(download_path)),
                ("Later", lambda *_: self._show_announcements())
            ]
        )
        modal.open()

    def _show_announcements(self):
        '''
        Fallback if no update or user declines.
        '''
        announcements = self.repo.get_announcements()
        if not announcements:
            return

        modal = FlexModal(
            "LATEST UPDATES",
            Announcements(announcements),
            buttons=[("OK", None)]
        )
        modal.open()

    # ------------------------------------------------------------
    # Update process
    # ------------------------------------------------------------
    def _begin_update(self, download_path):
        '''
        Downloads the new EXE and launches it.
        '''
        binary = self.repo.download_binary(download_path)
        if not binary:
            self._show_error("Failed to download update.")
            return

        exe_path = self._save_update_file(binary)
        if not exe_path:
            self._show_error("Failed to save update file.")
            return

        self._launch_update(exe_path)

    def _save_update_file(self, binary):
        '''
        Saves the downloaded EXE to a temp directory.
        '''
        try:
            target = os.path.join(tempfile.gettempdir(), "SDT-Update.exe")
            with open(target, "wb") as f:
                f.write(binary)
            return target
        except Exception:
            return None

    def _launch_update(self, exe_path):
        '''
        Launches the new EXE and closes the current app.
        '''
        try:
            os.startfile(exe_path)
        except Exception:
            self._show_error("Failed to launch update.")
            return

        # Close the running app
        from kivy.app import App
        App.get_running_app().stop()

    # ------------------------------------------------------------
    # Error handling
    # ------------------------------------------------------------
    def _show_error(self, message):
        modal = FlexModal(
            "Update Error",
            message,
            buttons=[("OK", None)]
        )
        modal.open()
