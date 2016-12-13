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

import logging

import git

from gitrepo.objects import RepoBase


class RepoSync(RepoBase):

    def __init__(self, src_url, repo_path, repo_name):
        super(RepoSync, self).__init__(repo_path, repo_name)
        try:
            self.repo = git.Repo(self.repo_full_path)
            self.repo.git.reset("--hard")
            self.repo.git.clean("-xdfq")
            self.repo.remote("origin").update()
        except git.exc.NoSuchPathError as e:
            logging.debug(e)
            self.repo = git.Repo.clone_from(src_url, self.repo_full_path)

    def setup_remote_dst_repo(self, dst_url, dst_name="dst"):
        """Setup remote repository to sync projects."""

        try:
            self.repo.delete_remote(dst_name)
        except git.exc.GitCommandError as e:
            logging.debug(e)

        self.repo.create_remote(dst_name, dst_url)

    def push_branch(self, branch, dst_name="dst", force=False):
        """Push changes from source branch to target one.

        :param branch: branch for pushing
        :type branch: str
        :param dst_name: destination repo name
        :type dst_name: str
        :param force: Forces update remote repo without any checks
        :type force: bool
        :return: success result as a tuple (True/False, err_msg)
        :rtype: tuple
        """

        push_infos = self.repo.remote(dst_name).push(
            "refs/remotes/origin/" + branch +
            ":" +
            "refs/heads/" + branch,
            force=force,
            tags=True
        )
        # Check for errors
        if push_infos:
            for push_info in push_infos:
                if push_info.flags & push_info.ERROR:
                    err_msg = ("Push failed for project '{0}': "
                               "{1}".format(self.repo_name, push_info.summary))
                    logging.error(err_msg)
                    return False, err_msg
        else:
            err_msg = "Push failed for project `{0}`".format(self.repo_name)
            logging.error(err_msg)
            return False, err_msg
        # if push was successful then error message is empty
        return True, ''
