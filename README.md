# dockerauto
*Automation, notes and management for Docker images*

---

## Introduction
This tool is a python wrapper around Docker to help solve some of the annoyances of managing lots of images for running tools and services.  

It provides a way to install and build images from a variety of sources, to stores notes on tool syntax, to save a base command for each tool (so you don't have to remember all the volumes and ports you need to map), and allows you to update or remove images singly or in bulk.

---

## Dependencies
***dockerauto*** is written to be used on a Linux machine, but is customised to run also on WSL (Windows Subsystem for Linux) - versions 1 or 2.  
It requires the following to be installed:
*  Python3
*  Git
*  Docker

On an apt-based system these can be installed be simply running:  
`sudo apt install python3.10 git docker.io -y`

---

## Installation
To install simply git clone this repo and then run the install command.

```
git clone https://github.com/ticarpi/dockerauto
cd dockerauto
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





