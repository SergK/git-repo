# -*- coding: utf-8 -*-

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
import logging

from cliff import app
from cliff.commandmanager import CommandManager

import gitrepo


class Application(app.App):
    """Main cliff application class.

    Performs initialization of the command manager and
    configuration of basic engines.
    """

    def configure_logging(self):

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s  %(levelname)8s  %(message)s"
        )

        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            git.cmd.Git.GIT_PYTHON_TRACE = True


def main(argv=None):
    return Application(
        description="The utility for work with git projects.",
        version=gitrepo.__version__,
        command_manager=CommandManager("gitrepo",
                                       convert_underscores=True)
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
        description="The utility for work with git projects.",
        version="0.0.1",
        command_manager=cmd_mgr
    ).run(argv)
