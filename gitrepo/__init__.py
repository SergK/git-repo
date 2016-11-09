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

import pbr.version

from gitrepo import v1

__all__ = ["v1", "__version__"]

try:
    __version__ = pbr.version.VersionInfo('gitrepo').version_string()
except Exception:
    __version__ = "0.0.0"


def get_client(resource, version='v1'):
    """Gets an API client for a resource

    gitrepo provides access to Gitrepo's API
    through a set of per-resource facades. In order to
    get a proper facade it's necessary to specify the name
    of the API resource and the version of Gitrepo's API.

    :param resource: Name of the resource to get a facade for.
    :type resource:  str
                     Valid values are environment, node and task
    :param version:  Version of the Gitrepo's API
    :type version:   str,
                     Available: v1. Default: v1.
    :return:         Facade to the specified resource that wraps
                     calls to the specified version of the API.

    """
    from gitrepo import v1

    version_map = {
        'v1': {
            'sync': v1.sync
        }
    }

    try:
        return version_map[version][resource].get_client()
    except KeyError:
        msg = 'Cannot load API client for "{r}" in the API version "{v}".'
        raise ValueError(msg.format(r=resource, v=version))
