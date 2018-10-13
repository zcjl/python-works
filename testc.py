#!/usr/bin/env python
#coding=utf-8
import wx
import socket
import threading
class WorkerThread(threading.Thread):
    def __init__(self,window,sockets):
        threading.Thread.__init__(self)
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.data =""
        self.socket = sockets
    def run (self):
        while 1:
            print "waiting for connection..."
            tcpCliSock,addr = self.socket.accept()
            wx.CallAfter(self.window.GetCliSock,tcpCliSock)
            print "connected from ",addr
            
            while 1:
                data = tcpCliSock.recv(1024)
                if not data :
                    print 'breaked'
                    break
                wx.CallAfter(self.window.SetShoreText,data)
                
            tcpCliSock.close()
        
    def stop(self):
        print 'close'
        self.socket.close()
        self.timeToQuit.set()
        
class MyServerTcp:
    """
    a simple tcp servrce class 
    """
    def __init__(self):
        self.listensocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
   
    def Bind(self,address,port):
        self.listensocket.bind((address,port))
    def listen(self,num=1):
        self.listensocket.listen(num)
        #self.clientsocket,self.clientaddress = self.listensocket.accept()
    
class MyChatFrame(wx.Frame):
    def __init__(self,titles,toplabel):
        wx.Frame.__init__(self,None,-1,title = titles)
        panel = wx.Panel(self,-1)
        
        
        self.Bind(wx.EVT_CLOSE,self.OnCloseWindow)
        self.server = MyServerTcp()
        
        self.bthread = False
        #首先建立需要建立的标签
        #文字信息
        toplabel = wx.StaticText(panel,-1,"simple test")
        toplabel.SetFont(wx.Font(18,wx.SWISS,wx.NORMAL,wx.BOLD))
        
        addrsssLabel = wx.StaticText(panel,-1,"IP地址:")
        self.address = wx.TextCtrl(panel,-1,"localhost")
        
        portLabel = wx.StaticText(panel,-1,"port:")
        self.port      = wx.TextCtrl(panel,-1,"8000")
        
        self.shore = wx.TextCtrl(panel,-1,"",size=(300,400),style=wx.TE_MULTILINE|wx.TE_RICH2 )
        
        self.input = wx.TextCtrl(panel,-1,"",size=(200,-1))
        buttonListen = wx.Button(panel,-1,"Listen")
        self.Listenbutton = buttonListen
        self.Bind(wx.EVT_BUTTON,self.OnListen,buttonListen)
        
        buttonSend = wx.Button(panel,-1,"send")
        buttonSend.Enable(False)
        self.Sendbutton=buttonSend
        self.Bind(wx.EVT_BUTTON,self.OnSend,buttonSend)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(toplabel,0,wx.ALL,5)
        #mainSizer.Add(wx.StaticLine(panel),0,wx.EXPAND|wx.TOP,wx.BOTTOM,5)
        
        #添加ip地址
        addrSizer = wx.FlexGridSizer(cols=2,hgap=5,vgap=5)
        addrSizer .AddGrowableCol(1)
        addrSizer.Add(addrsssLabel,0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.address,0,wx.EXPAND)
        addrSizer.Add(portLabel,0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.port,0,wx.EXPAND)
        addrSizer.Add(wx.StaticText(panel,-1,""),0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        
        
       
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        buttonSizer.Add(self.input,0,wx.EXPAND)
        buttonSizer.Add((20,20),1)
        buttonSizer.Add(buttonSend)
        buttonSizer.Add((20,20),1)
        
        
        
        mainSizer.Add(addrSizer,0,wx.EXPAND|wx.ALL,10)
        mainSizer.Add(buttonListen,0,wx.ALIGN_CENTER_HORIZONTAL)
        mainSizer.Add(self.shore,0,wx.EXPAND|wx.ALL,10)
        mainSizer.Add(buttonSizer,0,wx.EXPAND|wx.ALL,10)
        
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)
    def OnListen(self,event):
        address = self.address.GetValue()
        port = int(self.port.GetValue())
        self.server.Bind(address,port)
        self.server.listen(3)
        self.thread = WorkerThread(self,self.server.listensocket)
        self.thread.start()
        self.bthread=True
        self.Listenbutton.Enable(False)
        self.Sendbutton.Enable(True)
    def OnSend(self,event):
        
        data = self.input.GetValue()
        print data.encode('gb2312')
        if data:
            self.shore.AppendText(u"你说:"+data+"\n")
            
            if self.tcpClisocket:
                self.tcpClisocket.send(data.encode('gb2312'))
        
        
    def SetShoreText(self,data):
        self.shore.AppendText(u"客户:"+data+"\n")
    def GetCliSock(self,tcpClisocket):
        self.tcpClisocket = tcpClisocket
        
        
    def OnCloseWindow(self,event):
        if self.bthread:
            self.thread.stop()
        self.Destroy()
        
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyChatFrame("TCP Server","My Test")
    frame.Show()
    app.MainLoop()