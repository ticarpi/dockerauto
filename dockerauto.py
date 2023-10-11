#!/usr/bin/env python3
#
# DockerAuto version 0.3 (11_10_2023)
# Written by Andy Tyler (@ticarpi)
# Please use responsibly...
# Software URL: https://github.com/ticarpi/dockerauto
# Web: https://www.ticarpi.com
# Twitter: @ticarpi

dockerautovers = "0.3"
import os
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
            cmd = powershellcmd+'-c \''+dockerlist_json['dockeritems'][updateitem][3]+'\''
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
        update = input('\n[-] Are you sure you want to update all Docker images? (y/N)')
        if update=='y' or update=='Y':
            for key in dockerlist_json['dockeritems'].keys():
                run_update(dockerlist_json, key)
        else:
            print('Quitting...')
            exit(1)
    else:
        print('[+] Updating '+dockeritem)
        run_update(dockerlist_json, dockeritem)

def mode_run(dockeritem, args):
    with open(configfile, "r") as dockerlist:
        dockerlist_json = json.load(dockerlist)
    try:
        print("[+] Running docker command for "+dockeritem)
        if powershellcmd:
            cmd = powershellcmd+'-c \''+dockerlist_json['dockeritems'][dockeritem][1]+' '+args+'\''
        else:
            cmd = dockerlist_json['dockeritems'][dockeritem][1]+' '+args
        os.system(cmd)
    except:
        print("The specified tool ("+dockeritem+") could not be run. Try one of the following:")
        for key in dockerlist_json['dockeritems'].keys():
            print("    [*] "+key)

def mode_info(dockeritem):
    with open(configfile, "r") as dockerlist:
        dockerlist_json = json.load(dockerlist)
    if dockeritem in dockerlist_json['dockeritems']:
        try:
            print("[+] Info for: "+dockeritem+" (Last updated: "+dockerlist_json['dockeritems'][dockeritem][5]+")\n")
            print("    [*] Description: "+dockerlist_json['dockeritems'][dockeritem][0])
            print("    [*] Usage Notes: "+dockerlist_json['dockeritems'][dockeritem][2])
            print("    [*] Command: "+dockerlist_json['dockeritems'][dockeritem][1])
            print("    [*] Update command: "+dockerlist_json['dockeritems'][dockeritem][3])
            print("    [*] Dockerfile Generation Script: "+dockerlist_json['dockeritems'][dockeritem][4])
        except:
            print("ERROR processing the specified tool ("+dockeritem+").")
    else:
        print("The specified tool ("+dockeritem+") is not in the config file. Try one of the following:")
        for key in dockerlist_json['dockeritems'].keys():
            print("    [*] "+key)

def saveconfig(json):
    jsonfile=os.getcwd()+'/'+json
    print('[+] Saving config\nfrom: '+jsonfile+'\nto: '+configfile+'\n')
    try:
        shutil.copy2(jsonfile, configfile)
    except:
        print('Copy failed, check permissions on source and destination files:\nSource:'+jsonfile+'\nDestination: '+configfile)

def mode_install(json):
    if shutil.which('dockerauto') is None:
        os.system('sudo ln -s '+os.getcwd()+'/dockerauto.py /usr/bin/dockerauto')
        print('[+] DockerAuto now installed via simlink to /usr/bin/dockerauto, you can now run with:\n$ dockerauto [args]')
    #jsonpath=os.path.expanduser('~/dockerlist.json')
    if os.path.exists(configfile):
        overwrite = input('[-] DockerAuto config at '+configfile+' already exists.\nDo you want to overwrite this? (y/N)')
        if overwrite=='y' or overwrite=='Y':
            saveconfig(json)
        else:
            print('Quitting...')
            exit(1)
    else:
        saveconfig(json)
        
def checkwsl():
    powershellcmd = ''
    if os.environ.get('WSL_DISTRO_NAME'):
        for path in ['mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', 'mnt/c/Windows/SysWOW64/WindowsPowerShell/v1.0/powershell.exe']:
                if os.path.exists(path):
                    powershellcmd = path
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
    if powershellcmd:
        print('WSL detected, using PowerShell on host for compatibility:\n'+powershellcmd+')
    checkdeps()
    parser = argparse.ArgumentParser(epilog="OK, bye", formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='mode',required=True)
    parser_list = subparsers.add_parser('list')
    parser_info = subparsers.add_parser('info')
    parser_install = subparsers.add_parser('install')
    parser_update = subparsers.add_parser('update')
    parser_remove = subparsers.add_parser('remove')
    parser_run = subparsers.add_parser('run')
    parser_run.add_argument('dockeritem', type=str, action="store", help="Run the selected DockerAuto items", default='dockerauto')
    parser_update.add_argument('dockeritem', type=str, action="store", help="Run the selected DockerAuto items (or 'update ALL' to update all Docker images)", default='ALL')
    parser_run.add_argument("-a", "--args", action="store", help="Arguments to use in the docker command (surround in 'single quotes' if there are spaces e.g. -a='--help')", required=False, default='')
    parser_info.add_argument('dockeritem', type=str, action="store", help="Info about selected DockerAuto items", default='dockerauto')
    parser_install.add_argument("-j", "--json", action="store", help="URL or local filepath to grab your custom DockerAuto config from", required=False, default='example.dockerlist.json')
    args = parser.parse_args()
    if not os.path.exists(configfile) and args.mode != 'install':
        #usage()
        print('Install config before you can use any other DockerAuto functionality:\n$ python3 dockerauto.py install -j [Path/URL to dockerlist.json]')
        exit(1)
    if args.mode == 'install':
        mode_install(args.json)
    elif args.mode == 'info':
        mode_info(args.dockeritem)
    elif args.mode == 'update':
        mode_update(args.dockeritem)
    elif args.mode == 'remove':
        print('removing configs and images')
    elif args.mode == 'list':
        print('list configs and images')
    elif args.mode == 'run':
        mode_run(args.dockeritem, args.args)
