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
abt.py
Version: 2.01
Module to create About dialog box
'''

import wx
import wx.html


class About(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE &
                          ~ wx.MAXIMIZE_BOX)
        self.draw_gui()

    def draw_gui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        book = wx.Notebook(self)        
        content = wx.html.HtmlWindow(book)
        book.AddPage(content, 'About')
        content.LoadPage('abt.html')
        license = wx.TextCtrl(book, style=wx.TE_MULTILINE|wx.TE_READONLY)
        book.AddPage(license, 'License')
        license.LoadFile('license.txt')

        ok_button = wx.Button(self, label='OK')
        ok_button.Bind(wx.EVT_BUTTON, self.click_ok_button)

        sizer.Add(book, proportion=1, flag=wx.EXPAND)
        sizer.Add(ok_button, flag=wx.ALIGN_CENTRE_HORIZONTAL)
        self.Show()

    def click_ok_button(self, event):
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    About()
    app.MainLoop()


