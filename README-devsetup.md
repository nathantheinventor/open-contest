# Development Setup

1. Follow [installation instructions](README.md) to install open-contest in a Linux
   or Mac environment. Create the db folder in your home directory.

1. Clone this project (recommended location: your home directory).

1. Edit open-contest/test.sh and update the OC_CODE_DIR variable to point to the
   location of the source code if you placed it somewhere other than your home directory.

1. To start the contest server running using your development source code, execute
   ```
   bash ~/open-contest/test.sh
   ```

   Review the Admin credentials in the output. Then, point your browser to port 8000
   and login using the credentials.

1. Make changes to files in open-contest/src/main as needed, then press
   Ctrl-C in the console and re-execute the bash command above to restart the
   server and test the changes.

# Working with Visual Studio Code

Visual Studio Code includes excellent Python support. After installing the
Python extension, to enable improved code browsing, execute the following to
create a soft link named "code" that points to your main Python source code
folder (the below assumes that open-contest is installed in your home
directory):

```
ln -s ~/open-contest/src/main/ ~/code
```

Then, use the following command to start Visual Studio Code:

```
PYTHONPATH=~ code ~/open-contest
```
