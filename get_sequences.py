"""Write the sequences tagged L0_version_1-Template in the workspace export as GenBank files."""

import json
import os

TAG = "L0_version_1-Template"

workspace = json.load(open("project1/input/workspace.json"))

tag_id = next(t["id"] for t in workspace["tags"] if t["name"] == TAG)
file_contents = {s["id"]: s["file_content"] for s in workspace["cloning_strategy"]["sequences"]}

os.makedirs("project1/input/sequences", exist_ok=True)

for sequence in workspace["sequences"]:
    if tag_id in sequence["tag_ids"]:
        with open(f"project1/input/sequences/{sequence['name']}.gb", "w") as f:
            f.write(file_contents[sequence["id"]])
