from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import tempfile
import os
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

    def get_all_scripts(self) -> List[Dict[str, Any]]:
        if not self.parsed_tree:
            return []
        categories = self.parsed_tree.get("categories", {})
        return [script for scripts in categories.values() for script in scripts]

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