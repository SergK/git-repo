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

import git

from cliff import app
from cliff.commandmanager import CommandManager

import gitrepo


class Application(app.App):
    """Main cliff application class.

    Performs initialization of the command manager and
    configuration of basic engines.
    """

    def configure_logging(self):
        # Redefine cliff's default logging message format by adding threadName
        # tag to identify logs from multiple threads
        self.CONSOLE_MESSAGE_FORMAT = ('[%(threadName)s] : '
                                       '%(levelname)-8s '
                                       '%(message)s')
        self.LOG_FILE_MESSAGE_FORMAT = ('[%(threadName)s] '
                                        '[%(asctime)s] '
                                        '%(levelname)-8s '
                                        '%(name)s '
                                        '%(message)s')
        super(Application, self).configure_logging()

        # Enables debugging of GitPython's git commands
        # depending on verbosity level
        git.cmd.Git.GIT_PYTHON_TRACE = {0: False,  # '-q'
                                        1: True,   # default level
                                        2: 'full'  # '-v'
                                        }.get(self.options.verbose_level, True)


def main(argv=None):
    return Application(
        description="The utility for work with git repositories.",
        version=gitrepo.__version__,
        command_manager=CommandManager("gitrepo", convert_underscores=True),
        deferred_help=True
    ).run(argv)


def debug(name, cmd_class, argv=None):
    """Helper for debugging single command without package installation."""
    import sys

    if argv is None:
        argv = sys.argv[1:]

    argv = [name] + argv + ["-v", "-v", "--debug"]
    cmd_mgr = CommandManager("test_gitrepo", convert_underscores=True)
    cmd_mgr.add_command(name, cmd_class)
    return Application(
        description="The utility for work with git repositories.",
        version=gitrepo.__version__,
        command_manager=cmd_mgr
    ).run(argv)
