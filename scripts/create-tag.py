#!/usr/bin/python3

import glob
import json
import sys
from datetime import date

try:
    from git import Repo
except ImportError as ie:
    print(f"Could not import git module (install with apt install python3 or pip install GitPython): {ie}")
    sys.exit(1)


def read_versions():
    versions = {}

    revpi_hat_templates = sorted(glob.glob("./revpi-hat-PR*.json"))

    for template in revpi_hat_templates:
        with open(template, "r") as f:
            template_data = json.loads(f.read())

            product_id = template_data["pid"] + 100000
            product_revision = template_data["prev"]
            data_version = template_data["eeprom_data_version"]

            name = f"PR{product_id}R{product_revision:02d}"

            versions[name] = data_version

    return versions


versions = read_versions()

repo = Repo()

active_branch = repo.active_branch
last_tag = list(repo.tags)[-1]

repo.git.checkout(last_tag)
old_versions = read_versions()

repo.git.checkout(active_branch)


changelog = []

for product, version in versions.items():
    if version == 0:
        # ignore unreleased templates
        continue

    if product in old_versions:
        previous_version = old_versions[product]

        if version > previous_version:
            changelog.append(f"{product} V{previous_version} -> V{version}")
    else:
        changelog.append(f"{product} V{previous_version}")

if not changelog:
    print("No changes found. Exiting.")
    sys.exit(0)

counter = 1
today = date.today().strftime("%Y%m%d")

# check if we already have a tag for today and increment
if str(last_tag).startswith(today):
    _, counter = str(last_tag).split("-")
    counter = int(counter) + 1

tag = f"{today}-{counter}"
message = f"Release {tag}\n\n" + "\n".join(changelog)

print(f"Found {len(changelog)} changes. The following tag would be created:\n")
print("-" * 70)
print(message)
print("-" * 70)

print("\nIn order to proceed please press any key...")

input()

repo.create_tag(tag, message=message)

print(
    f"Successfully created tag '{tag}'."
    " Please check the result and don't forget to push tag via 'git push --tags' if everything is ok."
)
