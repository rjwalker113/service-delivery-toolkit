# utils\parse_help_block.py

import re

HELP_BLOCK_RE = re.compile(
    r"<#(.*?)#>",
    re.DOTALL | re.IGNORECASE
)

SECTION_RE = re.compile(
    r"\.(\w+)\s*(.*?)"
    r"(?=\n\.\w+|\Z)",
    re.DOTALL | re.IGNORECASE
)

def parse_help_block(script_text):
    '''
    Extracts .DESCRIPTION (primary) and .SYNOPSIS (fallback)
    from a PowerShell script's comment-based help block.
    '''

    result = {
        "description": None,
        "synopsis": None
    }

    # Extract help block
    match = HELP_BLOCK_RE.search(script_text)
    if not match:
        return result

    help_block = match.group(1).strip()

    # Extract sections
    sections = {}
    for sec, content in SECTION_RE.findall(help_block):
        sec_name = sec.lower().strip()
        sections[sec_name] = content.strip()

    # Populate result
    result["description"] = sections.get("description")
    result["synopsis"] = sections.get("synopsis")

    return result
