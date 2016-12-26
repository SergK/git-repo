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
import multiprocessing
import os

from functools import partial
from multiprocessing.dummy import Pool as ThreadPool

import git

from gitrepo import error
from gitrepo.objects.sync import RepoSync
from gitrepo.v1 import base


class GitSyncClient(base.GitBaseClient):
    """Provides high-level API to sync projects."""

    keys = ('project', 'src-repo', 'dst-repo', 'branches')

    @property
    def cache_dir(self):
        return os.path.join(os.getenv("HOME", "/home/jenkins"),
                            "gitrepo-sync-cache")

    def sync(self, data, projects=None, force=False, num_threads=1):
        """Sync specified projects from data. Supports multiple worker threads

        If projects is None then all projects from data will be synced.
         :param data: List of data description of projects
         :type data: list
         :param projects: List of string names of projects
         :type projects: list
         :param force: Forces update remote repository without any checks
         :type force: bool
         :param num_threads: Number of worker threads
         :type num_threads: int
         :return: list of sync results
         :rtype: list
         """

        if projects is not None:
            projects = self.filter_projects(data, projects)

        projects = projects or data

        partial_sync_single = partial(self.sync_single, force=force)

        pool = ThreadPool(num_threads)
        results = pool.map(partial_sync_single, projects)
        pool.close()
        pool.join()
        return results

    def sync_single(self, project, force=False):
        """Sync single project.

        :param project: Dict of data description of project
        :type project: dict
        :param force: Forces update remote repository without any checks
        :type force: bool
        :return: sync result as a dict {'project_name': (True/False, err_msg)}
        :rtype: dict
        """

        result, err_msg = False, None
        name, src, dst, branches = [project.get(k) for k in self.keys]
        # Set worker thread name based on repo project one
        multiprocessing.dummy.current_process().name = name
        logging.info("==== Synchronizing '{0}' ====".format(name))
        try:
            repo_obj = RepoSync(src, self.cache_dir, name)
            repo_obj.setup_remote_dst_repo(dst)
            for branch in branches:
                result, err_msg = repo_obj.push_branch(branch, force=force)
                if not result:
                    break
        except git.exc.GitCommandError as e:
            err_msg = "Unable to sync '{0}': {1}".format(name, str(e))
            logging.error(err_msg)
        return {name: (result, err_msg)}

    @staticmethod
    def filter_projects(data, projects):
        """Get specified projects from data.

         :param data: List of data description of projects
         :type data: list
         :param projects: List of all projects from data
         :type projects: list
         :return: List of specified projects from data
         :rtype: list
         """

        filtered_projects = []
        for project in projects:
            for item_data in data:
                if project == item_data['project']:
                    filtered_projects.append(item_data)
                    break
            else:
                log_msg = ("Input data for project '{}' "
                           "was not found ".format(project))
                logging.error(log_msg)

        if not filtered_projects:
            msg = "Nothing to do. No projects were found."
            raise error.ArgumentException(msg)

        return filtered_projects


def get_client():
    return GitSyncClient()
