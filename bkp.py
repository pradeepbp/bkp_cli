'''
    Initialisation script for command line based backup utility... V 1.0
    Copyright (C) 2012 Pradeep Balan Pillai

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
bkp.py: initialisation script for command line based backup utility
Version: 1.0

'''
import sys

import backup

# Function to process command
def process_command(command_list):
    try:
        file_handler = open(command_list[2], 'r')
        # Remove the newline character also while adding path list
        data = [line.rstrip() for line in file_handler.readlines()]
        #data = file_handler.readlines()
        file_handler.close()
    except IOError:
        print 'Error reading data file'

    # Remove the newline characters
    
    if command_list[1] == '-n':
        backup.create_new_backup(data[0])
    elif command_list[1] == '-a':
        backup.add_items_to_backup(data[1:], data[0])
    elif command_list[1] == '-t':
        pass # test code here


if len(sys.argv) < 3:
    print 'Insufficient parameters'
else:
    process_command(sys.argv)

        
