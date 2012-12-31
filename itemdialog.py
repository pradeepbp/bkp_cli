#!/usr/bin/env python

'''
    GUI interface for managing backups
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
bkpgui.py
Version: 2.0
Module to create dialog box for visually modifying contents of a list
'''

import wx
import os

class ItemDialog(wx.Dialog):
    def __init__(self, parent=None, title=None, initial_list=[]):
        wx.Dialog.__init__(self, parent)
        self.item_list = initial_list
        self.draw_gui(title)
        #self.ShowModal()


    # Method created the widgets for main window
    def draw_gui(self, title):
        self.SetTitle(title)
        self.SetSize((400,300))


        # Main layout manger
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)
        
        # Sub layout managers
        edit_sizer = wx.BoxSizer(wx.HORIZONTAL)
        edit_button_sizer = wx.BoxSizer(wx.VERTICAL)
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # main widgets
        command_text = wx.StaticText(self, label='Add files or folders:')
        self.item_display = wx.ListBox(self, style=wx.LB_MULTIPLE,
                                       choices=self.item_list)
        add_button = wx.Button(self, label='Add file')
        add_folder_button = wx.Button(self, label='Add folder')
        delete_button = wx.Button(self, label='Remove')
        delete_button.Enable(True)


        # Add respective widgets to sizers
        main_sizer.Add(command_text, flag=wx.EXPAND|wx.ALL, border=5)
        edit_sizer.Add(self.item_display, flag=wx.EXPAND, proportion=1,
                       border=5)
        edit_button_sizer.Add(add_button, border=5, flag=wx.ALL)
        edit_button_sizer.Add(add_folder_button, border=5, flag=wx.ALL)
        edit_button_sizer.Add(delete_button, border=5, flag=wx.ALL)
        edit_sizer.Add(edit_button_sizer, border=5, flag=wx.ALL)
        main_sizer.Add(edit_sizer, flag=wx.EXPAND|wx.ALL, 
                       proportion=1, border=5)

        control_sizer = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        main_sizer.Add(control_sizer, flag=wx.EXPAND|wx.ALL, border=10)

        # Resize frame
        #self.Fit()
        self.Bind(wx.EVT_CLOSE, self.on_close, self)
        add_button.Bind(wx.EVT_BUTTON, self.click_add_file)
        add_folder_button.Bind(wx.EVT_BUTTON, self.click_add_folder)
        delete_button.Bind(wx.EVT_BUTTON, self.click_delete)

    # Event handler for OK button
    def click_ok(self, event):
        list = self.get_list()
        print list
        self.Destroy()


    # Manage close event of the dialog
    def on_close(self, event):
        self.Destroy()


    # Event handler for 'add file' button
    def click_add_file(self, event):
        dialog = wx.FileDialog(self, style=wx.FD_OPEN|wx.FD_MULTIPLE)
        resp = dialog.ShowModal()
        if resp == wx.ID_OK:
            selected_paths = dialog.GetPaths()
            self.add_items_to_list(selected_paths)
            dialog.Destroy()
        else:
            dialog.Destroy()

    # Event hanlder for 'add folder' button
    def click_add_folder(self, event):
        dialog = wx.DirDialog(self, style=wx.DD_DIR_MUST_EXIST)
        resp = dialog.ShowModal()
        if resp == wx.ID_OK:
            self.add_items_to_list([dialog.GetPath()])
            dialog.Destroy()
        else:
            dialog.Destroy()

    # Event handler for 'delete' button
    def click_delete(self, event):
        rem_index = self.item_display.GetSelections()
        print rem_index
        mod_list = self.delete_items_from_list(rem_index) 
        print mod_list
        self.item_display.Clear()
        self.item_display.InsertItems(mod_list, 0)

    # All items to list and update list display
    def add_items_to_list(self, items):
        for path in items:
            npath = os.path.normpath(path)
            self.item_list.append(str(npath))
            self.item_display.InsertItems([npath], len(self.item_list)-1) 

    # Return the updated list
    def get_list(self):
        return self.item_list


    # This method removes an existing item from the list and returns
    # the updated list. The indices of the item needs to be passed 
    # as an argument
    def delete_items_from_list(self, item_index):
        display_list = self.get_list()
        for i in item_index:
            display_list.pop(i)
        return display_list
    

if __name__ == '__main__':
    app = wx.App(redirect=False)
    ItemDialog(title='test dialog')
    app.MainLoop()

