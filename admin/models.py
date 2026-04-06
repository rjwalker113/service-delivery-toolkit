# admin/models.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class BrandingConfig:
    icon: str
    splash: str

@dataclass
class ConnectionConfig:
    type: str
    script_repo_url: str
    log_repo_url: str
    pat: Optional[str]

@dataclass
class AppConfig:
    org_name: str
    contact: str
    app_name: str
    app_version: str
    require_admin: bool
    branding: BrandingConfig
    connection: ConnectionConfig
