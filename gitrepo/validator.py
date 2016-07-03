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

import jsonschema
import six

from gitrepo import errors
from gitrepo import utils


def validate_schema(data, schema, file_path, value_path=None):
    logging.debug(
        "Start schema validation for {0} file, {1}".format(
            file_path,
            schema
        )
    )
    try:
        jsonschema.validate(data, schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise errors.ValidationError(
            _make_error_message(exc, file_path, value_path))


def validate_file_by_schema(schema, file_path):
    if not utils.file_exists(file_path):
        raise errors.FileDoesNotExist(file_path)

    data = utils.parse_yaml(file_path)
    if data is not None:
        validate_schema(data, schema, file_path)
    else:
        raise errors.FileIsEmpty(file_path)
    return data


def _make_error_message(exc, file_path, value_path):
    if value_path is None:
        value_path = []

    if exc.absolute_path:
        value_path.extend(exc.absolute_path)

    if exc.context:
        sub_exceptions = sorted(
            exc.context, key=lambda e: len(e.schema_path), reverse=True)
        sub_message = sub_exceptions[0]
        value_path.extend(list(sub_message.absolute_path)[2:])
        message = sub_message.message
    else:
        message = exc.message

    error_msg = "File '{0}', {1}".format(file_path, message)

    if value_path:
        value_path = ' -> '.join(map(six.text_type, value_path))
        error_msg = '{0}, {1}'.format(
            error_msg, "value path '{0}'".format(value_path))

    return error_msg
