import getpass
import json
import logging
import os
import subprocess
from typing import Tuple


# TODO: user password can't be stored in a plain form,
# needs to be moved to a secret
USER_NAME           = "root"
CONFIG_FILE         = "configuration.json"
ALLOWED_DIR         = "/var/www/html/"
ROOT_DIR            = os.path.dirname(os.path.abspath(__file__))
FILES_REPO_DIR      = ROOT_DIR+"/files2deploy/"

REMOTE_SSH          = "sshpass -p {} ssh " + USER_NAME + "@{} "
RESTART_SERVICE     = "service {} restart"
REMOVE_RPM          = "apt remove {} -y"
INSTALL_RPM         = "apt install {} -y"

INSTALL_FILE        = "sshpass -p {} scp " + FILES_REPO_DIR + "{} " + USER_NAME + "@{}:" + ALLOWED_DIR
INSTALL_FILE_OWNER  = "chown {} " + ALLOWED_DIR + "{}"
INSTALL_FILE_GROUP  = "chgrp {} " + ALLOWED_DIR + "{}"
INSTALL_FILE_MODE   = "chmod {} " + ALLOWED_DIR + "{}"

logging.basicConfig(
                    filename='remote.log',
                    filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s:  %(funcName)20s() : %(levelname)-8s : %(message)s')


class RemoteExecutor:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.json_config = None

    def redact_password(self, cmd):
        return cmd.replace(self.password, '<censored>')

    # function executes a constructed remote command: SSH + OS command
    def run_cmd(self, cmd) -> Tuple[int, str]:
        logging.info('Running OS cmd: %s', self.redact_password(cmd))
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            output = proc.communicate()[0].strip().decode()
            res = proc.returncode
        except Exception as e:
            logging.error('Error while running remote cmd %s: %s', cmd, repr(e))
            res = -1
        return res, output

    # function constructs a remote command: SSH + OS command
    def run_ssh_cmd(self, cmd) -> Tuple[int, str]:
        cmd = REMOTE_SSH.format(self.password,self.hostname) + "'" + cmd + "'"
        res = self.run_cmd(cmd)
        if res[0] == 0:
            logging.info('Executed command %s successfully', self.redact_password(cmd))
        else:
            logging.error('Failed to run command %s, error: %s' , self.redact_password(cmd), res[1])
        return res

    # function restarts a remote Linux service
    def restart_service(self, service_name) -> Tuple[int, str]:
        logging.info('Restarting service: %s', service_name)
        res = self.run_ssh_cmd(RESTART_SERVICE.format(service_name))
        return res

    # function installs a remote package
    def install_rpm(self, package_name) -> Tuple[int, str]:
        logging.info('Installing OS package: %s', package_name)
        res = self.run_ssh_cmd(INSTALL_RPM.format(package_name))
        return res

    # function removes a remote package
    def remove_rpm(self, package_name) -> Tuple[int, str]:
        logging.info('Removing OS package: %s', package_name)
        res = self.run_ssh_cmd(REMOVE_RPM.format(package_name))
        return res

    # function installs a remote file and it's attributes
    def install_file(self, filename, owner, group, mode):
        logging.info('Installing file: %s to %s', filename, ALLOWED_DIR)

        cmd = INSTALL_FILE.format(self.password, filename, self.hostname)
        res = self.run_cmd(cmd)
        if res[0] == 0:
            logging.info('Installing file owner: %s, for %s', owner, filename)
            res = self.run_ssh_cmd(INSTALL_FILE_OWNER.format(owner, filename))

            logging.info('Installing group owner: %s for %s', group, filename)
            res = self.run_ssh_cmd(INSTALL_FILE_GROUP.format(group, filename))

            logging.info('Installing file mode: %s for file %s', mode, filename )
            res = self.run_ssh_cmd(INSTALL_FILE_MODE.format(mode, filename))
        else:
            logging.error('Failed to install file, skipping file attributes: %s. Error %s', filename, res[1])


class Control:
    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        self.read_configuration()


    # function loads deployment configuraiton from json file
    def read_configuration(self):
        logging.info('Reading deployment configuration')

        try:
            with open(self.config_file_name, 'r') as f:
                self.json_config = json.load(f)
        except Exception as e:
            logging.critical('Read configuration error %s', repr(e))
            quit()

        try:
            self.password = getpass.getpass(prompt=f"Enter password for user {USER_NAME} :")
        except Exception as error:
            logging.critical(f"Failed to get password for {USER_NAME} ")
            quit()

    def install(self):
        logging.info('Applying changes to remote hosts')

        for _host in self.json_config['hosts']:
            executor = RemoteExecutor(hostname=_host['hostname'], username=USER_NAME, password=self.password)

            # process all configured packages
            for _package in self.json_config['packages']:
                if _package['deploy_mode'] == 'install':
                    executor.install_rpm(_package['package_name'])
                elif _package['deploy_mode'] == 'remove':
                    executor.remove_rpm(_package['package_name'])
                else:
                    logging.info('Wrong deployment mode: %s for package %s', _package['deploy_mode'], _package['package_name'])

            # process all configured files
            for _file in self.json_config['files']:
                executor.install_file(_file['filename'], _file['owner'], _file['group'], _file['mode'])

            # as a very last step restart required services
            for _service in self.json_config['restarts']:
                executor.restart_service(_service['service_name'])


if __name__ == "__main__":
    control = Control(CONFIG_FILE)
    control.install()
