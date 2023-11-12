'''

The 3-Clause BSD License

Copyright 2023, merky (github.com/Gaomengkai)

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form or with modification must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the merky nor the names of its contributors may be used to endorse or promote products derived

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

import os
import wx
from pathlib import Path

import gaiming

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400, 300))
        # self.panel = wx.Panel(self)
        self.panel = self
        
        # subtitle path
        self.label1 = wx.StaticText(self.panel, label=" Subtitle Path")
        self.path_subtitle = wx.TextCtrl(self.panel, value="")
        self.btn_open_subtitle = wx.Button(self.panel, label="Open")
        self.btn_open_subtitle.Bind(wx.EVT_BUTTON, self.onOpen)
        self.horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontal_box.Add(self.path_subtitle, 1, wx.EXPAND)
        self.horizontal_box.Add(self.btn_open_subtitle, 0, wx.LEFT, 5)
        
        
        # video path
        self.label2 = wx.StaticText(self.panel, label=" Video Path")
        self.path_video = wx.TextCtrl(self.panel, value="")
        self.btn_open_video = wx.Button(self.panel, label="Open")
        self.btn_open_video.Bind(wx.EVT_BUTTON, self.onOpen)
        self.horizontal_box2 = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontal_box2.Add(self.path_video, 1, wx.EXPAND)
        self.horizontal_box2.Add(self.btn_open_video, 0, wx.LEFT, 5)
        
        
        self.vb = wx.BoxSizer(wx.VERTICAL)
        self.vb.Add(self.label1, 0, wx.EXPAND, 5)
        self.vb.Add(self.horizontal_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        self.vb.Add(self.label2, 0, wx.EXPAND, 5)
        self.vb.Add(self.horizontal_box2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        
        self.btn_run = wx.Button(self.panel, label="Run")
        self.btn_run.Bind(wx.EVT_BUTTON, self.onRun)
        self.vb.Add(self.btn_run, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        
        self.status_bar = self.CreateStatusBar()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.vb, 1, wx.EXPAND)
        # self.panel.SetSizer(self.vb)
        self.SetSizer(sizer)
        
        self.initUI()
    def initUI(self):
        self.SetTitle("字幕改名器 by merky")
        self.Centre()
        self.Show(True)
    def onOpen(self,e):
        """ Open a Path"""
        self.dirname = ''
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if os.path.exists(path):
                print(path)
                if e.GetEventObject() == self.btn_open_subtitle:
                    self.path_subtitle.SetValue(path)
                elif e.GetEventObject() == self.btn_open_video:
                    self.path_video.SetValue(path)
    def onRun(self,e):
        self.status_bar.SetStatusText(f"正在处理...")
        path_video = Path(self.path_video.GetValue())
        path_sub = Path(self.path_subtitle.GetValue())
        if path_sub.exists() and path_video.exists():
            try:
                x = gaiming.gaiming(path_video, path_sub)
                self.status_bar.SetStatusText(f"完成{len(x)}")
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
                print(e)
                self.status_bar.SetStatusText(f"Error")
        else:
            wx.MessageBox("路径不存在", "Error", wx.OK | wx.ICON_ERROR)
            self.status_bar.SetStatusText(f"路径不存在")
        
        
def main():
    try:
        app = wx.App()
        frame = MainFrame(None, "字幕改名器")
        app.MainLoop()
    except Exception as e:
        wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
        with open("errlog.log","w",encoding='utf8') as f:
            f.write(str(e))
            f.write(str(e.__traceback__))

if __name__ == '__main__':
    main()