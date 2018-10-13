#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from weather import Weather

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, pos=(150, 150), size=(350, 550))
        panel = wx.Panel(self)

        city = wx.StaticText(panel, -1, "Hangzhou:")
        city.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        city.SetSize(city.GetBestSize())

        forecast = wx.StaticText(panel, -1, Weather().forecast())

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(city, 0, wx.ALL, 10)
        sizer.Add(forecast, 1, wx.ALL, 10)

        panel.SetSizer(sizer)
        panel.Layout()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, "Weekly Weather Forecast")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

app = MyApp(redirect=True, filename="log.txt")
app.MainLoop()
