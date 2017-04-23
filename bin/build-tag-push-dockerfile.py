#!/usr/bin/env python
"""
    build-tag-push-dockerfile.py

    Simple deployment script for Dockerfile projects

    Builds, Tags and then Push a Docker Image based on
    a Dockerfile to Docker Hub and then can create a GitHub Release

"""

import os
import argparse
import subprocess
import re

from argparse import RawTextHelpFormatter
from functools import partial


COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')
STYLES = ()


def color(s, fg=None, bg=None, style=None):
    sgr = []

    if fg:
        if fg in COLORS:
            sgr.append(str(30 + COLORS.index(fg)))
        elif isinstance(fg, int) and 0 <= fg <= 255:
            sgr.append('38;5;%d' % int(fg))
        else:
            raise Exception('Invalid color "%s"' % fg)

    if bg:
        if bg in COLORS:
            sgr.append(str(40 + COLORS.index(bg)))
        elif isinstance(bg, int) and 0 <= bg <= 255:
            sgr.append('48;5;%d' % bg)
        else:
            raise Exception('Invalid color "%s"' % bg)

    if style:
        for st in style.split('+'):
            if st in STYLES:
                sgr.append(str(1 + STYLES.index(st)))
            else:
                raise Exception('Invalid style "%s"' % st)

    if sgr:
        prefix = '\x1b[' + ';'.join(sgr) + 'm'
        suffix = '\x1b[0m'
        return prefix + s + suffix
    else:
        return s

red = partial(color, fg='red')
green = partial(color, fg='green')
yellow = partial(color, fg='yellow')
blue = partial(color, fg='blue')


# ==============================================================================

# Argument Parsing
# ================
parser = argparse.ArgumentParser(
    description="Build, tag and push docker image.\n\n"
    "Note: The script will only create a new 'release' docker-compose file "
    "unless specified with the correct options.",
    formatter_class=RawTextHelpFormatter
)

parser.add_argument(
    "--image",
    dest="image_name",
    action="store",
    required=True,
    help="the docker image name WITHOUT tag in format <hub-user>/<repo-name>"
)

parser.add_argument(
    "--version",
    dest="version",
    action="store",
    help="the version you want to release"
)

parser.add_argument(
    "--github_release",
    dest="push_to_github",
    action="store_true",
    default=False,
    help="If added we push a release to github"
)
parser.add_argument(
    "--dockerhub_release",
    dest="push_to_dockerhub",
    action="store_true",
    default=False,
    help="If added we push a release to docker hub"
)

args = parser.parse_args()

print(
    green("====>> Creating Release: ") +
    yellow("%s" % args.version) + "\n" +
    green("====>> for Docker Image: ") +
    yellow("%s" % args.image_name)
)
print(
    green("====>> Push to Docker Hub: ") +
    yellow("%s" % args.push_to_dockerhub) + "\n" +
    green("====>> Push to GitHub: ") +
    yellow("%s" % args.push_to_github)
)


# Basic Sanity Checks
# ===================
if not os.path.isfile('./Dockerfile'):
    print red("\nERROR: Current Working Directory should have a Dockerfile\n")
    exit(1)

user_name = os.environ.get("DOCKERHUB_USER")
user_pass = os.environ.get("DOCKERHUB_PASS")

if None in [user_name, user_pass]:
    print red("\nERROR: Please set the DOCKERHUB_USER and DOCKERHUB_PASS to your user name, e.g.:")
    print red("       export DOCKERHUB_USER=james")
    print red("       export DOCKERHUB_PASS=password12\n")
    exit(1)

VERSION_FORMAT = re.compile('\d.\d.\d[\w]*')

if VERSION_FORMAT.match(args.version) is None:
    print red("\nERROR: The release version should be of the format <MAJOR>.<MINOR>.<PATCH>\n")
    exit(1)


# Create Docker Images
# ====================
RELEASE_TAG = args.image_name + ":" + args.version
DOCKER_HUB_FORMAT = re.compile('[-a-zA-Z0-9-]+\/[-a-zA-Z0-9-]+:[-a-zA-Z0-9]+')

if DOCKER_HUB_FORMAT.match(RELEASE_TAG) is None:
    print red("\nERROR: The Docker image should be of the format <hub-user>/<repo-name>:<tag>\n")
    exit(1)

# Build and Tag Docker Images
# ===========================
print green("====>> Building and Tagging Release: %s" % (RELEASE_TAG))
subprocess.check_call(["docker", "build", "-t", RELEASE_TAG, "."])


# Push to Docker Hub (if selected)
# ================================
if args.push_to_dockerhub:
    process = subprocess.Popen(["docker", "login", "-u", user_name, "-p", user_pass])
    process.wait()

    if process.returncode != 0:
        print red("\nERROR: Login to Docker Hub Failed.\n")
        exit(1)

    process = subprocess.Popen(["docker", "push", RELEASE_TAG])
    process.wait()

    if process.returncode != 0:
        print red("\nERROR: Push to Docker Hub Failed.\n")
        exit(1)

# Push to GitHub
# ==============
if args.push_to_github:
    process = subprocess.Popen(
        ["git", "status", "--porcelain"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    git_status = str(process.communicate()[0]).strip()

    if git_status:
        print red("\nERROR: There are some uncommited changes.\n")
        print red("%s" % git_status)
        exit(1)

    print green("====>> Removing any local only git tags")
    process = subprocess.Popen(
        ["git", "fetch", "--prune", "origin", "+refs/tags/*:refs/tags/*"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    git_prune_local_tags = str(process.communicate()[0]).strip()

    process = subprocess.Popen(
        ["git", "rev-list", "--tags", "--max-count=1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    git_rev = str(process.communicate()[0]).strip()

    if process.returncode == 0:
        process = subprocess.Popen(
            ["git", "describe", "--tags", git_rev],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        git_current_tag = str(process.communicate()[0]).strip()

        print green("====>> Getting the latest commits since %s for release notes" % git_current_tag)
        process = subprocess.Popen(
            ["git", "log", git_current_tag+'...HEAD'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        commits_since_tag = str(process.communicate()[0]).strip()
    else:
        print yellow("====>> No tags found. Finding ALL commits for release notes instead ...")
        process = subprocess.Popen(
            ["git", "log"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        commits_since_tag = str(process.communicate()[0]).strip()

    process = subprocess.Popen(
        ["git", "tag", "-a", args.version, "-m", commits_since_tag],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print blue("====>> Release Notes: \n\n%s\n" % commits_since_tag)
    print green("====>> Pushing %s to github" % args.version)

    process = subprocess.Popen(
        ["git", "push", "origin", args.version],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    process.wait()
    (output, error) = process.communicate()
    print output, error
