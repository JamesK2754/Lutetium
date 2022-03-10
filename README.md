
# Lutetium

Lutetium allows for the remote download of files, videos, and more, scheduled nightly and managed by a MYSQL database. 

Lu consists of two main parts: server and client.

### SERVER
For Lutetium to work it requires a running server. For the JamesDev instance, this server is a Raspberry Pi model B+ running Debian 11 Lite - so by no means does the server need to be powerful. The server manages the MYSQL database that records the download information and, most importantly, is the location the downloads are executed and stored on. All downloads are made using bash terminal commands (wget and YouTube-dl) and are stored in the media subdirectory of the Lu install.

### CLIENT
There are two client experiences provided: a core, command line based terminal and a GUI interface built using Tkinter. The decision of which is completely up to the user for whatever meets their need. 
|Experience| Files |
|--|--|
| Command line |  Lutetium.py|
| GUI | LutetiumApp.py + Lutetium.py



**Note:** Development is mostly focused on the GUI experience found in LutetiumApp.py and so will be the most feature rich.

### Server installation
Requirements:
 - OS with:
	 - bash 
	 -  crontab
 - System packages:
	 - wget
	 - Youtube-DL (ffmpeg or alternative is required for file conversions)
	 - Python3.10 or greater installed to bin
	 - PIP
	 - MYSQL or mariaDB
 - PIP:
	 - mysql.connector
 - Other:
	 - A SMTP mail account

### Client installation (from source)
For installations with an executable file these steps are not required.
Requirements:
 - OS:
	 - Linux
	 - Darwin (macOS)
	 - Windows
 - System packages:
	 - Python3.10 or greater
	 - PIP
 - PIP:
	 - mysql.connector
	 - yourls
	 - Tkinter Pillow
