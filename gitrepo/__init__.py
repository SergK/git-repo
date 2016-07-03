# -*- coding: utf-8 -*-

#    Copyright 2015 Mirantis, Inc.
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

import pbr.version

from gitrepo import v1

__all__ = ["v1", "__version__"]

try:
    __version__ = pbr.version.VersionInfo(
        'gitrepo').version_string()
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
