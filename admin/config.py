# admin/config.py
import os
import subprocess
import json
from pathlib import Path


# --- LOAD OPTIONS FROM CONFIG ---
options = json.loads(Path("config.json").read_text())


# --- CONFIG ---

## Organization
organization = options["org_name"]
contact = options["contact"]

## Branding
appicon = options["branding"]["icon"]
splashscreen = options["branding"]["splash"]

## Client details
app_name = options["app_name"]
build_number = options["app_version"]
exe_name = f"{app_name} - v{build_number}"

## Client settings
if options["require_admin"]:
    require_admin=True
else:
    require_admin=False

## Connectivity
repo_type = options["connection"]["type"]
script_repo_url = options["connection"]["script_repo_url"]
log_repo_url = options["connection"]["log_repo_url"]

token = os.getenv("SDT_KEY") or options["connection"]["pat"]
if not token:
    raise ValueError("Access token is missing or invalid.")