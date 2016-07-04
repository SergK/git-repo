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
import six


# TODO(skulanov): Add configuration file to remove some hard-coded code
class GitSyncClient(object):
    """Provides high-level API to sync projects."""

    def sync(self, data, projects=None, force=False):
        if projects is not None:
            projects = self._filter_projects(data, projects)

        projects = projects or data

        for project in projects:
            try:
                logging.info("Synchronizing `{0}`".format(project['project']))
                self._get_src_repo(project)
                self._setup_dst_repo(project)
                for branch in project['branches']:
                    self._push_branch(project, branch, force)
            except Exception as e:
                logging.error("Unable to sync '{0}': {1}".format(
                    project['project'],
                    str(e))
                )

    @staticmethod
    def _filter_projects(data, projects):
        filtered_projects = []
        for project in projects:
            filtered_projects.extend(
                filter(lambda p: p['project'] == project, data)
            )
        return filtered_projects

    def _get_src_repo(self, project):
        # Clone or update cached repository
        cache_dir = os.path.join(
            os.getenv("HOME", "/home/jenkins"),
            "gitrepo-sync-cache", project['project']
        )
        try:
            self.repo = git.Repo(cache_dir)
            self.repo.git.reset('--hard')
            self.repo.git.clean('-xdfq')
            self.repo.remote("origin").update()
        except git.exc.NoSuchPathError as e:
            logging.info(e)
            self.repo = git.Repo.clone_from(project['src-repo'], cache_dir)

    def _setup_dst_repo(self, project):
        # Add "dst" repository as remote
        if project['dst-repo'].startswith("ssh://"):
            dst_repo_list = list(
                six.moves.urllib.parse.urlsplit(
                    project['dst-repo']
                )
            )
            username = os.getenv("GIT_PUSH_USERNAME", "admin")
            dst_repo_list[1] = username + "@" + dst_repo_list[1]
            dst_repo = six.moves.urllib.parse.urlunsplit(dst_repo_list)
        else:
            dst_repo = project['dst-repo']

        try:
            self.repo.delete_remote("dst")
        except git.exc.GitCommandError as e:
            logging.debug(e)

        self.repo.create_remote("dst", dst_repo)

    def _push_branch(self, project, branch, force=False):
        push_infos = self.repo.remote("dst").push(
            "refs/remotes/origin/" + branch +
            ":" +
            "refs/heads/" + branch,
            force=force
        )
        # Check for errors
        if push_infos:
            for push_info in push_infos:
                if push_info.flags & push_info.ERROR:
                    logging.error(
                        "Push failed for project `{0}`: {1}".format(
                            project['project'], push_info.summary
                        )
                    )
        else:
            logging.error("Push failed for project `{0}`".format(
                project['project'])
            )


def get_client():
    return GitSyncClient()
