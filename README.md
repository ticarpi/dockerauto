![image](https://github.com/ticarpi/dockerauto/assets/19988419/a63c89da-3834-4443-9cdb-ee84539d532b)

*Automation, notes and management for Docker images*

## Introduction
This tool is a python wrapper around Docker to help solve some of the annoyances of managing lots of images for running tools and services.  

It provides a way to install and build images from a variety of sources, to stores notes on tool syntax, to save a base command for each tool (so you don't have to remember all the volumes and ports you need to map), and allows you to update or remove images singly or in bulk.

---

## Prerequisites
***dockerauto*** is written to be used on a Linux machine, but is customised to run also on WSL (Windows Subsystem for Linux) - versions 1 or 2.  
It requires the following to be installed:
*  Python3
*  Git
*  Docker

On an apt-based system these can be installed be simply running:  
`sudo apt install python3.10 git docker.io -y`

Also set your user to be able to run `docker` without sudo:
`sudo usermod -aG docker $USER`


### Windows installation
For Windows you will need the WSL components to be set up and a working WSL distrobution installed.  
This is a task I leave up to the reader, however on most modern systems this is simply a case of running the following:  
*  `wsl --install` (then reboot if necessary)
*  `wsl --install -d ubuntu` (for example)

To install dependencies run:  
`sudo apt install python3.10 git -y`

Then download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/) for Windows.  
Reboot your system again and you should be good to go.

---

## Installation
To install simply `git clone` this repo and then run the dockerauto `install` command.

```
git clone https://github.com/ticarpi/dockerauto
cd dockerauto/
python3 ./dockerauto.py install
```

As part of the installation ***dockerauto*** will:
*  add `dockerauto` command to your $PATH, so it can be run from anywhere on your system
*  create a base directory in your $HOME path (`~/.dockerauto/`)
*  copy a config file to the base directory

### Configuration files
When you install ***dockerauto*** it will set the default 'example' config file, with a few suggested images. Optionally you can specify a different file, either from a URL or locally on your filesystem.  
Some additional configs are included with ***dockerauto*** (named `[technology type].dockerlist.json`).  
Or alternatively you can modify an example list manually.  

To import a config run:  
`dockerauto install -c [path/URL to the file]`

---

## Running dockerauto
Once installed you can run:  
`dockerauto [mode] [OPTIONS]`

The modes are:  
Mode | Function
-|-
`list` | List all dockerauto items in the configfile
`info [dockeritem]` | Show the command, metadata and notes about the specified dockerauto item 
`run [dockeritem] [arguments]` | Run a docker container for the specified dockerauto item and provided arguments
`update [dockeritem/ALL]` | Pull a fresh DockerHub image, Git clone, download, or build a new image based on the configfile info
`shell [dockeritem]` | Run a basic shell within the container for troubleshooting, identifying file paths, or other manual tasks
`unload [dockeritem/ALL]` | Remove the docker image for the specified dockerauto item (for disk management, and purging broken images)
`add [dockeritem] [-d/-dc FILE]` | Add a new entry in the configfile for a tool - guided
`remove [dockeritem/ALL]` | Remove an entry in the configfile for the specified tool 
`install [-c CONFIGFILE]` | Initial setup, and to add alternative configfiles
`export` | Export the configfile to the current directory

---

### Example usage

LIST:  
`dockerauto list`

INFO with arguments:  
`dockerauto info myapp`

RUN with arguments:  
`dockerauto run myapp '-u https://example.com --title "text with spaces" -o /tmp/examplereport.txt'`

UPDATE:  
`dockerauto update myapp`

SHELL:  
`dockerauto shell myapp`

UNLOAD:  
`dockerauto unload myapp`

ADD with arguments:  
`dockerauto add newapp -d Dockerfile`

REMOVE:  
`dockerauto remove newapp`

INSTALL (local configfile):  
`dockerauto install -c CONFIGFILE`

INSTALL (online configfile):  
`dockerauto install -c https://gist.github.com/ticarpi/CONFIGFILE`

EXPORT:  
`dockerauto export`


### How to run from a specific directory in Windows?
If using Windows you can:
*  Open a directory in Explorer
*  Click into any open space in the window
*  Hit `Ctrl+Shift, Right-Click` to get the Advanced context menu.
*  Choose `Open Linux shell here`

From here you can install and run ***dockerauto***

---

## Quirks
If you want to run a container and call its Help function you may get a conflict with ***dockerauto***'s Help function.  
To avoid this add a space before the help option argument:  
`dockerauto run myapp ' -h'`
