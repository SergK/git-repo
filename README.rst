Project
=======

Synchronize git repositories (mirroring). Please check yaml format from docs/projects.yaml

.. code-block:: yaml

    - project: kubernetes
      src-repo: https://github.com/kubernetes/kubernetes
      dst-repo: ssh://127.0.0.1:29418/kubernetes/kubernetes
      branches:
        - "*"

Run
~~~
git-repo-sync -m docs/projects.yaml




ToDo
----
* add multithreading;
* allow to customise push user per each repo;
* add unit test



Contributors
------------

skulanov@mirantis.com
vitaliy@kulanov.org.ua
