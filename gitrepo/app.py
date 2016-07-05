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
