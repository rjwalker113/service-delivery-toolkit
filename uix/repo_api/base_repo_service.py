from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import tempfile
import os
from utils.parse_help_block import parse_help_block

# import urllib3

@dataclass
class RepoItem:
    '''Represents a file or folder in a repository tree.'''
    path: str
    name: str
    is_folder: bool
    metadata: Dict[str, Any]

class BaseRepoService:
    '''
    Abstract base class for repository backends.
    Override in specific backend classes as needed.
    '''

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self.parsed_tree = None
        self.cached_module_path = None

    # ------------------------------------------------------------
    # Abstract methods (must be implemented by each backend)
    # ------------------------------------------------------------

    def fetch_tree(self, path: str = "/") -> Dict[str, Any]:
        '''Fetch and parse the repository tree starting at `path`.'''
        raise NotImplementedError

    def download_file(self, path: str) -> Optional[str]:
        '''Download a text file from the repository.'''
        raise NotImplementedError

    def download_binary(self, path: str) -> Optional[bytes]:
        '''Download a binary file from the repository.'''
        raise NotImplementedError
    
    # ------------------------------------------------------------
    # Optional backend features
    # ------------------------------------------------------------

    def upload_log(self, repo_path: str, content: str) -> bool:
        '''Upload a log file. Not all backends support this.'''
        raise NotImplementedError

    # ------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------

    def get_categories(self) -> List[str]:
        if not self.parsed_tree:
            return []
        return list(self.parsed_tree.get("categories", {}).keys())

    def get_scripts_for_category(self, category: str) -> List[Dict[str, Any]]:
        if not self.parsed_tree:
            return []
        return self.parsed_tree.get("categories", {}).get(category, [])

    def get_all_scripts(self):
        '''
        Returns a list of script metadata dictionaries.
        Each dictionary includes:
        - name
        - category
        - path
        - description (from .DESCRIPTION)
        - synopsis (from .SYNOPSIS)
        '''
        scripts = []

        for file in self.tree:
            if not file["path"].lower().endswith(".ps1"):
                continue

            script_path = file["path"]
            script_name = script_path.split("/")[-1]
            category = script_path.split("/")[0]

            # Download script text
            script_text = self.download_file(script_path)
            if not script_text:
                continue

            # Parse help block
            help_data = parse_help_block(script_text)

            scripts.append({
                "name": script_name,
                "category": category,
                "path": script_path,
                "description": help_data.get("description"),
                "synopsis": help_data.get("synopsis")
            })

        return scripts

    def get_module_path(self) -> Optional[str]:
        '''Download and cache the PowerShell module used by scripts.'''
        if self.cached_module_path:
            return self.cached_module_path

        module_text = self.download_file("/library/m_file.psm1")
        if not module_text:
            return None

        temp_dir = tempfile.gettempdir()
        module_path = os.path.join(temp_dir, "m_file.psm1")

        with open(module_path, "w", encoding="utf-8") as f:
            f.write(module_text)

        self.cached_module_path = module_path
        return module_path