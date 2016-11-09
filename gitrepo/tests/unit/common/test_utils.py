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

import yaml

import mock

from oslotest import base as oslo_base

from gitrepo import utils


class TestUtils(oslo_base.BaseTestCase):

    @mock.patch('gitrepo.utils.os.path.lexists', side_effect=[True, False])
    def test_file_exists(self, lexists_mock):
        self.assertTrue(utils.file_exists('file1'))
        self.assertFalse(utils.file_exists('file2'))
        self.assertEqual(lexists_mock.call_args_list,
                         [mock.call('file1'), mock.call('file2')])

    def test_parse_yaml(self):
        test_data = {'test_key': 'test_val'}

        m_open = mock.mock_open(read_data=yaml.dump(test_data))
        with mock.patch('gitrepo.utils.open', m_open):
            self.assertEqual(utils.parse_yaml('fake/file/path'),
                             {'test_key': 'test_val'})
