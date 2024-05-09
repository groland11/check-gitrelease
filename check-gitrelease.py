#!/usr/bin/env python

import os
import re
import subprocess

latest_version = ""
current_version = ""

env = os.environ.copy()
env["https_proxy"] = "http://proxy.example.com:8080"

if not os.path.isfile("/bin/git"):
    print("git command is missing")
    exit(3)

# Get locally installed Bacula-Web version
dirlink = os.readlink("/opt/bacula-web")
m = re.search(r"[0-9.]+", dirlink)
if m:
    current_version = m[0]
else:
    print("Unable to get installed version")
    exit(3)

# Get latest Bacula-Web version from GitHub repo
try:
    p = subprocess.run(["git", "ls-remote", "--tags", "https://github.com/bacula-web/bacula-web.git"], 
        text=True, 
        capture_output=True,
        check=True,
        timeout=8,
        env=env
    )
except TimeoutExpired as e:
    print("Timeout expired while querying remote GitHub repo")
    exit(2)
except CalledProcessError as e:
    print(f"Error querying remote GitHub repo: {e}")
    exit(1)

latest_tag = p.stdout.split()[-1]
m = re.search(r"[0-9.]+", latest_tag)
if m:
    latest_version = m[0]
else:
    print("Unable to parse latest release version")
    exit(3)

# Compare currently installed version to latest version on GitHub
if latest_version != current_version:
    print("There is a new version of Bacula-Web available for download. Please update!")
    print(f"{latest_version=}")
    print(f"{current_version=}")
    exit(10)

exit(0)
