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

**gitrepo sync [-h] [-f] [-p PROJECT [PROJECT ...]] [-t NUM_THREADS] file**

Sync the projects.

positional arguments:
   file                - Path to projects mapping file in YAML format (see format bellow)

.. code-block:: yaml

    - project: kubernetes
      src-repo: https://github.com/kubernetes/kubernetes
      dst-repo: ssh://127.0.0.1:29418/kubernetes/kubernetes
      branches:
        - "*"

optional arguments:
   -h, --help           Show help message and exit
   -f, --force          Force update remote repository without any checks
   -p, --project        Project(s) to sync
   -t, --num-thread     Number of worker threads (1 by default)


ToDo
----
* add additional commands;
* add ability to customise connection parameters;
* add more unit tests;


Contributors
------------

* skulanov@mirantis.com
* vitaliy@kulanov.org.ua
