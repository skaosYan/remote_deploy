README.md# remote_deploy
Simple remote deployment tool  

#Architecture

# Notes
- For security reasons, it is a good practice not to use root access, some other user should be used and sudo privilege granted. But for the sake of  --- simplicity I use root.  
- For security reasons, it is a good practice not to store password in the code, so program will ask for password.  
- For security reasons, files are allowed to be installed only to ONE remote folder, which is web root, ALLOWED_DIR=/var/www/html/  
- For security reasons, root password is redacted from log, password replaced with the keyword <censored> :)
- For simplicity, creation of remote directories is not supported. Only remote files installation is supported as required.  

# Configuration

Deployment configuration is stored in JSON file configuration.json:
- "hosts" section lists the hosts where to install files
- "packages" section lists the packages to install or to remove
- "files" section lists the files and attributes to deploy. Only web root /var/www/html/ is allowed for deployment
- "restarts" section lists the services to restart


# How to invoke program
  ```python3 remote.py```
Script will ask for user password.

Check logs:
  ```tail -f remote.log```


# How to invoke tests
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

Example of successful execution

```(base) yb@Yan-Home-Mac remote_deploy % tail -f remote.log
2024-05-13 20:07:23,081:    read_configuration() : INFO     : Reading deployment configuration
2024-05-13 20:07:28,099:               install() : INFO     : Applying changes to remote hosts
2024-05-13 20:07:28,099:           install_rpm() : INFO     : Installing OS package: apache2
2024-05-13 20:07:28,099:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'apt install apache2 -y'
2024-05-13 20:07:45,002:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'apt install apache2 -y' successfully
2024-05-13 20:07:45,002:           install_rpm() : INFO     : Installing OS package: php libapache2-mod-php
2024-05-13 20:07:45,002:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'apt install php libapache2-mod-php -y'
2024-05-13 20:08:04,174:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'apt install php libapache2-mod-php -y' successfully
2024-05-13 20:08:04,174:          install_file() : INFO     : Installing file: index.php to /var/www/html/
2024-05-13 20:08:04,174:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> scp /Users/yb/Documents/Python/remote_deploy/files2deploy/index.php root@3.89.242.163:/var/www/html/
2024-05-13 20:08:05,786:          install_file() : INFO     : Installing file owner: www-data, for index.php
2024-05-13 20:08:05,786:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'chown www-data /var/www/html/index.php'
2024-05-13 20:08:06,733:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'chown www-data /var/www/html/index.php' successfully
2024-05-13 20:08:06,733:          install_file() : INFO     : Installing group owner: www-data for index.php
2024-05-13 20:08:06,733:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'chgrp www-data /var/www/html/index.php'
2024-05-13 20:08:07,639:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'chgrp www-data /var/www/html/index.php' successfully
2024-05-13 20:08:07,640:          install_file() : INFO     : Installing file mode: 700 for file index.php
2024-05-13 20:08:07,640:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'chmod 700 /var/www/html/index.php'
2024-05-13 20:08:08,557:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'chmod 700 /var/www/html/index.php' successfully
2024-05-13 20:08:08,557:       restart_service() : INFO     : Restarting service: apache2
2024-05-13 20:08:08,558:               run_cmd() : INFO     : Running OS cmd: sshpass -p <censored> ssh root@3.89.242.163 'service apache2 restart'
2024-05-13 20:08:09,746:           run_ssh_cmd() : INFO     : Executed command sshpass -p <censored> ssh root@3.89.242.163 'service apache2 restart' successfully
```
