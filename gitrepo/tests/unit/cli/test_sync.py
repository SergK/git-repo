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

import mock

from gitrepo.tests.unit.cli import clibase


PROJECTS_YAML = '''
- project: project_1
  src-repo: https://src/path/to/repo_1
  dst-repo: ssh://dst@127.0.0.1:9999/path/to/repo_1
  branches:
   - "*"
- project: project_2
  src-repo: https://src/path/to/repo_2
  dst-repo: ssh://dst@127.0.0.1:9999/path/to/repo_2
  branches:
   - master
'''


class TestSyncCommand(clibase.BaseCLITest):

    @mock.patch('gitrepo.utils.file_exists', return_value=True)
    def test_sync(self, _):
        expected_path = '/tmp/fake_projects.yaml'
        args = 'sync {file_path} -p project_1'.format(file_path=expected_path)

        m_open = mock.mock_open(read_data=PROJECTS_YAML)
        with mock.patch('gitrepo.utils.open', m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path)
        self.m_get_client.assert_called_once_with('sync', mock.ANY)

    @mock.patch('sys.stderr')
    def test_sync_fail(self, mocked_stderr):
        args = 'sync'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('error',
                      mocked_stderr.write.call_args_list[-1][0][0])
