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

import abc

from cliff import command
import six

import gitrepo

VERSION = 'v1'


@six.add_metaclass(abc.ABCMeta)
class BaseCommand(command.Command):
    """Super class for gitrepo commands."""

    def __init__(self, *args, **kwargs):
        super(BaseCommand, self).__init__(*args, **kwargs)
        self.client = gitrepo.get_client(self.entity_name, VERSION)

    @abc.abstractproperty
    def entity_name(self):
        """Name of the gitrepo entity."""
        pass

    @property
    def stdout(self):
        """Shortcut for self.app.stdout."""
        return self.app.stdout
