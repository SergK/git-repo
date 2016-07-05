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
                            help="Force push")
        parser.add_argument("path",
                            type=_projects_file,
                            metavar="file",
                            help="Path to mapping file in YAML format")
        parser.add_argument("-p", "--project",
                            nargs='+',
                            help="Project to sync")
        return parser

    def take_action(self, parsed_args):
        data = validator.validate_file_by_schema(
            schemas.PROJECTS_SCHEMA,
            parsed_args.path
        )
        self.client.sync(data, parsed_args.project, parsed_args.force)
        self.app.stdout.write("Synchronization process completed\n")


def debug(argv=None):
    """Helper to debug the Build command."""
    from gitrepo.app import debug
    debug("sync", GitSyncCommand, argv)


if __name__ == "__main__":
    debug()
