# -*- coding: utf-8 -*-
#
#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cliff import argparse

from gitrepo.commands import base
from gitrepo import schemas
from gitrepo import utils
from gitrepo import validator


class GitSyncCommand(base.BaseCommand):
    """Sync the projects."""

    entity_name = 'sync'

    def get_parser(self, prog_name):

        def _projects_file(path):
            if not utils.file_exists(path):
                raise argparse.ArgumentTypeError(
                    'File "{0}" does not exists'.format(path))
            return path

        parser = super(GitSyncCommand, self).get_parser(prog_name)
        parser.add_argument("-f", "--force",
                            action="store_true",
                            help="Force push.")
        parser.add_argument("path",
                            type=_projects_file,
                            metavar="file",
                            help="Path to mapping file in YAML format.")
        parser.add_argument("-p", "--project",
                            nargs='+',
                            help="Project(s) to sync.")
        return parser

    def take_action(self, parsed_args):
        data = validator.validate_file_by_schema(
            schemas.PROJECTS_SCHEMA,
            parsed_args.path
        )
        self.client.sync(data, parsed_args.project, parsed_args.force)
        self.app.stdout.write("====================\nCompleted...\n")


def debug(argv=None):
    """Helper to debug the Build command."""
    from gitrepo.app import debug
    debug("sync", GitSyncCommand, argv)


if __name__ == "__main__":
    debug()
