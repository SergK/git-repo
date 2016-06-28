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


class GitRepoSyncException(Exception):
    pass


class ValidationError(GitRepoSyncException):
    pass


class FileIsEmpty(ValidationError):
    def __init__(self, file_path):
        super(FileIsEmpty, self).__init__(
            "File '{0}' is empty".format(file_path)
        )


class FileDoesNotExist(ValidationError):
    def __init__(self, file_path):
        super(FileDoesNotExist, self).__init__(
            "File '{0}' does not exist".format(file_path)
        )
