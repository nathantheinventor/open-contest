# Development Setup

1. Follow [installation instructions](README.md) to install open-contest in a Linux
   or Mac environment. Create the db folder in your home directory.

1. Clone this project (recommended location: your home directory).
   ```
   cd ~
   git clone https://github.com/bjucps/open-contest
   ```

1. If you have not already done so, create an empty db directory to hold the
   contest database files.
   ```
   mkdir ~/db
   ~~~

1. To start the contest server running using your development source code, execute
   ```
   bash ~/open-contest/dev.sh [ <path-to-db-directory> ]
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


# Working with Visual Studio Code (NOT TESTED)

Visual Studio Code includes excellent Python support. 

To setup Visual Studio Code, install the Microsoft Python extension, then choose
**File > Open Folder** and select the open-contest/opencontest folder.
