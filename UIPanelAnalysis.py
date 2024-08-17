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
import FlightDataImporter
from UIReportFrame import *
from rRocketMonitorModel import *
from UIModelessDialog import *
import UIInputFileFormatFrame
from datetime import datetime
import os
import DataLogger
import numpy as np
import math


def getFlightEvents(filename):
  lines = []
  events = []
  strF=" s: Voo detectado"
  strD=" s: Drogue acionado"
  strP=" s: Paraquedas principal acionado"
  strL=" s: Aterrissagem detectada"
  with open(filename,'r') as  fp:
    lines = fp.readlines()
  
  for line in lines:
    if strF in line:
      line = line.replace(strF,"")
      line = line.replace("#","")
      events.append([float(line),0,0,0,"F"])
    elif strD in line:
      line = line.replace(strD,"")
      line = line.replace("#","")
      events.append([float(line),0,0,0,"D"])
    elif strP in line:
      line = line.replace(strP,"")
      line = line.replace("#","")
      events.append([float(line),0,0,0,"P"])
    elif strL in line:
      line = line.replace(strL,"")
      line = line.replace("#","")
      events.append([float(line),0,0,0,"L"])
  return events

class PanelAnalysis(UITemplate.PanelAnalysis):
    def __init__(self, parent, appversion):
        UITemplate.PanelAnalysis.__init__(self, parent)
        self.parent = parent
        self.appversion = appversion
        # Plot panel
        plotstyles1=[
            {"style":"-","color":"darkorange","title":"h-rRocket"},
            {"style":"-","color":"darkcyan","title":"h-Monitor"}
            ]
        plotstyles2=[
            {"style":"-","color":"blue","title":"Vbateria"},
            {"style":"-","color":"green","title":"Vdrogue"},
            {"style":"-","color":"purple","title":"Vparaquedas"}
            ]
        self.plotPanel = UIPlot.rRocketPlot(parent=self.panelBase, plotstyles=plotstyles1, fontsize=10,dpi=100,id=wx.ID_ANY,pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name="", plotstyles2=plotstyles2 )
        self.plotPanel.setXLabel("t (s)")
        self.plotPanel.setYLabel("")
        self.plotPanel.setTitle("")
        self.plotPanel.setLegend(bbox_to_anchor=(0.0, 1), loc='lower left',ncol=len(plotstyles1), fontsize='x-small')
        self.plotPanel.setLegend2(bbox_to_anchor=(1, 1), loc='lower right', ncol=len(plotstyles2), fontsize='x-small')
        self.plotPanel.setYLabel("h (m)")
        self.plotPanel.setYLabel2("Tensão (V)")
        self.plotPanel.setGrid()
        self.plotPanel.addToolbar()

        self.inputFileFormat = UIInputFileFormatFrame.InputFileFormat()
        self.tmpFolder="tmp"
        self.monitorfilename=self.tmpFolder+"/"+"monitorFile.txt"
        self.rrocketfilename=self.tmpFolder+"/"+"rRocketFile.txt"
        self.rRocketDataLogger = DataLogger.FlightLogger()
        self.monitorDataLogger = DataLogger.DataLogger()
        self.T0 = 0.0
        self.events=[]

    def plot1(self, tr, hr):
        empty = [np.array([0]),np.array([0])]
        #self.plotPanel.draw([[tr,hr],empty,empty,empty,empty])
        self.plotPanel.draw([[tr,hr]])

    def plot2(self, tm, hm, vB, vD, vP):
        empty = [np.array([0]),np.array([0])]
        #self.plotPanel.draw([empty,[tm,hm],[tm,vB],[tm,vD],[tm,vP]])
        self.plotPanel.draw([[tm,hm]])
        self.plotPanel.draw2([[tm,vB],[tm,vD],[tm,vP]])

    def plot3(self, tr, hr, tm, hm, vB, vD, vP):
        #self.plotPanel.draw([[tr,hr],[tm,hm],[tm,vB],[tm,vD],[tm,vP]])
        self.plotPanel.draw([[tr,hr],[tm,hm]])
        self.plotPanel.draw2([[tm,vB],[tm,vD],[tm,vP]])

    def plotEvent(self, event):
        self.plotPanel.plotEvent(event,showH=False)

    def onBtnSetTitle( self, event ):
        txt = self.txtCtrlPlotTitle.GetValue()
        self.plotPanel.setTitle(txt)
 
    def onFileMonitorChanged( self, event ):
        self.uploadMonitorFile(self.filePickerMonitor.GetPath())
        self.replot()

    def onSpinCtrlDoubleT0( self, event ):
        self.T0 = self.spinCtrlDoubleT0.GetValue()
        self.replot()

    def onFilerRocketChanged( self, event ):
        self.uploadRRocketFile(self.filePickerrRocket.GetPath())
        self.replot()

    def replot(self):
        if len(self.rRocketDataLogger.t) > 0 and len(self.monitorDataLogger.t) > 0: 
            self.plotPanel.clearEvents()
            for evt in self.events:
                self.plotEvent(evt)
            self.plot3(self.rRocketDataLogger.t, 
                       self.rRocketDataLogger.h, 
                      self.monitorDataLogger.t-self.T0, 
                      self.monitorDataLogger.h,
                      self.monitorDataLogger.vB,
                      self.monitorDataLogger.vD,
                      self.monitorDataLogger.vP
                      )
        elif len(self.rRocketDataLogger.t) > 0:
            for evt in self.events:
                self.plotEvent(evt)
            self.plot1(self.rRocketDataLogger.t, self.rRocketDataLogger.h)
        elif len(self.monitorDataLogger.t) > 0:
            self.plot2(self.monitorDataLogger.t-self.T0, 
                    self.monitorDataLogger.h,
                    self.monitorDataLogger.vB,
                    self.monitorDataLogger.vD,
                    self.monitorDataLogger.vP
                    )
            
    def uploadRRocketFile(self, filename):
        if filename == "":
            dlg = ModelessDialog(self, "Erro", "Por favor, selecione um arquivo válido (rRocket).", delayMS=5000)
            dlg.Show()
            return False
        try:
            ifile=filename
            ofile=self.rrocketfilename

            # Creating tmp directory, if not exist yet
            os.makedirs(self.tmpFolder, exist_ok = True)

            self.events = getFlightEvents(filename)
            
            FlightDataImporter.removeHeaderLinesFromFile(ifile,ofile,self.inputFileFormat.headerLines)
            if self.inputFileFormat.fieldSeparator == "," and self.inputFileFormat.decimalSeparator==",":
                FS = ";"
                FlightDataImporter.replaceStrInFile(ofile,ofile,", ",FS)
            else:
                FS = self.inputFileFormat.fieldSeparator
                        
            if self.inputFileFormat.decimalSeparator == ",":
                FlightDataImporter.replaceStrInFile(ofile,ofile,",",".")

            tCol = self.inputFileFormat.tCol-1
            hCol = self.inputFileFormat.hCol-1

            data = FlightDataImporter.importData(ofile,cols=[tCol,hCol],sep=FS, engine="python",comment=self.inputFileFormat.comment)

            # Converts the altitude unit to meter
            data[1] = data[1] * self.inputFileFormat.hUnit
            
            self.rRocketDataLogger.t = data[0]
            self.rRocketDataLogger.h = data[1]
            
            return True
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            dlg = ModelessDialog(self, "Erro", "Falha ao carregar arquivo (rRocket).\n", delayMS=5000)
            dlg.Show()
            self.rRocketDataLogger.clear()
            self.events=[]
            return False

    def uploadMonitorFile(self, filename):
        if filename == "":
            dlg = ModelessDialog(self, "Erro", "Por favor, selecione um arquivo válido (rRocket-Monitor).", delayMS=5000)
            dlg.Show()
            return False
        try:
            ifile=filename
            ofile=self.monitorfilename

            # Creating tmp directory, if not exist yet
            os.makedirs(self.tmpFolder, exist_ok = True)

            self.events = getFlightEvents(filename)
            
            FlightDataImporter.removeHeaderLinesFromFile(ifile,ofile,self.inputFileFormat.headerLines)
            if self.inputFileFormat.fieldSeparator == "," and self.inputFileFormat.decimalSeparator==",":
                FS = ";"
                FlightDataImporter.replaceStrInFile(ofile,ofile,", ",FS)
            else:
                FS = self.inputFileFormat.fieldSeparator
                        
            if self.inputFileFormat.decimalSeparator == ",":
                FlightDataImporter.replaceStrInFile(ofile,ofile,",",".")

            data = FlightDataImporter.importData(ofile,cols=[0,1,2,3,4],sep=FS, engine="python",comment=self.inputFileFormat.comment)
            
            self.monitorDataLogger.t = data[0]
            self.monitorDataLogger.h = data[1]
            self.monitorDataLogger.vB = data[2]
            self.monitorDataLogger.vD = data[3]
            self.monitorDataLogger.vP = data[4]
            
            return True
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            dlg = ModelessDialog(self, "Erro", "Falha ao carregar arquivo (rRocket-Monitor).\n", delayMS=5000)
            dlg.Show()
            self.monitorDataLogger.clear()
            return False


    def onBtnCalculate( self, event ):
        if len(self.rRocketDataLogger.t) > 0 and len(self.monitorDataLogger.t) > 0:   
            idxM = np.argmax(self.monitorDataLogger.h)
            idxR = np.argmax(self.rRocketDataLogger.h)
            t0 = self.monitorDataLogger.t[idxM]-self.rRocketDataLogger.t[idxR]

            N = 20
            objMin = 1E10
            iMin = 0
            dt=0.1
            for i in range(-N,N):
                t = t0 + i * dt
                obj = self.objFunction(t)
                if obj < objMin:
                    iMin = i
                    objMin = obj

            self.T0 = t0+iMin*dt
           
            self.spinCtrlDoubleT0.SetValue(self.T0)
            self.replot()

    def objFunction(self, t0):
        ts = self.monitorDataLogger.t-t0
        tmin = min(np.min(ts),np.min(self.rRocketDataLogger.t))
        tmax = max(np.max(ts),np.max(self.rRocketDataLogger.t))

        fm = FlightDataImporter.pathLinSpace(ts, self.monitorDataLogger.h, deltaT=0.1, tmin=tmin, tmax=tmax)
        fr = FlightDataImporter.pathLinSpace(self.rRocketDataLogger.t, self.rRocketDataLogger.h, deltaT=0.1, tmin=tmin, tmax=tmax)
        objF = np.sum( (fm[1]-fr[1])**2 )

        return objF

    def onBtnReport( self, event ):
        if len(self.rRocketDataLogger.t) > 0 and len(self.monitorDataLogger.t) > 0:
            log = []
            log.append("RELATÓRIO rRocket-Monitor   - "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            log.append("")
            log.append("")
            log.append("rRocket-Monitor-UI "+self.appversion)
            log.append("rRocket-Monitor "+self.parent.rRocketMonitorModel.firmwareVersion)
            log.append("")
            log.append("Arquivo de entrada (rRocket-Monitor): "+self.filePickerMonitor.GetPath())
            log.append("Arquivo de entrada (rRocket): "+self.filePickerrRocket.GetPath())
            log.append("")
            log.append("Deslocamento de tempo t0 entre as curvas hm(t-t0) e hr(t) (s) : %10.3f"%self.T0)
            log.append("")
            log.append("Legenda")
            log.append("t: tempo")
            log.append("hr: altura registrada pelo rRocket")
            log.append("hm: altura registrada pelo rRocket-Monitor")
            log.append("Vb: tensão na bateria")
            log.append("Vd: tensão no drogue")
            log.append("Vp: tensão no paraquedas")
            log.append("")
            log.append("%10s %10s %10s %10s %10s %10s"%("t (s)", "hr (m)", "hm (m)", "Vb (V)", "Vd (V)", "Vp (V)"))

            ts = self.monitorDataLogger.t-self.T0
            tmin = self.rRocketDataLogger.t[0]
            tmax = self.rRocketDataLogger.t[-1]

            fmh = FlightDataImporter.pathLinSpace(ts, self.monitorDataLogger.h, deltaT=0.1, tmin=tmin, tmax=tmax)
            fmB = FlightDataImporter.pathLinSpace(ts, self.monitorDataLogger.vB, deltaT=0.1, tmin=tmin, tmax=tmax)
            fmD = FlightDataImporter.pathLinSpace(ts, self.monitorDataLogger.vD, deltaT=0.1, tmin=tmin, tmax=tmax)
            fmP = FlightDataImporter.pathLinSpace(ts, self.monitorDataLogger.vP, deltaT=0.1, tmin=tmin, tmax=tmax)
            fr = FlightDataImporter.pathLinSpace(self.rRocketDataLogger.t, self.rRocketDataLogger.h, deltaT=0.1, tmin=tmin, tmax=tmax)

            log2 = []

            for i in range(0,len(fmh[0])):
                log2.append("%10.3f %10.3f %10.3f %10.3f %10.3f %10.3f"%(fmh[0][i], fr[1][i], fmh[1][i], fmB[1][i], fmD[1][i], fmP[1][i]))

            txt=""
            cmt="# "
            eol="\r\n"
            for line in log:
                txt = txt + cmt + line + eol

            for line in log2:
                txt = txt + line + eol

            reportFrm = ReportFrame(self)
            reportFrm.setText(txt)
            reportFrm.Show() 
        else:
            dlg = ModelessDialog(self, "Erro", "Sem dados suficientes para gerar relatório de comparação.", delayMS=5000)
            dlg.Show()
            return False

    def setDisconnectedAppearance(self):
        self.btnCalculate.Enable(True)
        self.btnReport.Enable(True)

    def setReadyAppearance(self):
        self.btnCalculate.Enable(True)
        self.btnReport.Enable(True)
