from pathlib import Path
import re
import json

# Get the path of this file.
path = Path(__file__).parent

with open(path / ".vimrc", "r", encoding="utf-8") as f:
    lines = f.readlines()

maptypes = {
    "nmap": "vim.normalModeKeyBindings",
    "vmap": "vim.visualModeKeyBindings",
    "imap": "vim.insertModeKeyBindings",
    "nnoremap": "vim.normalModeKeyBindingsNonRecursive",
    "vnoremap": "vim.visualModeKeyBindingsNonRecursive",
    "inoremap": "vim.insertModeKeyBindingsNonRecursive",
}

jsondata = {
    "vim.normalModeKeyBindings": [],
    "vim.visualModeKeyBindings": [],
    "vim.insertModeKeyBindings": [],
    "vim.normalModeKeyBindingsNonRecursive": [],
    "vim.visualModeKeyBindingsNonRecursive": [],
    "vim.insertModeKeyBindingsNonRecursive": [],
}


# Parses abc to ["a", "b", "c"] and :wq<CR> to [":wq"]
def mapToJSONList(mapstring, after=False):
    if after and mapstring.startswith(":") and len(mapstring) > 1:
        map_json = re.match("(:\w+)", mapstring).group(1)
        return {"command": [map_json]}

    parts = re.findall("(<[^>]+>|.)", mapstring)
    return {"after" if after else "before": parts}


# Get all the mappings and place them in the correct category.
for item in lines:
    matches = re.match("(^.*map)\s([\S]+)\s+([\S]+)$", item)
    if matches:
        maptype = matches.group(1)
        before = mapToJSONList(matches.group(2))
        after = mapToJSONList(matches.group(3), True)
        maptype = maptypes[maptype]
        jsondata[maptype].append({**before, **after})


# Write the JSON to settings.json in the same directory.
with open(path / "settings.json", "w") as f:
    json.dump(jsondata, f, indent=4)
