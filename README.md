# remote_deploy
Simple tool to deploy remote files and packages

# Requirements
- Python3 is required.
- sshpass package is required to pass SSH password non-interactively. Install sshpass on MacOS:  
```brew install sshpass```

# Architecture

All the code is placed in a single Python file remote.py, located on a client. Remote hosts do not need any bootstrap.  

Based on the local configuration.json, Python script remote.py through SSH connects to remote hosts. Script processes configured hosts one by one, installs/remove packages, installs files and restarts services by running remote SSH commands.

Two Python classes handle the workflow:
- RemoteExecutor. This class opens SSH session and executes remote commands over SSH
- Control. This class reads JSON configuration, password and creates RemoteExecutor instances, passing configuration info to them

Script manages deployments in a single thread. For a larger number of hosts class Control can be easily extended into multi-threaded architecture to manage a massive number of hosts in parallel, asynchronously.

# Configuration

Deployment configuration is stored in JSON file configuration.json:
- "hosts" section lists the hosts where to install files
- "packages" section lists the packages to install or remove. JSON "deploy_mode" element controls mode: it can take a value "install" or "remove".
- "files" section lists the files to deploy with their attributes . Only web root /var/www/html/ is allowed for deployment
- "restarts" section lists the OS services to restart  

Files for remote installation are taken from files2deploy folder.

# Notes
- For security reasons it is a good practice not to use root access, some other user should be used and sudo privilege granted. But for the sake of  --- simplicity root user is used.  
- For security reasons it is a good practice not to store password in the code, so program will ask for password.  
- For security reasons files are allowed to be installed only to ONE remote folder, which is web root, ALLOWED_DIR=/var/www/html/  
- For security reasons root password is redacted from log, password replaced with the keyword <censored> :)
- For simplicity creation of remote directories is not supported. Only remote files installation is supported as required.  

# How to invoke program
  ```python3 remote.py```
Script will ask for a password.  

Check logs:
```tail -f remote.log```

# Unit tests
Validate that a host responds through HTTP with response "Hello, world!\n"  

How to invoke tests:
  ```python3 tests/tests.py```

Check logs:
  ```tail -f tests/remote.log```

Sample tests output:

```
Enter password for user root :

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.


WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

.
----------------------------------------------------------------------
Ran 1 test in 15.826s

OK
```

# Logs

Example of successful execution:

```(base) yb@Yan-Home-Mac remote_deploy % tail -f remote.log
2024-05-13 21:24:52,123:    read_configuration() : INFO     : Reading deployment configuration
2024-05-13 21:24:52,126:               install() : INFO     : Applying changes to remote hosts
2024-05-13 21:24:52,126:               install() : INFO     : Starting with host 54.174.79.219
2024-05-13 21:24:52,126:           install_rpm() : INFO     : Installing OS package: apache2
2024-05-13 21:24:52,126:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@54.174.79.219 'apt install apache2 -y'
2024-05-13 21:24:54,308:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@54.174.79.219 'apt install apache2 -y' successfully
2024-05-13 21:24:54,309:           install_rpm() : INFO     : Installing OS package: php libapache2-mod-php
2024-05-13 21:24:54,309:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@54.174.79.219 'apt install php libapache2-mod-php -y'
2024-05-13 21:24:56,011:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@54.174.79.219 'apt install php libapache2-mod-php -y' successfully
2024-05-13 21:24:56,012:          install_file() : INFO     : Installing file index.php to /var/www/html/
2024-05-13 21:24:56,012:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> scp /Users/yb/Documents/Python/remote_deploy/files2deploy/index.php root@54.174.79.219:/var/www/html/
2024-05-13 21:24:57,414:          install_file() : INFO     : Installing owner www-data, for file index.php
2024-05-13 21:24:57,414:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@54.174.79.219 'chown www-data /var/www/html/index.php'
2024-05-13 21:24:58,669:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@54.174.79.219 'chown www-data /var/www/html/index.php' successfully
2024-05-13 21:24:58,669:          install_file() : INFO     : Installing group: www-data for file index.php
2024-05-13 21:24:58,670:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@54.174.79.219 'chgrp www-data /var/www/html/index.php'
2024-05-13 21:24:59,891:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@54.174.79.219 'chgrp www-data /var/www/html/index.php' successfully
2024-05-13 21:24:59,891:          install_file() : INFO     : Installing mode: 700 for file index.php
2024-05-13 21:24:59,891:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@54.174.79.219 'chmod 700 /var/www/html/index.php'
2024-05-13 21:25:01,157:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@54.174.79.219 'chmod 700 /var/www/html/index.php' successfully
2024-05-13 21:25:01,158:       restart_service() : INFO     : Restarting service: apache2
2024-05-13 21:25:01,158:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@54.174.79.219 'service apache2 restart'
2024-05-13 21:25:02,946:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@54.174.79.219 'service apache2 restart' successfully
2024-05-13 21:25:02,947:               install() : INFO     : Completed with host 54.174.79.219
2024-05-13 21:25:02,947:               install() : INFO     : Starting with host 3.89.242.163
2024-05-13 21:25:02,947:           install_rpm() : INFO     : Installing OS package: apache2
2024-05-13 21:25:02,947:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'apt install apache2 -y'
2024-05-13 21:25:04,658:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'apt install apache2 -y' successfully
2024-05-13 21:25:04,658:           install_rpm() : INFO     : Installing OS package: php libapache2-mod-php
2024-05-13 21:25:04,658:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'apt install php libapache2-mod-php -y'
2024-05-13 21:25:06,349:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'apt install php libapache2-mod-php -y' successfully
2024-05-13 21:25:06,350:          install_file() : INFO     : Installing file index.php to /var/www/html/
2024-05-13 21:25:06,350:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> scp /Users/yb/Documents/Python/remote_deploy/files2deploy/index.php root@3.89.242.163:/var/www/html/
2024-05-13 21:25:07,756:          install_file() : INFO     : Installing owner www-data, for file index.php
2024-05-13 21:25:07,756:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'chown www-data /var/www/html/index.php'
2024-05-13 21:25:08,942:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'chown www-data /var/www/html/index.php' successfully
2024-05-13 21:25:08,942:          install_file() : INFO     : Installing group: www-data for file index.php
2024-05-13 21:25:08,943:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'chgrp www-data /var/www/html/index.php'
2024-05-13 21:25:10,134:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'chgrp www-data /var/www/html/index.php' successfully
2024-05-13 21:25:10,135:          install_file() : INFO     : Installing mode: 700 for file index.php
2024-05-13 21:25:10,135:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'chmod 700 /var/www/html/index.php'
2024-05-13 21:25:11,373:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'chmod 700 /var/www/html/index.php' successfully
2024-05-13 21:25:11,373:       restart_service() : INFO     : Restarting service: apache2
2024-05-13 21:25:11,373:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'service apache2 restart'
2024-05-13 21:25:13,072:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'service apache2 restart' successfully
2024-05-13 21:25:13,072:               install() : INFO     : Completed with host 3.89.242.163
2024-05-13 21:25:13,072:               install() : INFO     : Completed applying changes to all configured hosts
```
