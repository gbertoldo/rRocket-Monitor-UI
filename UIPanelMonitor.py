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
import UITemplate
import UIPlot
from UIReportFrame import *
from rRocketMonitorModel import *
from UIModelessDialog import *

class PanelMonitor(UITemplate.PanelMonitor):
    def __init__(self, parent, monitor: rRocketMonitorModel):
        UITemplate.PanelMonitor.__init__(self, parent)
        self.parent = parent
        self.monitor = monitor
        # Plot panel
        plotstyles1=[
            {"style":"-","color":"darkorange","title":"h-Monitor"}
            ]
        plotstyles2=[
            {"style":"-","color":"blue","title":"Vbateria"},
            {"style":"-","color":"green","title":"Vdrogue"},
            {"style":"-","color":"purple","title":"Vparaquedas"}
            ]
        self.plotPanel = UIPlot.rRocketPlot( self.panelBase, plotstyles1, 10,100, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL,plotstyles2=plotstyles2 )
        self.plotPanel.setXLabel("t (s)")
        self.plotPanel.setYLabel("h (m)")
        self.plotPanel.setYLabel2("Tensão (V)")
        self.plotPanel.setTitle("")
        self.plotPanel.setLegend(bbox_to_anchor=(0.0, 1), loc='lower left',ncol=len(plotstyles1), fontsize='x-small')
        self.plotPanel.setLegend2(bbox_to_anchor=(1, 1), loc='lower right', ncol=len(plotstyles2), fontsize='x-small')
        self.plotPanel.setGrid()
        self.plotPanel.addToolbar()
        self.btnStartStop.SetLabel("Iniciar")
        
    def plot(self, t, h, vB, vD, vP):   
        self.plotPanel.draw([[t,h]])
        self.plotPanel.draw2([[t,vB],[t,vD],[t,vP]])

    def onBtnSetTitle( self, event ):
        txt = self.txtCtrlPlotTitle.GetValue()
        self.plotPanel.setTitle(txt)
 
    def onBtnClear( self, event ):
        self.monitor.clearDataLogger()

    def onBtnReport( self, event ):
        log = self.parent.report()
        reportFrm = ReportFrame(self)
        reportFrm.setText(log)
        reportFrm.Show() 

    def onBtnStartStop( self, event ):
        if self.monitor.isRecording:
            self.monitor.stopRecording()
            self.btnStartStop.SetLabel("Iniciar")
        else:
            self.monitor.startRecording()
            self.btnStartStop.SetLabel("Parar")

    def setDisconnectedAppearance(self):
        self.btnClear.Enable(True)
        self.btnReport.Enable(True)
        self.btnStartStop.Enable(False)

    def setReadyAppearance(self):
        self.btnClear.Enable(True)
        self.btnReport.Enable(True)
        self.btnStartStop.Enable(True)
