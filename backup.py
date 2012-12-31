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
backup.py
Module for performing various backup related activities
Version: 2.0
'''
#!/usr/bin/python

import os
import shutil
import time



# Function updates the file at backup location
def update_file(path, bkp_location):
    npath = os.path.normpath(path)
    nbkp_location = os.path.normpath(bkp_location)
    arch_path = os.path.join(nbkp_location, os.path.split(npath)[1])
    update_path(npath, arch_path)


# Function updates folder at backup location
def update_folder(path, bkp_location):
    npath = os.path.normpath(path)
    nbkp_location = os.path.normpath(bkp_location)
    
    tree = os.walk(npath)
    base = os.path.split(npath)[0]

    for item in tree:
        for name in item[2]:
            abs_path = os.path.normpath(os.path.join(item[0], name))
            arch_path = os.path.normpath(os.path.join(nbkp_location,
                                            abs_path.lstrip(base)))

            print 'abs:%s arch:%s' % (abs_path, arch_path)
            update_path(abs_path, arch_path)

# Function for updatibg the path
def update_path(abs_path, arch_path):
    nabs_path = os.path.normpath(abs_path)
    narch_path = os.path.normpath(arch_path)
    print 'Checking: %s' % nabs_path
    if os.path.exists(narch_path) and (os.path.getmtime(nabs_path)
                                    < os.path.getmtime(narch_path)):
        pass
    else:
        # Create sub-directories if required
        try:
            os.makedirs(os.path.split(narch_path)[0])
        except os.error:
            pass
        
        # Copy file path
        try:
            print 'Adding: %s...%d' % (nabs_path, os.path.getsize(nabs_path))
            shutil.copy(nabs_path, narch_path)
        except IOError:
            print 'Error while handling file'

# Function to add or update files/ folders to backup location
def update_backup_location(path_list, bkp_location):
    for path in path_list:
        if os.path.isfile(path):
            update_file(os.path.normpath(path), os.path.normpath(bkp_location))
        elif os.path.isdir(path):
            update_folder(os.path.normpath(path),
                          os.path.normpath(bkp_location))
    print '\n' + 10*'=' + ' DONE ' + 10*'='            

# Function to create an empty data file at backup location
def create_data_file(bkp_location):
    file_handle = open(os.path.join(bkp_location, 'bkpconfig.txt'), 'w')
    file_handle.write(os.path.normpath(bkp_location)+'\n')
    file_handle.close()

# Function to add single path to data file
def add_path_to_data_file(bkp_path, source_path):
    try:
        file_handle = open(os.path.join(os.path.normpath(bkp_path),
                           'bkpconfig.txt'),'a')
        file_handle.write(os.path.normpath(source_path) + '\n')
        file_handle.close()
    except IOError:
        print 'Error opening config data file; check backup path'


# Function to add multiple paths to data file at a time
def add_paths_to_data_file(bkp_path, source_paths):

    try:
        file_handle = open(os.path.join(os.path.normpath(bkp_path),
                           'bkpconfig.txt'),'a')
        for path in source_paths:
            file_handle.write(os.path.normpath(path) + '\n')
        file_handle.close()
    except IOError:
        print 'Error opening config data file; check backup path'
  
# Function to update backup when only backup location is passed as an argument
def update_all(bkp_location):
    try:
        file_handler = open(os.path.join(os.path.normpath(bkp_location),
                            'bkpconfig.txt'), 'r')
        path_data = [line.rstrip() for line in file_handler.readlines()]
        file_handler.close()
        update_backup_location(path_data[1:], bkp_location)
    except IOError:
        print 'Error opening config data file; check backup path.'

'''
Functions returns True if the passed path is a valid backup location
by examining the presence of config file
'''
def is_valid_backup(path):
    pass
    config_file_path = os.path.join(os.path.normpath(path), 'bkpconfig.txt')
    if os.path.exists(config_file_path):
        return True
    else:
        return False


''' 
Function to return the file path contained in the config file
'''
def get_backup_sources(bkp_location):
    config_file = os.path.join(os.path.normpath(bkp_location), 'bkpconfig.txt')
    try:
        file_h = open(config_file, 'r')
        source_paths = [line.rstrip() for line in file_h.readlines()]
        file_h.close()
        return source_paths[1:]

    except:
        print 'Configuration File Error'

'''
Function to update config file with new source data; return True if
update was successfull
'''
def update_config_file(bkp_location, source_paths):
    config_file = os.path.join(os.path.normpath(bkp_location), 'bkpconfig.txt')
    try:
        file_h = open(config_file, 'w')
        file_h.write(os.path.normpath(bkp_location) + '\n')
        for path in source_paths:
            file_h.write(os.path.normpath(path)+'\n')
        file_h.close()
        return True
    except:
        return False
