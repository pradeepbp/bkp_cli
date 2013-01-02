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
Version: 2.01
GUI front end for managing backups
'''


import wx

import backup
import itemdialog
import abt

class MainFrame(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent)
        self.draw_gui()
        self.Show()

    def draw_gui(self):
        self.SetTitle('Backup Utility')
        self.SetSize((500, 300))

        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_panel.SetSizer(main_sizer)

        select_label = wx.StaticText(main_panel, label='Select:')
        location_panel = wx.Panel(main_panel)
        edit_panel = wx.Panel(main_panel)
        control_panel = wx.Panel(main_panel)

        main_sizer.Add(select_label, flag=wx.EXPAND | wx.ALL, border=5)
        main_sizer.Add(location_panel, flag=wx.EXPAND | wx.ALL, border=5)
        main_sizer.Add(edit_panel, flag=wx.EXPAND|wx.ALL, border=5,
                       proportion=1)
        main_sizer.Add(control_panel, flag=wx.EXPAND|wx.ALL, border=5)



        # Location panel
        location_sizer = wx.BoxSizer(wx.HORIZONTAL)
        location_panel.SetSizer(location_sizer)
        self.path = wx.TextCtrl(location_panel,
                                value='Click to open location...',
                                style=wx.TE_READONLY)
        open_button = wx.Button(location_panel, wx.ID_OPEN)

        location_sizer.Add(self.path, proportion=1, flag=wx.GROW|wx.ALL,
                           border=5)
        location_sizer.Add(open_button, flag=wx.ALL, border=5)
        
        self.Bind(wx.EVT_BUTTON, self.click_open, open_button)

        location_panel.Show()



        # Edit panel
        edit_sizer = wx.StaticBoxSizer(wx.StaticBox(edit_panel,label=
                                        'Messages'), wx.HORIZONTAL)
        edit_panel.SetSizer(edit_sizer)
        self.message_pane = wx.TextCtrl(edit_panel, style=wx.TE_MULTILINE |
                                   wx.TE_READONLY)

        edit_sizer.Add(self.message_pane, flag=wx.EXPAND|wx.ALL, proportion=1,
                       border=5)


        # Control panel
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        control_panel.SetSizer(control_sizer)
        self.create_button = wx.Button(control_panel, label='Cre&ate')
        self.create_button.Enable(False)
        self.edit_button = wx.Button(control_panel, label='&Edit')
        self.edit_button.Enable(False)
        self.update_button = wx.Button(control_panel, label='&Update')
        self.update_button.Enable(False)
        close_button = wx.Button(control_panel, wx.ID_CLOSE)
        about_button = wx.Button(control_panel, label='&About')

        control_sizer.Add(self.create_button, proportion=0, border=5)
        control_sizer.Add(self.edit_button, proportion=0, border=5)
        control_sizer.Add(self.update_button, proportion=0, border=5)
        control_sizer.Add(close_button, border=5)
        control_sizer.Add(about_button, flag=wx.LEFT, border=50)

        self.Bind(wx.EVT_BUTTON, self.click_create, self.create_button)
        self.Bind(wx.EVT_BUTTON, self.on_click_close, close_button)
        self.Bind(wx.EVT_BUTTON, self.click_update, self.update_button)
        self.edit_button.Bind(wx.EVT_BUTTON, self.click_edit)
        about_button.Bind(wx.EVT_BUTTON, self.click_about)

        # Resize the frame to contain all widgets
        #self.Fit()

    # Event handler for path updates in the path field
    def path_updated(self, event):
        pass
        print 'path_update'

    # Event handler for close button
    def on_click_close(self, event):
        self.Close()

    # Event handler for open button
    def click_open(self, event):
        dir_open_dialog = wx.DirDialog(self, message='Choose backup location',
                                       style=wx.DD_DEFAULT_STYLE,
                                       defaultPath="")
        resp = dir_open_dialog.ShowModal()
        print dir_open_dialog.GetPath()
        if resp == wx.ID_OK:
            print dir_open_dialog.GetPath()
            self.path.ChangeValue(dir_open_dialog.GetPath())
            if backup.is_valid_backup(self.path.GetValue()):
                self.edit_button.Enable(True)
                self.update_button.Enable(True)
            else:
                self.create_button.Enable(True)
            dir_open_dialog.Destroy()
        else:
            dir_open_dialog.Destroy()

    # Event handler for add file button
    def add_file(self, event):
        file_open_dialog = wx.FileDialog(self, style=wx.FD_OPEN,
                                         message='Choose the file to add')
        resp = file_open_dialog.ShowModal()
        if resp == wx.ID_OK:
            backup.add_path_to_data_file(self.path.GetValue(),
                                        file_open_dialog.GetPath())
            file_open_dialog.Destroy()
        else:
            file_open_dialog.Destroy()

    def click_create(self, event):
        backup.create_data_file(self.path.GetValue())
        self.edit_button.Enable(True)
        self.update_button.Enable(True)
        self.create_button.Enable(False)
        self.message_pane.AppendText('New backup location created\n')


    # Event handler for add folder button.
    def add_folder(self, event):
        pass
        dir_dialog = wx.DirDialog(self, style=wx.DD_DEFAULT_STYLE,
                                  message='Choose folder to add')
        resp = dir_dialog.ShowModal()
        if resp == wx.ID_OK:
            backup.add_path_to_data_file(self.path.GetValue(),
                                         dir_dialog.GetPath())
            dir_dialog.Destroy()
        else:
            dir_dialog.Destroy()

    # Event handler for update button
    def click_update(self, event):
        self.message_pane.AppendText('Updating backup...wait\n')
        backup.update_all(self.path.GetValue())
        self.message_pane.AppendText('Done!\n')

    # Event handler for edit button
    def click_edit(self, event):
        selected_bkp = self.path.GetValue()
        source_paths = backup.get_backup_sources(selected_bkp)
        dialog = itemdialog.ItemDialog(self,'Add item',source_paths)
        resp = dialog.ShowModal()
        if resp == wx.ID_OK:
            modified_paths = dialog.get_list()
            backup.update_config_file(selected_bkp, modified_paths)
            dialog.Destroy()
        else:
            dialog.Destroy()

    def click_about(self, event):
        abt.About()
        
# App initialiser
if __name__ == '__main__':
    app = wx.App(redirect=False)
    MainFrame()
    app.MainLoop()
