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

import os


class RepoBase(object):

    def __init__(self, repo_path, repo_name):
        self._repo_path = repo_path
        self._repo_name = repo_name

    @property
    def repo_full_path(self):
        return os.path.join(self._repo_path, self._repo_name)

    @property
    def repo_name(self):
        return self._repo_name
