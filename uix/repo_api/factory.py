# uix/repo_api/factory.py

from uix.repo_api.azure_devops import AzureDevOpsRepoService
from uix.repo_api.github import GitHubRepoService

BACKENDS = {
    "azure_devops": AzureDevOpsRepoService,
    "github": GitHubRepoService,
}

def create_repo_service(type, url, token, branch="main"):
    if not url or not isinstance(url, str):
        raise ValueError("Repository URL is missing or invalid.")

    backend = type.strip().lower()

    if backend not in BACKENDS:
        raise ValueError(
            f"Unsupported backend type '{type}'. "
            f"Valid options are: {', '.join(BACKENDS.keys())}"
        )

    return BACKENDS[backend](url, token, branch)

    
