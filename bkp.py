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
            update_folder(os.path.normpath(path), os.path.normpath(bkp_location))
    print '\n' + 10*'=' + ' DONE ' + 10*'='            
