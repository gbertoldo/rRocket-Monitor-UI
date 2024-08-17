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

import numpy as np

class DataLogger:
  def __init__(self):
    self.clear()

  def clear(self):
    self.t = np.array([])
    self.h = np.array([])
    self.vB = np.array([])
    self.vD = np.array([])
    self.vP = np.array([])
    
  def appendData(self, t, h, vB, vD, vP):
    self.t = np.append( self.t, t )
    self.h = np.append( self.h, h )
    self.vB = np.append( self.vB, vB )
    self.vD = np.append( self.vD, vD )
    self.vP = np.append( self.vP, vP )

class FlightLogger:
  def __init__(self):
    self.clear()

  def clear(self):
    self.t = np.array([])
    self.h = np.array([])
    
  def appendData(self, t, h, vB, vD, vP):
    self.t = np.append( self.t, t )
    self.h = np.append( self.h, h )

