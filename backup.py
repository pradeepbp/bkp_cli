'''
    Module defining functions for a simple backup utility..V 1.01
    Copyright (C) 2012  Pradeep Balan PIllai

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
backup.py: module containing functions for backup utility
Version: 1.01
'''

#!/usr/bin/python

import os
import shutil
import time

CFG_FILE = 'bkp.txt'
CFG_DATA = []

# Funtion to create a bew backup location
def create_new_backup(bkp_location):
    try:
        os.mkdir(bkp_location)
        bkp_config = open(os.path.join(bkp_location, CFG_FILE), 'w')
        bkp_config.close()
        print 'Backup location successfully created at: %s' % bkp_location
    except OSError:
        print 'Unable to create new backup location. Check for duplicates.'


# Function to add the list of files to backup location
def add_items_to_backup(path_list, bkp_location):

    # Load configuration data for reference
    CFG_DATA = read_conf(bkp_location)
    #print CFG_DATA

    if os.path.exists(os.path.join(bkp_location,CFG_FILE)):
        bkp_cfg = open(os.path.join(bkp_location,CFG_FILE), 'w')
    else:
        print 'Error: Cannot open configuration file'
        return
    for path in path_list:
        print 'Checking...%s' % os.path.normpath(path)
        if os.path.isfile(path):              
            if update_required(path, CFG_DATA):
                print 'Adding:%s...%d %s' % (os.path.normpath(path), os.path.getsize(path),'bytes')
                try:
                    shutil.copy(path, bkp_location) 
                except IOError:
                    print 'Error: File operation...%s' % path
            arch_path = os.path.normpath(os.path.join(bkp_location, os.path.split(path)[1]))
            bkp_cfg.write(os.path.normpath(path) + ',' + arch_path +
                            ',' + str(time.time()) + '\n')
        elif os.path.isdir(path):
            tree_paths = get_folder_tree_paths(path, bkp_location)
            if update_required(path, CFG_DATA):
                #print 'Updating folder'
                bkp_cfg.write(os.path.normpath(path) + ',' +
                                os.path.normpath(os.path.join(bkp_location, os.path.split(path)[1])) + ',' +
                                str(time.time()) + '\n')
                for item in tree_paths:
                    if update_required(item[0], CFG_DATA):
                        # First create the sub-directories, if required
                        try:
                            os.makedirs(os.path.split(item[1])[0])
                        except os.error:
                            pass
                        print 'Adding: %s...%d' % (item[0], os.path.getsize(item[0]))
                        try:
                            shutil.copy(item[0], item[1])
                        except IOError:
                            print 'Error: File operation...%s' % path

                    bkp_cfg.write(os.path.normpath(item[0]) + ',' + os.path.normpath(item[1]) +
                                ',' + str(time.time())+'\n')
            else:
                bkp_cfg.write(os.path.normpath(path) + ',' +
                                os.path.normpath(os.path.join(bkp_location, os.path.split(path)[1])) + ',' +
                                return_timestamp(path, CFG_DATA) + '\n')
                for item in tree_paths:
                    if update_required(item[0], CFG_DATA):
                        # First create the sub-directories, if required
                        try:
                            os.makedirs(os.path.split(item[1])[0])
                        except os.error:
                            pass
                        print 'Adding: %s...%d' % (item[0], os.path.getsize(item[0]))
                        try:
                            shutil.copy(item[0], item[1])
                        except IOError:
                            print 'Error: File operation...%s' % path
                            
                        bkp_cfg.write(os.path.normpath(item[0]) + ',' + os.path.normpath(item[1]) +
                                    ',' + str(time.time()) + '\n')
                    else:
                        bkp_cfg.write(os.path.normpath(item[0]) + ',' + os.path.normpath(item[1]) +
                                    ',' + return_timestamp(item[0],CFG_DATA)+'\n')


        else:
            print 'Error, path not found: %s' % path
    bkp_cfg.close()

def get_folder_tree_paths(folder_path, bkp_location):
    path_list = []
    tree = os.walk(folder_path)
    base = os.path.normpath(os.path.split(folder_path)[0])
    for item in tree:
        real_path = os.path.normpath(item[0])
        for file_name in item[2]:
            abs_path = os.path.normpath(os.path.join(real_path,file_name))
            arch_path = os.path.normpath(os.path.join(bkp_location, abs_path.lstrip(base)))
            path_list.append((abs_path, arch_path))
    return path_list

# This function reads the existing configuration entry into a list of meaningful
# dictionary
def read_conf(bkp_location):
    conf_data = []
    content = []
    try:
        cnf = open(os.path.join(bkp_location, CFG_FILE),'r')
        file_content = cnf.readlines() 
    except IOError:
        print 'Error: Cannot open configuration file'
        return None
    cnf.close()

    if len(file_content) != 0:
        for line in file_content:
            content.append(line.split('\n'))

    if len(content) != 0:
        for item in content:
            data = item[0].split(',')
            conf_data.append({'abs_path':data[0], 'arch_path':data[1], 'up_time':data[2]})
    return conf_data

# This function return a list of source paths from the configuration file
def get_source_paths(bkp_location):
    return [item['abs_path'] for item in (read_conf(bkp_location))]

# Function to return the update status of path; True, if update is required,
# and False, if not required
def update_required(path, config_data):
    npath = os.path.normpath(path)
    flag = True
    for data in config_data:
        nabs_path = os.path.normpath(data['abs_path'])
        #print 'Checking: %s %s' % (npath, nabs_path)
        if (npath == nabs_path) and (os.path.getmtime(npath) > float(data['up_time'])):
            #print 'Existing file...update required:%s,%f,%s'% (npath,os.path.getmtime(npath), data['up_time'])
            flag = True
            break
        elif (npath == nabs_path) and (os.path.getmtime(npath) <= float(data['up_time'])): 
            #print 'Existing file...update not required:%s,%f,%s'% (npath,os.path.getmtime(npath), data['up_time'])
            flag = False
            break
        else:
            flag = True
            #print 'New file... to be added:%s,%f,%s'% (npath,os.path.getmtime(npath), data['up_time'])
    return flag

def update_backup(bkp_location):
    add_items_to_backup(bkp_location)
    
# Return the time stamp from cfg data
def return_timestamp(path, cfg_data):
    npath = os.path.normpath(path)
    for data in cfg_data:
        nabs_path = os.path.normpath(data['abs_path'])
        if npath == nabs_path:
            return data['up_time']
