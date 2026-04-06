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
splashscreen = options["branding"]["splashscreen"]

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






# # --- EXPORT CURRENT VERSION INFO
# result = subprocess.run(
#     ["python", "-m", "update.set_version_details"],
#     capture_output=True,
#     text=True
# )
# 
# print("STDOUT:\n", result.stdout)
# print("STDERR:\n", result.stderr)


# --- BUILD CUSTOM CLIENT ---
pyinstaller_cmd = [
    "pyinstaller",
    "main.py",
    f"--name={exe_name}",
    "--icon=images/FieldOps_AppIcon_256.ico",
    "--onefile",
    "--windowed",
    "--uac-admin",
    "--clean",
    "--add-data=images:images",
    "--add-data=fonts:fonts",
    "--version-file=update/version.txt",
    "--splash=images/splash.bmp"
]

print("Building with PyInstaller...")
subprocess.run(pyinstaller_cmd, check=True)
print("Build complete")