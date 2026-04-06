import subprocess
from admin.config import options

# --- SET CONFIG VARS ---
app_name = options["app_name"]
version = options["app_version"]
icon = options["branding"]["icon"]
splash = options["branding"]["splash"]
require_admin = options["require_admin"]

exe_name = f"{app_name} - v{version}"

# --- PYINSTALLER COMMAND ---
pyinstaller_cmd = [
    "pyinstaller",
    "main.py",
    f"--name={exe_name}",
    f"--icon={icon}",
    "--onefile",
    "--windowed",
    "--clean",
    f"--splash={splash}",
    "--add-data=assets:assets",
    "--add-data=branding:branding",
]

print("Building with PyInstaller...")
subprocess.run(pyinstaller_cmd, check=True)
print("Build complete.")
