# Development Setup

The following instructions have been tested in an Ubuntu 18.04 environment.

1. Install Docker:
   ```
   sudo apt install docker.io
   ```

1. Execute the following to add the current user to the docker group
   so that docker commands can be executed without using sudo:
   ```
   sudo usermod -a -G docker $USER
   ```
   Logout, then login to make the change take effect.

1. Clone this project (recommended location: your home directory).
   ```
   git clone https://github.com/bjucps/open-contest ~/open-contest
   ```

1. Create the Docker images needed for development:
   ```
   docker build -t bjucps/open-contest ~/open-contest/opencontest
   cd ~/open-contest/contest/runners
   bash build.sh
   ```

1. Optionally copy the sample contest database to your home directory
   to use for testing:
   ```
   cp -r ~/open-contest/test/db ~
   ```

1. To start the contest server running, execute
   ```
   ~/open-contest/launch.sh --dev -p 8000 --fg --log-stdout 
   ```
   See "The launch script" below for details on the options.

   Review the Admin credentials in the output:
   ```
   Admin username is "Admin".
   Admin password is "...".
   ```
   Then, point your browser to port 8000 and login using the credentials. 

1. Make changes to files in open-contest/opencontest as needed, then press
   Ctrl-C in the console and re-execute the bash command above to restart the
   server and test the changes.
   
# The launch script

The launch script provides the following command line options:

* `--db` *database-directory* specifies the location of the local database directory.
   If the directory does not exist, it is created.

* `--dev` overrides the open-contest code in the Docker container with the code in the
  local open-contest folder

* `--fg` runs the container in the foreground, allowing it to be shutdown with a Ctrl-C.
  The default is to run the container in the background. To shut down the container
  when run in the background, use **docker ps** to determine the name of the container, 
  then **docker kill *container-name***

* `--log-stdout` sends logging output from open-contest to stdout instead of to
  the open-contest.log file in the database directory

* `--log-debug` includes DEBUG-level logging in the log output

* `--log-all-requests` outputs an entry in the log file for every HTTP request to the
  open-contest application. Since this results in a lot of log data, by default, HTTP requests are not logged.

* `-p` *port* specifies the port number for the open-contest server (default: 80)

* `--local-only` specifies that only browsers running on localhost can connect to the open-contest server

# Working in PyCharm
PyCharm Professional provides out-of-the-box Django support, but PyCharm Community 
may also be used. After opening the project in PyCharm Community, mark the project
directory (named "opencontest") as project root. This configuration will allow
PyCharm to find things within Django's directory structure. 


# Working with Visual Studio Code

Visual Studio Code includes excellent Python support. 

To setup Visual Studio Code, install the Microsoft Python extension, then choose
**File > Open Folder** and select the open-contest/opencontest folder.
