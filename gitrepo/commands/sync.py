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

import junit_xml

from cliff import argparse

from gitrepo.commands import base
from gitrepo import schemas
from gitrepo import utils
from gitrepo import validator


class GitSyncCommand(base.BaseCommand):
    """Sync the projects."""

    entity_name = 'sync'

    @staticmethod
    def unpack_results(project):
        return ''.join([': '.join((k, v[1])) for k, v in project.items()])

    @staticmethod
    def create_junit_xml_file(projects, xml_file_path):
        """Create JUnit XML report file that can be used in Jenkins."""

        synced_projects = []
        for project in projects:
            for k, v in project.items():
                tc = junit_xml.TestCase(k)
                tc.add_error_info(message=v[1])
                synced_projects.append(tc)
        ts = junit_xml.TestSuite("Sync", synced_projects)
        with open(xml_file_path, 'w') as f:
            junit_xml.TestSuite.to_file(f, [ts])

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
        parser.add_argument("-t", "--num-threads",
                            type=int,
                            default=1,
                            help="Number of threads.")
        parser.add_argument("--junit-xml",
                            nargs='?',
                            metavar='XML_FILE',
                            const='result.xml',
                            help="Create JUnit XML file.")
        return parser

    def take_action(self, parsed_args):
        data = validator.validate_file_by_schema(
            schemas.PROJECTS_SCHEMA,
            parsed_args.path
        )
        result = self.client.sync(data,
                                  parsed_args.project,
                                  parsed_args.force,
                                  parsed_args.num_threads)
        total = len(result)
        passed = sum([v.values()[0][0] for v in result])
        failed_projects = [i for i in result if not i.values()[0][0]]
        failed_msg = '\n'.join(map(self.unpack_results, failed_projects))
        self.app.stdout.write("====================\nCompleted...\n\n")
        self.app.stdout.write("TOTAL: {0}\n"
                              "  Successfully synced: {1}\n"
                              "  Synced FAILED: {2}\n-----\n{3}\n"
                              "".format(total,
                                        passed,
                                        total - passed,
                                        failed_msg))
        if parsed_args.junit_xml:
            self.create_junit_xml_file(result, parsed_args.junit_xml)


def debug(argv=None):
    """Helper to debug the Sync command."""
    from gitrepo.app import debug
    debug("sync", GitSyncCommand, argv)


if __name__ == "__main__":
    debug()
