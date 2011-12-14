# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow,  QFileDialog
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import Qt
from PyQt4 import Qsci

from Ui_mainwindow import Ui_MainWindow
from OCC.Display.qtDisplay import qtViewer3d

import evaluator
import exceptions

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.glWidget = qtViewer3d()
        self.splitterH.addWidget(self.glWidget)
        self.filename = None
        self.object = None
        self.sourceEdit.setLexer(Qsci.QsciLexerPython())
        self.sourceEdit.setAutoIndent(True)
        self.sourceEdit.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)
        self.sourceEdit.setIndentationGuides(True)
        self.sourceEdit.setText(
'''#press F8 to compile
result = (
  Torus(70,69) - 
  Text('Hello World', 
    fontpath='/usr/share/fonts/truetype/freefont/FreeSans.ttf', 
    height = 40, thickness = 150, center=True) 
  - Torus(130,20).rotate(Y_axis,30)
  )''')
        self.markerNumber = self.sourceEdit.markerDefine( Qsci.QsciScintilla.Circle)
        self.sourceEdit.setMarkerBackgroundColor( Qt.red,  self.markerNumber )
        self.errorMarker  = None
    
    def setup(self):
        h = self.size().height()
        self.splitterV.setSizes([h*4/5,  h/5])
        w = self.size().width()
        self.splitterH.setSizes([w/2,  w/2])
    
    @pyqtSignature("")
    def on_action_Compile_activated(self):
        """
        Public slot invoked when the user selects the compile action
        """
        class OutPutter:
            def __init__(self, widget):
                self.w = widget
                self.w.clear()
            def write(self, txt):
                self.w.appendPlainText(str(txt).rstrip())
        out = OutPutter(self.consoleEdit)
        result = evaluator.safeEvaluate(str( self.sourceEdit.text() ), out)
        self.glWidget._display.EraseAll()
        self.object = None
        if result:
            import cadmium
            if isinstance(result, cadmium.solid.Solid):
                self.object = result
                self.glWidget._display.DisplayShape(self.object.shape,  update = True)
            elif isinstance(result, exceptions.SyntaxError):
                self.displayCompileError(result)
            else:
                self.displayOtherError(result)
    
    def displayCompileError(self, e):
        d = e.args[0]
        line = e.args[1][1]
        col = e.args[1][2]
        self.consoleEdit.setPlainText('Error in line {0}, column {1}: {2}'.format(line,  col, d))
        self.errorMarker = self.sourceEdit.markerAdd(line-1, self.markerNumber)
        self.sourceEdit.setCursorPosition(line-1,  col-1)

    def displayOtherError(self, e):
        self.consoleEdit.setPlainText(e.__class__.__name__+":"+str(e.args[0]))
        line = e.args[-1][1]
        self.errorMarker = self.sourceEdit.markerAdd(line-1, self.markerNumber)
        self.sourceEdit.setCursorPosition(line-1,  0)


    @pyqtSignature("")
    def on_action_Save_activated(self):
        """
        Save Object Code
        """
        if (not self.filename):
            self.on_actionSave_as_activated()
        else:
            with open(self.filename, 'w') as f:
                f.write(str( self.sourceEdit.text() ))
    
    @pyqtSignature("")
    def on_actionSave_as_activated(self):
        """
        Query Name, then save Object Code
        """
        self.filename = QFileDialog.getSaveFileName(self, 'Object File Name',  filter='*.py')
        if (self.filename):
            self.on_action_Save_activated()
    
    @pyqtSignature("")
    def on_action_Open_activated(self):
        """
        Query Name, then open Object Code
        """
        self.filename = QFileDialog.getOpenFileName(self, 'Object File Name',  filter='*.py')
        with open(self.filename, 'r') as f:
            self.sourceEdit.setText( f.read() )
    
    @pyqtSignature("")
    def on_actionE_xport_STL_activated(self):
        """
        Query Name, then save STL
        """
        if (self.object):
            stlname = str(QFileDialog.getSaveFileName(self, 'STL File Name',  filter='*.stl'))
            if (stlname):
                self.object.toSTL(filename = stlname)
    
    @pyqtSignature("")
    def on_sourceEdit_textChanged(self):
        """
        Delete all markers, when Text changed
        """
        if self.errorMarker:
            self.sourceEdit.markerDeleteHandle(self.errorMarker)
            self.errorMarker = None
