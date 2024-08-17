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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import (
    FigureCanvasWxAgg as FigureCanvas,
    NavigationToolbar2WxAgg as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import numpy as np
# https://www.youtube.com/playlist?list=PLecOfLY9Yl9cqDZ1opVnWWfAxqrDgk-MH

class wxMultiPlotPanel(wx.Panel):
  def __init__(self, parent, plotstyles, fontsize, dpi, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.PanelNameStr, plotstyles2=[]):
    wx.Panel.__init__(self, parent=parent, id=id, pos=pos, size=size, style=style, name=name)

    plt.rcParams['font.size'] = str(fontsize)
 
    self.figure = Figure((3, 2), dpi)
    self.axes = self.figure.add_subplot(111)
 
    # FigureCanvas is a kind of wx.Panel for Matplotlib
    self.canvas = FigureCanvas(self, -1, self.figure)

    # Lets add a sizer to contain the canvas (Panel)
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.EXPAND)
    self.SetSizer(self.sizer)

    # Creating an empty plot
    self.plotstyles = plotstyles
    numberOfLines = len(plotstyles)
    command = "self.lines = self.axes.plot("
    x=np.array([])
    for i in range(0,numberOfLines-1):
      command = command + "x,x,plotstyles["+str(i)+"]['style'],"
    i = numberOfLines-1
    command = command + "x,x,plotstyles["+str(i)+"]['style'])"
    exec(command)

    for i in range(0,len(plotstyles)):
       self.lines[i].set_color(plotstyles[i]["color"])

    # Creating the second y axis
    self.plotstyles2 = plotstyles2
    if len(plotstyles2) > 0:
      self.axes2 = self.axes.twinx()
      numberOfLines = len(plotstyles2)
      command = "self.lines2 = self.axes2.plot("
      x=np.array([])
      for i in range(0,numberOfLines-1):
        command = command + "x,x,plotstyles2["+str(i)+"]['style'],"
      i = numberOfLines-1
      command = command + "x,x,plotstyles2["+str(i)+"]['style'])"
      exec(command)

      for i in range(0,len(plotstyles2)):
        self.lines2[i].set_color(plotstyles2[i]["color"])

    # Capturing mouse events
    self.canvas.mpl_connect('button_press_event', self.onClick)

    # Markers
    self.pointMarkers = []

    # Drawing the figure
    self.canvas.draw()

    # Now lets create a sizer on the parent widget to contain the current panel and to expand it
    bSizer = wx.BoxSizer(wx.VERTICAL)
    bSizer.Add(self, wx.ID_ANY, wx.LEFT | wx.TOP | wx.EXPAND | wx.ALL, 1)
    parent.SetSizer(bSizer)

    self.Fit()
    self.isDrawing=False

  def drawGeneric(self, vec, axes, lines):
    if self.isDrawing:
       return
    self.isDrawing = True
    numberOfLines = len(vec)
    
    isEmpty=True
    for i in range(0,numberOfLines):
      if vec[i][0].size > 0:
        isEmpty=False

    if isEmpty:
      xmin = 0
      xmax = 1
      ymin = 0
      ymax = 1
    else:
      xmin = 1e10
      xmax = -1e10
      ymin = 1e10
      ymax = -1e10

    for i in range(0,numberOfLines):
      if vec[i][0].size > 0:
        if np.min(vec[i][0]) < xmin:
          xmin = np.min(vec[i][0])
        if np.max(vec[i][0]) > xmax:
            xmax = np.max(vec[i][0])
        if vec[i][1].size > 0:
          if np.min(vec[i][1]) < ymin:
            ymin = np.min(vec[i][1])
        if np.max(vec[i][1]) > ymax:
            ymax = np.max(vec[i][1])

    dx = xmax-xmin
    xmin = xmin - 0.05*dx
    xmax = xmax + 0.05*dx
    dy = ymax-ymin
    ymin = ymin - 0.05*dy
    ymax = ymax + 0.05*dy

    axes.set_xlim(xmin,xmax)
    axes.set_ylim(ymin,ymax)    

    for i in range(0, numberOfLines):
      lines[i].set_data(vec[i][0], vec[i][1])

    self.canvas.draw()

    self.canvas.flush_events()
    self.isDrawing = False


  def draw(self, vec):
    self.drawGeneric(vec, self.axes, self.lines)

  def draw2(self, vec):
    self.drawGeneric(vec, self.axes2, self.lines2)

  def setXLabel(self, label):
    self.axes.set_xlabel(label,)

  def setYLabel(self, label):
    self.axes.set_ylabel(label)

  def setYLabel2(self, label):
    if self.axes2:
       self.axes2.set_ylabel(label)

  def setTitle(self, label):
    self.axes.set_title(label)
    self.UpdatePlot()

  def UpdatePlot(self):
    self.canvas.draw()
    self.canvas.flush_events()
    self.Refresh()

  def setLegend(self, *args, **kwargs):
    for i in range(0,len(self.plotstyles)):     
     self.lines[i].set_label(self.plotstyles[i]["title"])
    self.axes.legend(*args, **kwargs)
    

  def setLegend2(self, *args, **kwargs):
    for i in range(0,len(self.plotstyles2)):     
     self.lines2[i].set_label(self.plotstyles2[i]["title"])
    self.axes2.legend(*args, **kwargs)

  def setGrid(self):
    self.axes.grid()

  def addToolbar(self):
    self.toolbar = NavigationToolbar(self.canvas)
    self.toolbar.Realize()
    # By adding toolbar in sizer, we are able to put it at the bottom
    # of the frame - so appearance is closer to GTK version.
    self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
    # update the axes menu on the toolbar
    self.toolbar.update()

  def onClick(self, event):
    return
    # This function was disable because some bugs appear when the second y axis is added. 
    if event.xdata and event.ydata:
      x=event.xdata
      y=event.ydata

      # When the second axis is added y is always equal to y2. So it is necessary to remap.
      if len(self.lines2)>0:
        y1i, y1f = self.axes.get_ylim()
        y2i, y2f = self.axes2.get_ylim()
        if (y2f-y2i)>1E-16:
          y1 = (y1f-y1i)/(y2f-y2i)*(y-y2i)+y1i
        else:
          y1=y
      print(x,y,y1)

      if not self.addMarker(self.axes, self.lines, x, y1):
        if len(self.lines2)>0:
          self.addMarker(self.axes2, self.lines2, event.xdata, event.ydata)

  def addMarker(self, axes, lines, x, y):
    dx, dy = self.getPlotSize(axes)
    d2ref = dx**2 + dy**2
    xdata=np.array([])
    ydata=np.array([])
    for line in lines:
      xdata = np.append(xdata,line.get_xdata())
      ydata = np.append(ydata,line.get_ydata())
    ans = self.getClosestPlotPointInfo(axes, xdata, ydata, x, y)
    cp = ans["closestPoint"]
    d2 = ans["distSquared"]
    if (d2 < 0.000001 * d2ref ):
      self.clearPointMarkers()
      self.addPointMarker(axes, cp[0],cp[1])
      return True
    else:
      self.clearPointMarkers()
      return False

  def clearPointMarkers(self):
    for marker in self.pointMarkers:
          self.removePointMarker()

  def getClosestPointInfo(self, xdata, ydata, x, y):
    dx2 = (xdata-x)**2
    dy2 = (ydata-y)**2
    ds2 = dx2+dy2
    idx = np.argmin(ds2)
    ans={"closestPoint":[xdata[idx],ydata[idx]],"distSquared":ds2[idx]}
    return ans
  
  def getClosestPlotPointInfo(self, axes, xdata, ydata, x, y):
    rwidth, rheight = self.getPlotSize(axes)
    aspect = self.getFrameAspectRatio() 
    if aspect > 0 :
      rwidth = rwidth * aspect
    dx2 = (xdata-x)**2
    dy2 = ((ydata-y)*rwidth/rheight)**2
    ds2 = dx2+dy2
    idx = np.argmin(ds2)
    ans={"closestPoint":[xdata[idx],ydata[idx]],"distSquared":ds2[idx]}
    return ans

  def getFrameAspectRatio(self):
        width, height = self.GetSize()      
        # Calculating the aspect ratio
        if width != 0: 
            aspectRatio = height/width
        else:
            aspectRatio=0
        return aspectRatio

  def getPlotSize(self, axes):
    xLeft, xRight = axes.get_xlim()
    yLow, yHigh = axes.get_ylim()

    return [abs((xRight - xLeft)),abs((yHigh - yLow))]

  def addPointMarker(self, axes, x, y, annotate:bool = True, percentage:float=0.05):
      rwidth, rheight = self.getPlotSize(axes)
      rwidth = rwidth * percentage
      rheight = rheight * percentage
      aspect = self.getFrameAspectRatio() 
      if aspect > 0 :
        rwidth = rwidth * aspect
      label = f"({x:.2f}, {y:.1f})"
      contour = Rectangle((x-0.5*rwidth, y-0.5*rheight), rwidth, rheight, edgecolor='r', facecolor='none')  # Círculo vermelho sem preenchimento
      axes.add_patch(contour)
      if annotate:
        annotation = axes.annotate(label, xy=(x, y), xytext=(x+0.5*rwidth, y+0.5*rheight))
      else:
        annotation = None
      self.pointMarkers.append({"contour":contour,"annotation":annotation})
      self.canvas.draw()  

  def removePointMarker(self):
      if self.pointMarkers:
          marker = self.pointMarkers.pop()
          contour=marker["contour"]
          annotation=marker["annotation"]
          contour.remove()
          if annotation is not None:
              annotation.remove()
          self.canvas.draw() 