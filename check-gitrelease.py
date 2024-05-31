#!/usr/bin/env python

import argparse
import logging
import os
import re
import sys
import subprocess

from urllib.parse import urlparse


__license__ = "GPLv3"
__version__ = "0.9"


latest_version = ""
local_version = ""

def parseargs():
    """Process command line arguments"""
    parser = argparse.ArgumentParser(description="Compare locally installed version of a program with latest release on GitHub")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="generate additional debug information")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    parser.add_argument("-l", "--local", type=str, required=True,
                        help="symbolic link to program file, e.g. /opt/app/application")
    parser.add_argument("-r", "--remote", type=str, required=True,
                        help="remote git repository, e.g. https://invent.kde.org/graphics/digikam")
    parser.add_argument("-p", "--proxy", type=str,
                        help="proxy, e.g. http://proxy.example.com:8080")
    parser.add_argument("-V", "--version", action="version", version=__version__)
    return parser.parse_args()

class LogFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.DEBUG, logging.INFO)

def get_logger(debug: bool = False) -> logging.Logger:
    """Retrieve logging object"""
    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    h1 = logging.StreamHandler(sys.stdout)
    h1.setLevel(logging.DEBUG)
    h1.addFilter(LogFilter())

    h2 = logging.StreamHandler(sys.stderr)
    h2.setLevel(logging.ERROR)

    logger.addHandler(h1)
    logger.addHandler(h2)

    return logger

def main():
    args = parseargs()
    logger = get_logger(args.debug)

    env = os.environ.copy()

    # Set internet proxy
    if args.proxy is not None:
        logger.debug(f"{args.proxy=}")
        env["https_proxy"] = args.proxy
        #print(env)
    
    # Check prerequisites
    if not os.path.isfile("/bin/git"):
        logger.error("ERROR: git command is missing")
        exit(3)
    
    # Get locally installed version
    # Symbolic link in form of: program -> program-2.3.4-release1 (version will be 2.3.4)
    logger.debug(f"Local link: {args.local}")
    try:
        dirlink = os.readlink(args.local)
    except FileNotFoundError as e:
        logger.error(f"ERROR: invalid local symbolic link {args.local}")
        exit(3)
    except OSError as e:
        logger.error(f"ERROR: file is not a symbolic link {args.local}")
        exit(3)

    m = re.search(r"[0-9.]+", dirlink)
    if m:
        local_version = m[0]
    else:
        logger.error(f"Unable to get version from file {dirlink}")
        exit(3)

    # Validate remote git url
    result = urlparse(args.remote)
    if result.scheme not in ["http", "https"] or result.netloc == "":
        logger.error(f"ERROR: invalid remote git repo {args.remote}")
        exit(3)

    # Get latest Bacula-Web version from GitHub repo
    logger.debug(f"Remote git repo: {args.remote}")
    try:
        p = subprocess.run(["git", "ls-remote", "--tags", args.remote], 
            text=True, 
            capture_output=True,
            check=True,
            timeout=8,
            env=env
        )
    except subprocess.TimeoutExpired as e:
        logger.error("Timeout expired while querying remote GitHub repo")
        exit(2)
    except subprocess.CalledProcessError as e:
        logger.error(f"Unable to query remote GitHub repo: {e}")
        exit(1)
    
    latest_tag = p.stdout.split()[-1]
    m = re.search(r"[0-9.]+", latest_tag)
    if m:
        latest_version = m[0]
    else:
        logger.error(f"Unable to parse latest release version {latest_tag}")
        exit(3)
    
    # Compare currently installed version to latest version on GitHub
    logger.debug(f"{local_version=}")
    logger.debug(f"{latest_version=}")
    if latest_version != local_version:
        logger.info(f"There is a new version {latest_version} available for download at {args.remote}. Please update!")
        exit(10)
    
if __name__ == '__main__':
    main()
