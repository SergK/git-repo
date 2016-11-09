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

PROJECTS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "branches": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "dst-repo": {
                "type": "string"
            },
            "project": {
                "type": "string"
            },
            "src-repo": {
                "type": "string"
            }
        },
        "required": [
            "branches",
            "dst-repo",
            "project",
            "src-repo"
        ]
    }
}
