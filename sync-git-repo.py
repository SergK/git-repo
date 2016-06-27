#! /usr/bin/env python2

import argparse
import jsonschema
import logging
import os
import sys
import urlparse
from os import path

import git
import yaml


class BaseSchema(object):

    @property
    def metadata_schema(self):
        return {
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


class BaseValidator(object):

    @classmethod
    def validate_schema(cls, data, schema, file_path):
        logging.debug(
            'Start schema validation for %s file, %s', file_path, schema)
        try:
            jsonschema.validate(data, schema)
        except jsonschema.exceptions.ValidationError as exc:
            raise exc


class Project(object):

    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.cache_dir = path.join(os.getenv("HOME", "/home/jenkins"),
                                   "sync-git-repos-cache", self.name)

    def sync(self, force=False):
        self._force = force
        logging.info("Synchronizing `%s`", self.name)
        self._get_src_repo()
        self._setup_dst_repo()
        for branch in self.config["branches"]:
            self._push_branch(branch)

    def _get_src_repo(self):
        # Clone or update cached repository
        try:
            self.repo = git.Repo(self.cache_dir)
            self.repo.git.reset('--hard')
            self.repo.git.clean('-xdfq')
            self.repo.remote("origin").update()

        except git.exc.NoSuchPathError as e:
            logging.info(e)
            self.repo = git.Repo.clone_from(self.config["src-repo"],
                                            self.cache_dir)

    def _setup_dst_repo(self):
        # Add "dst" repository as remote
        if self.config["dst-repo"].startswith("ssh://"):
            dst_repo_list = list(urlparse.urlsplit(self.config["dst-repo"]))
            username = os.getenv("GIT_PUSH_USERNAME", "admin")
            dst_repo_list[1] = username + "@" + dst_repo_list[1]
            dst_repo = urlparse.urlunsplit(dst_repo_list)
        else:
            dst_repo = self.config["dst-repo"]

        try:
            self.repo.delete_remote("dst")
        except git.exc.GitCommandError as e:
            logging.debug(e)

        self.repo.create_remote("dst", dst_repo)

    def _push_branch(self, branch):
        push_infos = self.repo.remote("dst").push(
            "refs/remotes/origin/" + branch +
            ":" +
            "refs/heads/" + branch,
            force=self._force
        )
        # Check for errors
        if push_infos:
            for push_info in push_infos:
                if push_info.flags & push_info.ERROR:
                    logging.error(
                        "Push failed for project `%s`: %s",
                        self.name, push_info.summary
                    )
        else:
            logging.error("Push failed for project `%s`", self.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync repositories according to provided mapping"
    )
    parser.add_argument("-f", "--force", action="store_true",
                        help="force push")
    parser.add_argument("-m", "--mapping", metavar="FILE",
                        default="projects.yaml",
                        help="path to mapping file (default: %(default)s)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s  %(levelname)8s  %(message)s")
    if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
        git.cmd.Git.GIT_PYTHON_TRACE = True

    schema = BaseSchema()
    mapping = yaml.safe_load(open(args.mapping))
    BaseValidator.validate_schema(mapping,
                                  schema.metadata_schema,
                                  args.mapping)
    ec = 0
    logging.info("Started")
    for project in mapping:
        try:
            Project(project['project'], project).sync(force=args.force)
        except Exception as e:
            logging.error("Unable to sync `%s`: %s", project['project'], str(e))
            ec = 1
    logging.info("Finished")
    sys.exit(ec)
