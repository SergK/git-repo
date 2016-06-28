# -*- coding:utf8 -*-

#    Copyright 2016 Mirantis, Inc.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import logging

import argparse
import git
import sys

from git_repo_sync import schemas
from git_repo_sync.objects.projects import Project
from git_repo_sync.validator import Validator


def get_parser():
    parser = argparse.ArgumentParser(
        description="Sync repositories according to provided mapping"
    )
    parser.add_argument("-f", "--force",
                        action="store_true",
                        help="force push")
    parser.add_argument("-m", "--mapping",
                        metavar="FILE",
                        required=True,
                        help="path to mapping file in YAML format")
    parser.add_argument("-p", "--project",
                        metavar="PROJECT_NAME",
                        nargs='+',
                        help="project to sync")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s  %(levelname)8s  %(message)s")
    if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
        git.cmd.Git.GIT_PYTHON_TRACE = True

    validator = Validator()
    mapping = validator.validate_file_by_schema(
        schemas.PROJECTS_SCHEMA, args.mapping
    )

    # Sync only projects that are specified in cmd ('-p' option),
    # wrong project names will be omitted
    projects = []
    if args.project:
        for p_args in args.project:
            projects.extend(filter(lambda p: p['project'] == p_args, mapping))

    ec = 0
    # If there is no specified projects then sync all of them (from mapping)
    projects = projects or mapping
    logging.info("Started")
    for project in projects:
        try:
            Project(project['project'], project).sync(force=args.force)
        except Exception as e:
            logging.error("Unable to sync '{0}': {1}".format(
                project['project'],
                str(e))
            )
            ec = 1
    logging.info("Finished")
    sys.exit(ec)


if __name__ == "__main__":
    main()
