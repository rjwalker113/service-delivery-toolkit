# uix/repo_api/azure_devops.py

import os
import json
import time
import requests
import urllib3
from urllib.parse import quote

from kivy.clock import Clock  # You may remove this if you remove UI callbacks
from .base_repo_service import BaseRepoService
from uix.repo_api.session_setup import SystemTrustAdapter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AzureDevOpsRepoService(BaseRepoService):
    '''
    Azure DevOps implementation of BaseRepoService.
    Handles:
      - Tree fetch
      - File downloads
      - Binary downloads
      - Optional log uploads
    '''

    def __init__(self, base_url: str, token: str, branch: str = "main"):
        '''
        base_url: full repo URL, e.g.
          https://dev.azure.com/org/project/_apis/git/repositories/repo
        token: PAT
        branch: branch name to read from
        '''
        super().__init__(base_url, token)
        self.branch = branch

        # Session setup
        self.session = requests.Session()
        self.session.auth = ("", token)
        self.session.verify = True
        self.session.mount("https://", SystemTrustAdapter())

        # Derived URLs
        self.items_url = f"{base_url}/items"
        self.refs_url = f"{base_url}/refs"
        self.pushes_url = f"{base_url}/pushes"

    # ------------------------------------------------------------
    # Internal retry wrapper
    # ------------------------------------------------------------
    def _retry(self, func, *args, **kwargs):
        for attempt in range(3):
            try:
                response = func(*args, **kwargs)

                if response.status_code in (200, 201):
                    return response

                if response.status_code == 503:
                    time.sleep(attempt + 1)
                    continue

                if response.status_code in (401, 403):
                    # In SDT, we raise instead of showing UI popups
                    raise PermissionError("Azure DevOps token expired or invalid.")

                return None

            except requests.exceptions.SSLError:
                raise PermissionError("SSL error — token may be invalid.")

            except Exception:
                raise

        return None

    # ------------------------------------------------------------
    # Tree fetch
    # ------------------------------------------------------------
    def fetch_tree(self, path="/"):
        url = (
            f"{self.items_url}"
            f"?scopePath={path}"
            f"&versionDescriptor.version={self.branch}"
            f"&recursionLevel=Full"
            f"&includeContentMetadata=true"
            f"&api-version=7.1"
        )

        r = self._retry(self.session.get, url)
        if not r:
            return None

        tree_json = r.json()
        self.parsed_tree = self._parse_repo_tree(tree_json)
        return self.parsed_tree

    # ------------------------------------------------------------
    # Parsing logic
    # ------------------------------------------------------------
    def _parse_repo_tree(self, tree_json):
        files = tree_json.get("value", [])

        result = {
            "categories": {},
            "library": [],
            "announcements": None,
            "changelog": None,
            "descriptions": None,
            "other": []
        }

        SPECIAL_FOLDERS = {"library", "binaries", "releases", "_inactive"}

        # Identify top-level folders
        top_folders = set()
        for item in files:
            if not item.get("isFolder", False):
                continue

            path = item.get("path", "")
            parts = path.strip("/").split("/")

            if len(parts) == 1:
                folder = parts[0].lower()
                if folder not in SPECIAL_FOLDERS:
                    top_folders.add(folder)

        for folder in top_folders:
            result["categories"][folder] = []

        # Classify files
        for item in files:
            path = item.get("path", "")
            lower = path.lower()

            if item.get("isFolder", False):
                continue

            # announcements
            if lower.endswith("announcements.md"):
                result["announcements"] = item
                continue

            # changelog
            if lower.endswith("changelog.md"):
                result["changelog"] = item
                continue

            # descriptions
            if lower.endswith("descriptions.json"):
                result["descriptions"] = item
                continue

            # library scripts
            if lower.startswith("/library/") and lower.endswith(".ps1"):
                filename = os.path.basename(path)
                item["name"] = filename
                item["category"] = "library"
                result["library"].append(item)
                continue

            # category scripts
            parts = path.strip("/").split("/")
            if len(parts) == 2:
                folder, filename = parts
                if folder in result["categories"] and filename.endswith(".ps1"):
                    item["name"] = filename
                    item["category"] = folder
                    result["categories"][folder].append(item)
                    continue

            # everything else
            result["other"].append(item)

        return result

    # ------------------------------------------------------------
    # File downloads
    # ------------------------------------------------------------
    def download_file(self, path):
        encoded = quote(path, safe="/")
        url = (
            f"{self.items_url}"
            f"?path={encoded}"
            f"&versionDescriptor.version={self.branch}"
            f"&versionDescriptor.versionType=branch"
            f"&api-version=7.1"
        )
        r = self._retry(self.session.get, url)
        return r.text if r else None

    def download_binary(self, path):
        encoded = quote(path, safe="/")
        url = (
            f"{self.items_url}"
            f"?path={encoded}"
            f"&versionDescriptor.version={self.branch}"
            f"&versionDescriptor.versionType=branch"
            f"&includeContent=true"
            f"&api-version=7.1"
        )
        r = self._retry(self.session.get, url)
        return r.content if r else None

    # ------------------------------------------------------------
    # Optional: log upload (Azure DevOps supported)
    # ------------------------------------------------------------
    def upload_log(self, repo_path, content):
        '''
        Uploads a text file to the repo via a push.
        '''
        branch = self.branch
        old_id = self._get_branch_object_id(branch)

        payload = {
            "refUpdates": [
                {
                    "name": f"refs/heads/{branch}",
                    "oldObjectId": old_id
                }
            ],
            "commits": [
                {
                    "comment": "SDT log upload",
                    "changes": [
                        {
                            "changeType": "add",
                            "item": {"path": repo_path},
                            "newContent": {
                                "content": content,
                                "contentType": "rawtext"
                            }
                        }
                    ]
                }
            ]
        }

        headers = {"Content-Type": "application/json"}

        r = self._retry(
            self.session.post,
            self.pushes_url + "?api-version=7.1",
            headers=headers,
            data=json.dumps(payload)
        )

        return r is not None and r.status_code in (200, 201)

    # ------------------------------------------------------------
    # Branch helper
    # ------------------------------------------------------------
    def _get_branch_object_id(self, branch_name):
        url = f"{self.refs_url}?filter=heads/{branch_name}&api-version=7.1"
        r = self._retry(self.session.get, url)
        if not r:
            return None

        data = r.json()
        refs = data.get("value", [])

        for ref in refs:
            if ref.get("name") == f"refs/heads/{branch_name}":
                return ref.get("objectId")

        if refs:
            return refs[0].get("objectId")

        return None
