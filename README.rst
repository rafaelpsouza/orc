ORC: Ops Remote Config
========================

This script helps you to export your tools configuration (like: sensu, collectd, HAProxy ...) to a remote git repository.

Installation
----

sudo pip install -e git+https://github.com/rafaelpsouza/orc.git#egg=orc

Usage
----

1) Using orc command::

	orc -r <REMOTE_REPOSITORY> -e <REMOTE_DIR> -c <CONFIG_DIR> -p <POST_CHANGE_COMMAND> -i <INTERVAL>

	orc --remote-repository <REMOTE_REPOSITORY> --remote-dir <REMOTE_DIR> --config-dir <CONFIG_DIR> --post-change-command <POST_CHANGE_COMMAND> --interval <INTERVAL>

** REMOTE_REPOSITORY: ** git repository url where the configuration is stored.

** REMOTE_DIR: ** A folder inside the git repository where the configuration is stored. Useful to create one folder per environment. ex: (dev, test, prod)

** CONFIG_DIR: ** Local configuration directory that will be replaced by a remote configuration. Ex: /etc/sensu

** POST_CHANGE_COMMAND: ** Command to be executed after a configuration change. Ex: 'sudo service xxx restart'

** INTERVAL: ** Interval, in seconds, that orc will check for remote configuration changes.

2. Using orc-runner.py

If you prefer or customize orc code, you can also clone orc repository and run orc-runner.py script with the same parameters above.

Usages and Examples
----

1. Sensu-server remote config::

	sudo orc -r https://github.com/rafaelpsouza/remote-config.git -e dev -c /etc/sensu -i 30 -p 'sudo sensu-server restart'

2. Collectd remote config::

	sudo orc -r https://github.com/rafaelpsouza/remote-config.git -e prod -c /etc/collectd -i 30 -p 'sudo collectd restart'