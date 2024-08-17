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

import wxpserial
import DataLogger


"""
    Codes for receiving messages from rRocket-Monitor
"""
class InputMessageCode:
    def __init__(self):
        self.inputData         = 1
        self.firmwareVersion   = 2

rRocketMonitorState = {"Disconnected":1, "Ready":2}

class rRocketMonitorModel(wxpserial.wxPSerial):
    def __init__(self, parent):
        wxpserial.wxPSerial.__init__(self, parent)

        self.icode = InputMessageCode()

        self.firmwareVersion = ""

        self.state = rRocketMonitorState["Disconnected"]
        
        self.createDataLogger()
        self.isRecording=False
        
    # Overriding the parent's method 
    def start(self, serialParameters: wxpserial.SerialParameters, notificationPeriod=250, parser=wxpserial.BracketsMessageParser("<",">")):
        wxpserial.wxPSerial.start(self, serialParameters, notificationPeriod,parser)
        self.clearDataLogger()
        self.setState(rRocketMonitorState["Ready"])

    # Overriding the parent's method 
    def stop(self):
        wxpserial.wxPSerial.stop(self)
        self.setState(rRocketMonitorState["Disconnected"])

    def setState(self, state):
        self.state = state
        for observer in self.observerList:
            observer.rRocketMonitorModelStateUpdate()

    def startRecording(self):
        self.clearDataLogger()
        self.isRecording=True

    def stopRecording(self):
        self.isRecording=False

    def report(self, cmt="# ", eol="\r\n"):
        log = []
        log.append("")
        log.append("Legenda")
        log.append("t: tempo")
        log.append("h: altura")
        log.append("VB: tensão na bateria")
        log.append("VD: tensão no drogue")
        log.append("VP: tensão no paraquedas")
        log.append("")
        log.append("%9s%11s%11s%11s%11s"%("t (s)","h (m)","VB (V)", "VD (V)", "VP (V)"))
        
        txt = ""
        for line in log:
            txt = txt + cmt + line + eol

        data = self.dataLogger
        log = []
        for i in range(0,len(data.t)):
            log.append("%11.3f%11.3f%11.3f%11.3f%11.3f"%(data.t[i], data.h[i], data.vB[i], data.vD[i], data.vP[i]))
        for line in log:
            txt = txt + line + eol

        return txt
    
    def createDataLogger(self):
        self.dataLogger = DataLogger.DataLogger()
        try:
          for observer in self.observerList:
            observer.rRocketMonitorModelDataUpdate()
        except:
            pass
        return 

    def clearDataLogger(self):
        self.dataLogger.clear()
        try:
          for observer in self.observerList:
            observer.rRocketMonitorModelDataUpdate()
        except:
            pass
        return 
    
    def notify(self, data):
        """
            Notify all observers about the news
        """
          
        if len(data["msgs"]) > 0:
            updatedData = False
            updatedParameters = False
            for msg in data["msgs"]:
                msgSplit = msg.split(",")
                code = int(msgSplit[0])
                if code == self.icode.inputData:
                    if self.isRecording:
                        t=float(msgSplit[1])*1E-3 # ms to s
                        h=float(msgSplit[2]) # m
                        vB=float(msgSplit[3]) # V
                        vD=float(msgSplit[4]) # V
                        vP=float(msgSplit[5]) # V
                        self.dataLogger.appendData(t, h, vB, vD, vP)
                        updatedData = True
                if code == self.icode.firmwareVersion:
                    self.firmwareVersion = msgSplit[1]
                    updatedParameters = True
            if updatedParameters:
                for observer in self.observerList:
                        observer.rRocketMonitorModelParameterUpdate()
            if updatedData:
                for observer in self.observerList:
                        observer.rRocketMonitorModelDataUpdate()
