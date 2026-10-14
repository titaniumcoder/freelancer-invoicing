import datetime
import os
import pathlib
import re
import subprocess


changelog_path = pathlib.Path("CHANGELOG.md")
changelog = changelog_path.read_text()

match = re.search(r"## \[Unreleased\]\n(.*?)(?=^## \[|\Z)", changelog, re.S | re.M)
body = match.group(1) if match else ""
entries = [line for line in body.splitlines() if line.startswith("- ")]

if not entries:
    with open(os.environ["GITHUB_OUTPUT"], "a") as out:
        out.write("skip=true\n")
    raise SystemExit(0)

bump = "patch"
if "<!-- major -->" in body:
    bump = "major"
elif "<!-- minor -->" in body:
    bump = "minor"

tags = subprocess.run(
    ["git", "tag", "--list", "v*", "--sort=-v:refname"],
    capture_output=True, text=True, check=True,
).stdout.split()
last = tags[0].lstrip("v") if tags else "0.0.0"
major, minor, patch = (int(part) for part in last.split("."))

if bump == "major":
    major, minor, patch = major + 1, 0, 0
elif bump == "minor":
    minor, patch = minor + 1, 0
else:
    patch += 1

version = f"{major}.{minor}.{patch}"
today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()

fresh_unreleased = """## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

"""

release_section = f"## [{version}] - {today}\n{body.rstrip()}\n\n"

new_changelog = changelog[: match.start()] + fresh_unreleased + release_section + changelog[match.end():]
changelog_path.write_text(new_changelog)

pathlib.Path("release-notes.md").write_text(body.rstrip() + "\n")

with open(os.environ["GITHUB_OUTPUT"], "a") as out:
    out.write(f"skip=false\nversion={version}\n")
