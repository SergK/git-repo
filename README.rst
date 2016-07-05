=======
gitrepo
=======

gitrepo provides a CLI tool and a Python API wrapper for interacting with git repositories


Usage
-----

**gitrepo [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]**

The utility for work with git projects.

optional arguments:
  --version            show program's version number and exit
  -v, --verbose        Increase verbosity of output. Can be repeated.
  -q, --quiet          Suppress output except warnings and errors.
  --log-file LOG_FILE  Specify a file to log output. Disabled by default.
  -h, --help           Show help message and exit.
  --debug              Show tracebacks on errors.

Commands:
  :complete:       print bash completion command
  :help:           print detailed help for another command
  :sync:           Sync the projects.

'gitrepo sync' example
----------------------

gitrepo sync [-h] [-f] [-p PROJECT [PROJECT ...]] file

Sync the projects.

positional arguments:
   file                 Path to mapping file in YAML format (see format bellow)

.. code-block:: yaml

    - project: kubernetes
      src-repo: https://github.com/kubernetes/kubernetes
      dst-repo: ssh://127.0.0.1:29418/kubernetes/kubernetes
      branches:
        - "*"

optional arguments:
   -h, --help           Show help message and exit
   -f, --force          Force push
   -p, --project        Project to sync


ToDo
----
* add additional commands;
* add ability allow to customise push user per each repo;
* add multithreading;
* add ability to customise connection parameters;
* add unit tests;


Contributors
------------

* skulanov@mirantis.com
* vitaliy@kulanov.org.ua
