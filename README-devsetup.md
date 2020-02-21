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

1. Create the Docker image needed for development:
   ```
   docker build -t bjucps/open-contest ~/open-contest/opencontest
   ```

1. Optionally copy the sample contest database to your home directory
   to use for testing:
   ```
   cp -r ~/open-contest/test/db ~
   ```

1. To start the contest server running, execute
   ```
   ~/open-contest/launch.sh -dev -p 8000 -d ~/db --log-stdout --log-debug --log-all-requests
   ```

   Review the Admin credentials in the output:
   ```
   Admin username is "Admin".
   Admin password is "...".
   ```
   Then, point your browser to port 8000 and login using the credentials. 

1. Make changes to files in open-contest/opencontest as needed, then press
   Ctrl-C in the console and re-execute the bash command above to restart the
   server and test the changes.
   
# Working in PyCharm
PyCharm Professional provides out-of-the-box Django support, but PyCharm Community 
may also be used. After opening the project in PyCharm Community, mark the project
directory (named "opencontest") as project root. This configuration will allow
PyCharm to find things within Django's directory structure. 


# Working with Visual Studio Code

Visual Studio Code includes excellent Python support. 

To setup Visual Studio Code, install the Microsoft Python extension, then choose
**File > Open Folder** and select the open-contest/opencontest folder.
