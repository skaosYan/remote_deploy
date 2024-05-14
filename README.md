# remote_deploy
Simple remote deployment tool  

# Notes
For security reasons, it is a good practice not to use root access, some other user should be used and sudo privilege granted. But for the sake of simplicity I use root.  
For security reasons, it is a good practice not to store password in the code, so program will ask for password.  
For security reasons, files are allowed to be installed only to ONE remote folder, which is web root, ALLOWED_DIR=/var/www/html/  
For security reasons, root password is redacted from log, password replaced with the keyword <censored> :)

For simplicity, creation of remote directories is not supported. Only remote files installation is supported as required.  

# Configuration



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
