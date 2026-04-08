# uix/repo_api/github.py

import base64
import json
import requests
from urllib.parse import quote

from .base import BaseRepoService


class GitHubRepoService(BaseRepoService):
    '''
    GitHub implementation of BaseRepoService.
    Uses the GitHub REST API to fetch trees and download files.
    '''

    def __init__(self, base_url: str, token: str, branch: str = "main"):
        '''
        base_url: GitHub API repo URL, e.g.
          https://api.github.com/repos/owner/repo
        token: GitHub PAT
        branch: branch name to read from
        '''
        super().__init__(base_url, token)
        self.branch = branch

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        })

        # Derived URLs
        self.contents_url = f"{base_url}/contents"
        self.trees_url = f"{base_url}/git/trees"

    # ------------------------------------------------------------
    # Tree fetch (GitHub uses /git/trees)
    # ------------------------------------------------------------
    def fetch_tree(self, path="/"):
        '''
        GitHub requires a two-step process:
        1. Get the SHA of the branch
        2. Fetch the full tree recursively
        '''
        # Step 1: get branch SHA
        branch_url = f"{self.base_url}/branches/{self.branch}"
        r = self.session.get(branch_url)
        if r.status_code != 200:
            return None

        sha = r.json()["commit"]["sha"]

        # Step 2: fetch full tree
        tree_url = f"{self.trees_url}/{sha}?recursive=1"
        r = self.session.get(tree_url)
        if r.status_code != 200:
            return None

        tree_json = r.json()
        self.parsed_tree = self._parse_repo_tree(tree_json)
        return self.parsed_tree

    # ------------------------------------------------------------
    # Parsing logic (mirrors Azure DevOps version)
    # ------------------------------------------------------------
    def _parse_repo_tree(self, tree_json):
        files = tree_json.get("tree", [])

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
            if item.get("type") != "tree":
                continue

            path = item.get("path", "")
            parts = path.split("/")

            if len(parts) == 1:
                folder = parts[0].lower()
                if folder not in SPECIAL_FOLDERS:
                    top_folders.add(folder)

        for folder in top_folders:
            result["categories"][folder] = []

        # Classify files
        for item in files:
            if item.get("type") != "blob":
                continue

            path = item.get("path", "")
            lower = path.lower()

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
            if lower.startswith("library/") and lower.endswith(".ps1"):
                filename = path.split("/")[-1]
                item["name"] = filename
                item["category"] = "library"
                result["library"].append(item)
                continue

            # category scripts
            parts = path.split("/")
            if len(parts) == 2:
                folder, filename = parts
                if folder in result["categories"] and filename.endswith(".ps1"):
                    item["name"] = filename
                    item["category"] = folder
                    result["categories"][folder].append(item)
                    continue

            result["other"].append(item)

        return result

    # ------------------------------------------------------------
    # File downloads
    # ------------------------------------------------------------
    def download_file(self, path):
        encoded = quote(path)
        url = f"{self.contents_url}/{encoded}?ref={self.branch}"

        r = self.session.get(url)
        if r.status_code != 200:
            return None

        data = r.json()
        if data.get("encoding") == "base64":
            return base64.b64decode(data["content"]).decode("utf-8")

        return None

    def download_binary(self, path):
        encoded = quote(path)
        url = f"{self.contents_url}/{encoded}?ref={self.branch}"

        r = self.session.get(url)
        if r.status_code != 200:
            return None

        data = r.json()
        if data.get("encoding") == "base64":
            return base64.b64decode(data["content"])

        return None

    # ------------------------------------------------------------
    # GitHub does NOT support log uploads via simple API calls
    # ------------------------------------------------------------
    def upload_log(self, repo_path, content):
        '''
        GitHub commits require a more complex flow (get SHA, create blob, create tree, create commit).
        For SDT v1, we simply do not support log uploads on GitHub.
        '''
        return False
