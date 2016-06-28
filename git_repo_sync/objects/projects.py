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

import git
import os
import urlparse


class Project(object):

    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.cache_dir = os.path.join(os.getenv("HOME", "/home/jenkins"),
                                      "sync-git-repos-cache", self.name)

    def sync(self, force=False):
        self._force = force
        logging.info("Synchronizing `%s`", self.name)
        self._get_src_repo()
        self._setup_dst_repo()
        for branch in self.config["branches"]:
            self._push_branch(branch)

    def _get_src_repo(self):
        # Clone or update cached repository
        try:
            self.repo = git.Repo(self.cache_dir)
            self.repo.git.reset('--hard')
            self.repo.git.clean('-xdfq')
            self.repo.remote("origin").update()

        except git.exc.NoSuchPathError as e:
            logging.info(e)
            self.repo = git.Repo.clone_from(self.config["src-repo"],
                                            self.cache_dir)

    def _setup_dst_repo(self):
        # Add "dst" repository as remote
        if self.config["dst-repo"].startswith("ssh://"):
            dst_repo_list = list(urlparse.urlsplit(self.config["dst-repo"]))
            username = os.getenv("GIT_PUSH_USERNAME", "admin")
            dst_repo_list[1] = username + "@" + dst_repo_list[1]
            dst_repo = urlparse.urlunsplit(dst_repo_list)
        else:
            dst_repo = self.config["dst-repo"]

        try:
            self.repo.delete_remote("dst")
        except git.exc.GitCommandError as e:
            logging.debug(e)

        self.repo.create_remote("dst", dst_repo)

    def _push_branch(self, branch):
        push_infos = self.repo.remote("dst").push(
            "refs/remotes/origin/" + branch +
            ":" +
            "refs/heads/" + branch,
            force=self._force
        )
        # Check for errors
        if push_infos:
            for push_info in push_infos:
                if push_info.flags & push_info.ERROR:
                    logging.error(
                        "Push failed for project `%s`: %s",
                        self.name, push_info.summary
                    )
        else:
            logging.error("Push failed for project `%s`", self.name)
