# admin/config.py
import os
import json
from pathlib import Path
from .models import AppConfig, BrandingConfig, ConnectionConfig

def load_config():
    raw = json.loads(Path("config.json").read_text())

    branding = BrandingConfig(**raw["branding"])
    connection = ConnectionConfig(**raw["connection"])

    config = AppConfig(
        org_name=raw["org_name"],
        contact=raw["contact"],
        app_name=raw["app_name"],
        app_version=raw["app_version"],
        require_admin=raw["require_admin"],
        branding=branding,
        connection=connection
    )

    # Dev override
    config.connection.pat = os.getenv("SDT_KEY") or config.connection.pat

    return config

config = load_config()


# # --- LOAD OPTIONS FROM CONFIG ---
# options = json.loads(Path("config.json").read_text())


# # --- CONFIG ---

# ## Organization
# organization = options["org_name"]
# contact = options["contact"]

# ## Branding
# appicon = options["branding"]["icon"]
# splashscreen = options["branding"]["splash"]

# ## Client details
# app_name = options["app_name"]
# build_number = options["app_version"]
# exe_name = f"{app_name} - v{build_number}"

# ## Client settings
# require_admin = bool(options["require_admin"])



# ## Connectivity
# repo_type = options["connection"]["type"]
# script_repo_url = options["connection"]["script_repo_url"]
# log_repo_url = options["connection"]["log_repo_url"]

# token = os.getenv("SDT_KEY") or options["connection"]["pat"]
# if not token:
#     raise ValueError("Access token is missing or invalid.")