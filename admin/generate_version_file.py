from datetime import datetime
import json
from pathlib import Path

def generate_version_file(config):
    version = config["app_version"]
    app_name = config["app_name"]
    org_name = config["org_name"]
    build_date = datetime.now().strftime('%d.%m.%Y')

    # Convert semantic version "1.2.3" → tuple (1,2,3,0)
    version_tuple = tuple(map(int, version.split("."))) + (0,)

    version_text = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version_tuple},
    prodvers={version_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable('040904E4', [
        StringStruct('CompanyName', '{org_name}'),
        StringStruct('FileDescription', '{app_name}'),
        StringStruct('FileVersion', '{version}'),
        StringStruct('ProductVersion', '{version}'),
        StringStruct('ProductName', '{app_name}'),
        StringStruct('InternalName', '{app_name}'),
        StringStruct('OriginalFilename', '{app_name}.exe'),
        StringStruct('BuildDate', '{build_date}')
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""

    out_path = Path("admin/version.txt")
    out_path.write_text(version_text, encoding="utf-8")
    return out_path
