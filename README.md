# Django Snippet - Customermodel & Authentication

### Global Setup (Python Installation)
*Windows Installation*

**1. To run a Python or Django project, you first of all need to download and install Python. The Python download requires about 30MB of disk space. Follow this link [here](https://www.python.org/downloads/) to download Python.**


**2. Underneath the heading at the top that says `Python Releases for Windows`, click on the link for the `Latest Python 3 Release - Python 3.x.x`.**


**3. Scroll to the bottom and select either `Windows x64 executable installer` for 64-bit or `Windows x86 executable installer` for 32-bit.**


**4. Once you have chosen and downloaded an installer, simply run it by double-clicking on the `downloaded file`.**


>**Important:** You want to be sure to check the box that says **Add Python 3.x to PATH** as shown to ensure that the interpreter will be placed in your execution path.


**5. Then just click `Install Now`. That should be all there is to it. A few minutes later you should have a working Python 3 installation on your system.**


*Linux/MacOS Installation*

**1. There is a very good chance your Linux distribution has Python installed already, but it probably wonâ€™t be the latest version, and it may be Python 2 instead of Python 3.**

>To find out what version(s) you have, open a terminal window and try the following commands:

```
python --version
python2 --version
python3 --version
```
>One or more of these commands should respond with a version, as below:

```
$ python3 --version
Python 3.6.5
```

### Project Setup
**1. Whenever you are starting a new Django project, it's a good idea to first set up your development environment. Create a new directory for your project to live in, and navigate into it. In shell:**

>1.1 Ubuntu / MacOS / Windows

```
$ mkdir <folder_name>
```
 
**2. Move into the project root directory.**
 
```
cd <folder_name>
```
**3. Clone the project from the GitBucket repository.**
>Open an interactive terminal, preferably [**Git Bash**](https://git-scm.com/downloads)
```
$ git clone https://bitbucket.org/getinnotized_GH/cp-be/src/master/
``` 

**4. A [virtual environment](https://docs.python.org/3/tutorial/venv.html) is recommended. See the [setup information](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).**
 
 
**5. Create and start your virtual environment. Inside the new directory you created for your project, run the commands below:**
 
5.1. Ubuntu / MacOS
```
python3 -m venv venv
source venv/bin/activate
```
 >**Note:** If you don't use a virtual environment on Ubuntu or MacOS, you will need to specify your python or pip version at every of the following steps
 
5.2. Windows

```
pip install virtualenv
source\venv\Scripts\activate.bat
```

>Where **source** is the absolute path to the **venv directory**

**4. Update pip**
>For Windows

```
pip install --upgrade pip
```

>For MacOS/Ubuntu

```
$ sudo pip install --upgrade pip
```

 
**5. Install all of the Requirements. The `requirements.txt` file contains all packages needed to run this project. Instead of running the individual commands one after the other, Python provides a very easy way of getting all packages installed without stress. Just a line of code and we are good!**

```
pip install -r requirements.txt
```
 >After this step all packages required for the project are installed. Among them especially Django, Django RestFramework, Django Corsheaders and dotenv.
 
 
**6. This Project is using a .env file for API-Keys and some individual configurations. The command below makes a copy of the `.env.example` and names it `.env`. This environment file contains very sensitive information and must not be altered unless absolutely necessary.**

```
cp .env.example .env
```
 
6.1. **SECRET_KEY** 

>Don't use the given Secret Key for production! Regenerate it and replace it. You can simply regenerate the key by using some [webservices](https://djecrety.ir). If you are working locally for development you can use the example key.


**7. Migrate the Database.** 

>This creates a database for the project where all current and future data are stored.

```
python manage.py migrate
```


**8. Create a Superuser, in other words, an admin of the project.**
 
```
python manage.py createsuperuser
```
 
 
**9. To get the project running, the server needs to be started. Use the command below to start the Server:**

```
python manage.py runserver
```


**Congratulations. If you do not get an error, everything works fine and you are done with the server side setup**
