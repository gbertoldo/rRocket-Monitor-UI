"""
  The MIT License (MIT)
 
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

class ModelessDialog(UITemplate.ModelessDialog):
    def __init__(self, parent, title, message, delayMS=0):
        UITemplate.ModelessDialog.__init__(self, parent)
        self.SetTitle(title)
        self.txtMessage.SetLabel(title)
        szTitle = self.txtMessage.GetSize()
        self.txtMessage.SetLabel(message)
        szMsg = self.txtMessage.GetSize()
        szBtn = self.btnOk.GetSize()
        width = 100
        if szTitle[0] > szMsg[0]:
            width = width + szTitle[0]
        else:
            width = width + szMsg[0]
        height = szMsg[1]+szBtn[1]+80
        self.SetSize(width, height)
        self.Layout()
        if delayMS > 0:
          self.timer = wx.Timer(self)
          self.Bind(wx.EVT_TIMER, self.onBtnOk, self.timer)
          self.timer.Start(delayMS, oneShot=wx.TIMER_ONE_SHOT)
    def onBtnOk( self, event ):
        self.Destroy()

if __name__ == "__main__":
    app = wx.App()

    frm = ModelessDialog(None, "Estado da memória de voo", "Memória de voo vazia", delayMS=2000)
    frm.Show()
    app.MainLoop()