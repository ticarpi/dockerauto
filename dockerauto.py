#!/usr/bin/env python3
#
# DockerAuto version 0.5 (13_10_2023)
# Written by Andy Tyler (@ticarpi)
# Please use responsibly...
# Software URL: https://github.com/ticarpi/dockerauto
# Web: https://www.ticarpi.com
# Twitter: @ticarpi

dockerautovers = "0.5"
import os
from urllib.request import urlretrieve
#import subprocess
#import re
import json
import argparse
#from datetime import datetime
import shutil

configfile = os.path.expanduser('~/dockerlist.json')

def run_update(dockerlist_json, updateitem):
    try:
        print("\n[+] Running docker update command for "+updateitem)
        if powershellcmd:
            cmd = powershellcmd+' -c \''+dockerlist_json['dockeritems'][updateitem][3]+'\''
        else:
            cmd = dockerlist_json['dockeritems'][updateitem][3]
        os.system(cmd)
    except:
        print('[-] The specified tool ('+updateitem+') could not be updated')

def mode_update(dockeritem):
    with open(configfile, "r") as dockerlist:
        dockerlist_json = json.load(dockerlist)
    if dockeritem == 'ALL' or dockeritem == 'all':
        print("[+] Updating all of the following:")
        for key in dockerlist_json['dockeritems'].keys():
            print("    [*] "+key)
        update = input('\n[!] Are you sure you want to update all Docker images? (y/N)')
        if update=='y' or update=='Y':
            for key in dockerlist_json['dockeritems'].keys():
                run_update(dockerlist_json, key)
        else:
            print('Quitting...')
            exit(1)
    else:
        print('[+] Updating '+dockeritem)
        run_update(dockerlist_json, dockeritem)

def run_remove(dockerlist_json, removeitem):
    print("\n[+] Removing config entry for "+removeitem)
    del dockerlist_json['dockeritems'][removeitem]
    with open(configfile, "w") as dockerdump:
        dockerdump.write(json.dumps(dockerlist_json))
        print('\n[+] '+removeitem+' has been removed from the config')

def mode_remove(dockeritem):
    with open(configfile, "r") as dockerlist:
        dockerlist_json = json.load(dockerlist)
    if dockeritem in dockerlist_json['dockeritems'].keys():
        print('[+] Removing '+dockeritem+' from the config:')
        remove = input('\n[!] Are you sure you want to remove this item? (y/N)')
        if remove=='y' or remove=='Y':
            run_remove(dockerlist_json, dockeritem)
        else:
            print('Quitting...')
            exit(1)
    else:
        print("The specified tool ("+dockeritem+") is not in the config file. Try one of the following:")
        for key in dockerlist_json['dockeritems'].keys():
            print("    [*] "+key)

def mode_run(dockeritem, args):
    with open(configfile, "r") as dockerlist:
        dockerlist_json = json.load(dockerlist)
    try:
        print("[+] Running docker command for "+dockeritem)
        if powershellcmd:
            cmd = powershellcmd+' -c \''+dockerlist_json['dockeritems'][dockeritem][1]+' '+args+'\''
        else:
            cmd = dockerlist_json['dockeritems'][dockeritem][1]+' '+args
        os.system(cmd)
    except:
        print("The specified tool ("+dockeritem+") could not be run. Try one of the following:")
        for key in dockerlist_json['dockeritems'].keys():
            print("    [*] "+key)

def unload_image(dockeritem, dockerlist_json):
    print(dockerlist_json['dockeritems'][dockeritem][3])
    try:
        if powershellcmd:
            cmd = powershellcmd+' -c \'docker image rm '+dockerlist_json['dockeritems'][dockeritem][3]+'\''
        else:
            cmd = 'docker images --format json'
        os.system(cmd)
    except:
        print("[!] ERROR processing the specified tool ("+dockeritem+").")

def mode_unload(dockeritem):
    with open(configfile, "r") as dockerlist:
        dockerlist_json = json.load(dockerlist)
    if dockeritem == 'ALL' or dockeritem == 'all':
        print("[+] Unloading all of the following Docker images:")
        for key in dockerlist_json['dockeritems'].keys():
            print("    [*] "+key+' ('+dockerlist_json['dockeritems'][key][3]+')')
        update = input('\n[!] Are you sure you want to unload all Docker images? (y/N)')
        if update=='y' or update=='Y':
            for key in dockerlist_json['dockeritems'].keys():
                unload_image(key, dockerlist_json)
        else:
            print('Quitting...')
            exit(1)
    if dockeritem in dockerlist_json['dockeritems']:
        unload_image(dockeritem, dockerlist_json)
    elif dockeritem != 'ALL' and dockeritem != 'all':
        print("The specified tool ("+dockeritem+") is not in the config file. Try one of the following:")
        for key in dockerlist_json['dockeritems'].keys():
            print("    [*] "+key)


def buildscript(repourl):
    print('[+] Building Dockerfile generation script\n')
    genscr = ''
    if 'github.com' in repourl:
        print('[+] Detected GitHub repo, cloning...\n')
        split = repourl.rstrip('/').split('/')
        imgname = ['GitHub', split[-1]]
    else:
        imgname = ['Dockerfile', input('\n[*] Please enter the image name with no spaces(e.g. jwt_tool)\n')
    print('[!] Script generation function not yet ready')
    # TODO
    return genscr, imgname

def file2echo(inputfile):
    #TODO
    return echooutput


def mode_add(dockeritem, dockerfile, configfile):
    print('\n[+] Creating entry for new DockerAuto item: '+dockeritem)
    newitem = ["","","",[],"",""]
    newitem[5] = ''
    newitem[0] = input('\n[*] Please enter a short description of the image\n')
    with open(configfile, "r") as dockerlist:
        dockerlist_json = json.load(dockerlist)
    if dockerfile:
        option = input('[*] Select which method you want to use to generate your Docker content:\n    [1] Clone a GitHub repo\n    [2] Download a zip\n    [3] No codebase to import.\n')
        if option == '1':
            repourl = 'https://www.github.com/'+input('\n[*] Please enter the "user/name" of the GitHub repo for cloning (e.g. ticarpi/jwt_tool)\n')
        elif option == '2':
            zipurl = input('\n    [*] Please enter the URL of the zipfile you wish to download\n')
            zipdir = input('\n    [*] Please enter a directory name that the files are within in the zip file (or leave blank if no zip subdirectory)\n')
        elif option == '3':
            zipurl = input('\n    [*] Please enter the URL of the zipfile you wish to download\n')
        else:
            print('Not a valid option. Quitting...')
            exit(1)
        genscr, imgname = buildscript(repourl)
        newitem[3] = imgname
        newitem[4] = genscr
    else:
        newitem[4] = ''
        newitem[3] = ['DockerHub', input('\n[*] Please enter the DockerHub repo (e.g. ticarpi/jwt_tool)\n')]
    newitem[1] = input('\n[*] Please enter the base command used to run this container. e.g. docker run -it --network \"host\" --rm -v \"${PWD}:/tmp\" -v \"${HOME}/.jwt_tool:/root/.jwt_tool\" ticarpi/jwt_tool\n    Include the following:\n    [*] volume mapping "-v"\n    [*] port mapping "-p"\n    [*] environment variables "-e"\n    [*] Remove instruction "--rm"\n    [*] and make sure the image referenced is: '+newitem[3]+'\n')
    newitem[2] = input('\n[*] Please enter any useful notes for running the container, separating each note with a semicolon. e.g. "-h; PWD mapped to /tmp"\n')
    dockerlist_json['dockeritems'][dockeritem] = newitem
    with open(configfile, "w") as dockerdump:
        dockerdump.write(json.dumps(dockerlist_json))
        print('\n[+] new item ('+dockeritem+') has been added to the config')

def mode_info(dockeritem):
    with open(configfile, "r") as dockerlist:
        dockerlist_json = json.load(dockerlist)
    if dockeritem in dockerlist_json['dockeritems']:
        try:
            print("[+] Info for: "+dockeritem+" (Last updated: "+dockerlist_json['dockeritems'][dockeritem][5]+")")
            print("    [*] Description: "+dockerlist_json['dockeritems'][dockeritem][0])
            print("    [*] Usage Notes:\n        [*] "+dockerlist_json['dockeritems'][dockeritem][2].replace(';','\n        [*] '))
            print("    [*] Command: "+dockerlist_json['dockeritems'][dockeritem][1])
            print("    [*] Image Name: "+str(dockerlist_json['dockeritems'][dockeritem][3]))
            print("    [*] Dockerfile Generation Script: "+dockerlist_json['dockeritems'][dockeritem][4])
        except:
            print("ERROR processing the specified tool ("+dockeritem+").")
    else:
        print("The specified tool ("+dockeritem+") is not in the config file. Try one of the following:")
        for key in dockerlist_json['dockeritems'].keys():
            print("    [*] "+key)

def mode_list():
    with open(configfile, "r") as dockerlist:
        dockerlist_json = json.load(dockerlist)
        imagelist = checkimage()
        print('[+] Images in config:')
        for key in dockerlist_json['dockeritems'].keys():
            installed = ' - not installed'
            imgname = dockerlist_json['dockeritems'][key][3]
            if imgname in imagelist:
                installed = ' - INSTALLED ('+imgname+')'
            print("    [*] "+key+installed)

def saveconfig(sourcefile, destfile):
    print('\n[+] Saving config\nfrom: '+sourcefile+'\nto: '+destfile+'\n')
    try:
        shutil.copy2(sourcefile, destfile)
    except:
        print('Copy failed, check permissions on source and destination files:\nSource:'+sourcefile+'\nDestination: '+destfile)

def downloadfile(URL, filename):
    urlretrieve(URL, filename)

def checkimage():
    if powershellcmd:
        cmd = powershellcmd+' -c \'docker images --format json\''
    else:
        cmd = 'docker images --format json'
    images = os.popen(cmd).readlines()
    imagelist = []
    for image in images:
        img = json.loads(image)
        imagelist.append(img['Repository']+':'+img['Tag'])
    return imagelist

def mode_export():
    saveconfig(configfile, os.getcwd()+'/EXPORT.dockerlist.json')

def mode_install(json):
    if shutil.which('dockerauto') is None:
        os.system('sudo ln -s '+os.getcwd()+'/dockerauto.py /usr/bin/dockerauto')
        print('[+] DockerAuto now installed via simlink to /usr/bin/dockerauto, you can now run with:\n$ dockerauto [args]')
    if json.startswith('http://') or json.startswith('https://'):
        downloadfile(json, 'temp.json')
        json = 'temp.json'
    if not os.path.exists(json):
        print('[!] Cannot find '+json+' check the filepath')
        exit(1)
    if os.path.exists(configfile):
        overwrite = input('[!] DockerAuto config at '+configfile+' already exists.\nDo you want to overwrite this? (y/N)')
        if overwrite=='y' or overwrite=='Y':
            jsonfile=os.getcwd()+'/'+json
            saveconfig(jsonfile, configfile)
        else:
            print('Quitting...')
            exit(1)
    else:
        saveconfig(json)
        
def checkwsl():
    powershellcmd = ''
    if os.environ.get('WSL_DISTRO_NAME'):
        print('[+] WSL detected, checking for PowerShell path...')
        for path in ['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '/mnt/c/Windows/SysWOW64/WindowsPowerShell/v1.0/powershell.exe']:
                if os.path.exists(path):
                    powershellcmd = path
                    break
    
    if powershellcmd:
        print('    [*] PowerShell path: '+powershellcmd+'\n')
    else:
        print("[-] PowerShell couldn't be found, trying with WSL2 Docker instead.\n")
    return powershellcmd

def checkdeps():
    errors=0
    if shutil.which('docker') is None and not powershellcmd:
        print('[-] Docker NOT installed.\nThis is a requirement for a tool that runs Docker containers.\n\nOn Kali and other Linux distros that use the APT package manager you can install this and configure it by running the following command:\nsudo apt update && sudo apt install docker.io -y && sudo usermod -aG docker $USER\n')
        errors+=1
    if shutil.which('git') is None:
        print('[-] Git NOT installed.\nThis is a requirement in order to update and pull Git repos to build new Docker containers.\n\nOn Kali and other Linux distros that use the APT package manager you can install this by running the following command:\nsudo apt update && sudo apt install git -y\n')
        errors+=1
    if errors>0:
        exit(1)


#logo = "\t[DockerAuto Logo_Not_Found]\n@ticarpi\t\tversion "+dockerautovers+"\n"
logo="\n██████   ██████   ██████ ██   ██ ███████ ██████   █████  ██    ██ ████████  ██████  \n"
logo+="██   ██ ██    ██ ██      ██  ██  ██      ██   ██ ██   ██ ██    ██    ██    ██    ██ \n"
logo+="██   ██ ██    ██ ██      █████   █████   ██████  ███████ ██    ██    ██    ██    ██ \n"
logo+="██   ██ ██    ██ ██      ██  ██  ██      ██   ██ ██   ██ ██    ██    ██    ██    ██ \n"
logo+="██████   ██████   ██████ ██   ██ ███████ ██   ██ ██   ██  ██████     ██     ██████  \n"
logo+="\t@ticarpi\t\t\t\t\t\tversion "+dockerautovers+"\n"

if __name__ == '__main__':
    print(logo)
    powershellcmd = checkwsl()
    checkdeps()
    parser = argparse.ArgumentParser(epilog="OK, bye", formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='mode',required=True)
    parser_install = subparsers.add_parser('install', help="Install a new config file (and set up symlink to run DockerAuto from any directory)")
    parser_run = subparsers.add_parser('run', help="Run Docker commands for DockerAuto items")
    parser_list = subparsers.add_parser('list', help="Show all DockerAuto items in the config (and install status)")
    parser_info = subparsers.add_parser('info', help="Look up info about each DockerAuto item in the config")
    parser_add = subparsers.add_parser('add', help="Add new DockerAuto items to the config manually")
    parser_remove = subparsers.add_parser('remove', help="Remove DockerAuto items from the config manually")
    parser_update = subparsers.add_parser('update', help="Pull any new Docker image updates for DockerAuto items in the config - or for everything (update ALL)")
    parser_unload = subparsers.add_parser('unload', help="Delete stored Docker images for DockerAuto items in the config - or for everything (unload ALL)")
    parser_export = subparsers.add_parser('export', help="Export the config file")
    parser_add.add_argument('dockeritem', type=str, action="store", help="A new DockerAuto item", default='dockerauto')
    parser_add.add_argument('-d', '--dockerfile', action="store", help="Dockerfile for the new DockerAuto item")
    parser_run.add_argument('dockeritem', type=str, action="store", help="Run the selected DockerAuto items", default='dockerauto')
    parser_update.add_argument('dockeritem', type=str, action="store", help="Update the selected DockerAuto items (or 'update ALL' to update all Docker images)", default='ALL')
    parser_unload.add_argument('dockeritem', type=str, action="store", help="Unload the selected DockerAuto item to the config", default='ALL')
    parser_remove.add_argument('dockeritem', type=str, action="store", help="Remove the selected DockerAuto item from the config", default='ALL')
    parser_run.add_argument("-a", "--args", action="store", help="Arguments to use in the docker command (surround in 'single quotes' e.g. -a='--help')", required=False, default='')
    parser_info.add_argument('dockeritem', type=str, action="store", help="Info about selected DockerAuto items", default='dockerauto')
    parser_install.add_argument("-j", "--json", action="store", help="URL or local filepath to grab your custom DockerAuto config from", required=False, default='example.dockerlist.json')
    args = parser.parse_args()
    if not os.path.exists(configfile) and args.mode != 'install':
        print('Install config before you can use any other DockerAuto functionality:\n$ python3 dockerauto.py install -j [Path/URL to dockerlist.json]')
        exit(1)
    if args.mode == 'install':
        mode_install(args.json)
    elif args.mode == 'info':
        mode_info(args.dockeritem)
    elif args.mode == 'update':
        mode_update(args.dockeritem)
    elif args.mode == 'unload':
        mode_unload(args.dockeritem)
    elif args.mode == 'remove':
        mode_remove(args.dockeritem)
    elif args.mode == 'list':
        mode_list()
    elif args.mode == 'export':
        mode_export()
    elif args.mode == 'run':
        mode_run(args.dockeritem, args.args)
    elif args.mode == 'add':
        mode_add(args.dockeritem, args.dockerfile, configfile)
