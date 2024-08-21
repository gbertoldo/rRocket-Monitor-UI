"""
  The MIT License (MIT)

  rRocket-Monitor-UI Graphical User Interface for rRocket
  Copyright (C) 2024 Guilherme Bertoldo
  (UTFPR) Federal University of Technology - Parana

  Permission is hereby granted, free of charge, to any person obtaining a 
  copy of this software and associated documentation files (the “Software”), 
  to deal in the Software without restriction, including without limitation 
  the rights to use, copy, modify, merge, publish, distribute, sublicense, 
  and/or sell copies of the Software, and to permit persons to whom the Software 
  is furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all 
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import wx
import os
import bitmaptools
import wx.adv
import wxpserial
from datetime import datetime

import UITemplate
from UIReportFrame import *
from UIPanelConnection import *
from UIPanelMonitor import *
from UIPanelAnalysis import *
from UIModelessDialog import *

from rRocketMonitorModel import *

APP_VERSION_STRING="v.1.0.0"

def onLinux() -> bool:
	if os.name == 'posix':
		return True
	return False

class rRocketUIListbook(wx.Listbook):
    """
    Listbook class
    """
    def __init__(self, parent, statusBar):
        """
        Constructor
        """
        wx.Listbook.__init__(self, parent, wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             )
        
        self.statusBar = statusBar

        # make an image list using the LBXX images
        toolsize = 50
        il = wx.ImageList(toolsize, toolsize)
        
        fig1 = bitmaptools.scale_bitmap(wx.Bitmap( bitmaptools.resource_path(u"fig/usb-cable-icon.png"), wx.BITMAP_TYPE_ANY ), toolsize, toolsize)
        fig2 = bitmaptools.scale_bitmap(wx.Bitmap( bitmaptools.resource_path(u"fig/ecg-monitoring-icon.png"), wx.BITMAP_TYPE_ANY ), toolsize, toolsize)
        fig3 = bitmaptools.scale_bitmap(wx.Bitmap( bitmaptools.resource_path(u"fig/market-research-analysis-icon.png"), wx.BITMAP_TYPE_ANY ), toolsize, toolsize)
        il.Add(fig1)
        il.Add(fig2)
        il.Add(fig3)
        self.AssignImageList(il)

        self.serialParameters = wxpserial.SerialParameters(port=None
            , baudrate=115200
            , bytesize=8
            , parity=wxpserial.serial.PARITY_NONE
            , stopbits=wxpserial.serial.STOPBITS_ONE
            , timeout=0.05
            , xonxoff=False
            , rtscts=False
            , write_timeout=0.05
            , dsrdtr=False
            , inter_byte_timeout=None
            , exclusive=True)
        
        self.rRocketMonitorModel = rRocketMonitorModel(self)
        self.panelConnection = PanelConnection(self)
        self.panelMonitor = PanelMonitor(self, self.rRocketMonitorModel)
        self.panelAnalysis = PanelAnalysis(self, APP_VERSION_STRING)

        pages = [(self.panelConnection, "Conexão"),
                 (self.panelMonitor, "Monitor"),
                 (self.panelAnalysis, "Análise")]
        imID = 0
        for page, label in pages:
            self.AddPage(page, label, imageId=imID)
            imID += 1
        self.setDisconnectedAppearance()


    def isFirmwareVersionCompatible(self,version):
        decomposedVersion = version.strip().split(".")
        try:
            if (int(decomposedVersion[0]) == 1) and (int(decomposedVersion[1]) == 0):
                return True
            else:
                return False
        except:
            return False

    def rRocketMonitorModelStateUpdate(self):
        state = self.rRocketMonitorModel.state
        if state == rRocketMonitorState["Disconnected"]:
            self.setDisconnectedAppearance()
        elif state == rRocketMonitorState["Ready"]:
            self.setReadyAppearance()   
        elif state == rRocketMonitorState["Initializing"]:
            self.setInitializingAppearance()
        else:
            self.rRocketMonitorModel.stop()
            wx.MessageBox(self, "rRocket-Monitor em estado desconhecido. Conexão fechada.", "Erro", wx.OK | wx.ICON_ERROR)


    def rRocketMonitorModelDataUpdate(self):
        t=self.rRocketMonitorModel.dataLogger.t
        h=self.rRocketMonitorModel.dataLogger.h
        vB=self.rRocketMonitorModel.dataLogger.vB
        vD=self.rRocketMonitorModel.dataLogger.vD
        vP=self.rRocketMonitorModel.dataLogger.vP
        self.panelMonitor.plot(t, h, vB, vD, vP)
        
    def rRocketModelParameterUpdate(self, event):
        pass

    def report(self):
        log = []
        log.append("")
        log.append("rRocket-Monitor. Firmware: "+self.rRocketMonitorModel.firmwareVersion)
        log.append("")
        txt = ""
        for item in log:
            txt = txt + "# " + str(item)+"\n"
        return txt+self.rRocketMonitorModel.report()

    def setDisconnectedAppearance(self):
        self.panelConnection.setDisconnectedAppearance()
        self.panelMonitor.setDisconnectedAppearance()
        self.panelAnalysis.setDisconnectedAppearance()
        self.statusBar.SetStatusText("rRocket-Monitor desconectado")

    def setReadyAppearance(self):
        self.panelConnection.setReadyAppearance()
        self.panelMonitor.setReadyAppearance()
        self.panelAnalysis.setReadyAppearance()
        self.statusBar.SetStatusText("")

    def setInitializingAppearance(self):
        self.panelConnection.setInitializingAppearance()
        self.panelMonitor.setInitializingAppearance()
        self.panelAnalysis.setInitializingAppearance()
        self.statusBar.SetStatusText("rRocket-Monitor em processo de inicialização... Por favor, aguarde.")




class MainFrame(UITemplate.MainFrame):
    def __init__(self, parent):
        UITemplate.MainFrame.__init__(self,parent)

        notebook = rRocketUIListbook(self.basePanel, self.statusBar)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND, 5)
        self.basePanel.SetSizer(sizer)

        self.Layout()
        sizer.Fit(self.basePanel)

    def onMenuItemClose( self, event ):
        self.Close()

    def onMenuItemAbout( self, event ):
        aboutInfo = wx.adv.AboutDialogInfo()
        aboutInfo.SetName("rRocket-Monitor-UI")
        aboutInfo.SetIcon(wx.Icon(bitmaptools.resource_path("./fig/rRocketMonitor.ico"), desiredWidth=1))
        aboutInfo.SetVersion(APP_VERSION_STRING)
        aboutInfo.SetDescription("Interface Gráfica para rRocket-Monitor")
        aboutInfo.SetCopyright("(C) 2024 - Universidade Tecnológica Federal do Paraná")
        #aboutInfo.SetWebSite("http:#myapp.org")
        aboutInfo.AddDeveloper("Guilherme Bertoldo")
        aboutInfo.AddArtist("Guilherme Bertoldo")
        aboutInfo.AddArtist("uxwing.com")

        wx.adv.AboutBox(aboutInfo)