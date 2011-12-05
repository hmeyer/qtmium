# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow,  QFileDialog
from PyQt4.QtCore import pyqtSignature

from Ui_mainwindow import Ui_MainWindow
from OCC.Display.qtDisplay import qtViewer3d

import evaluator

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
        self.splitter.addWidget(self.glWidget)
        self.filename = None
        self.object = None
    
    def setup(self):
        size = self.splitter.size().width()
        self.splitter.setSizes([size/2,  size/2])
    
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
        out = OutPutter(self.console)
        self.object = evaluator.safeEvaluate(str( self.sourceEdit.toPlainText() ), out)
        self.glWidget._display.EraseAll()        
        self.glWidget._display.DisplayShape(self.object.shape,  update = True)
    
    @pyqtSignature("")
    def on_action_Save_activated(self):
        """
        Save Object Code
        """
        if (not self.filename):
            self.on_actionSave_as_activated()
        else:
            with open(self.filename, 'w') as f:
                f.write(str( self.sourceEdit.toPlainText() ))
    
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
            self.sourceEdit.setPlainText( f.read() )
    
    @pyqtSignature("")
    def on_actionE_xport_STL_activated(self):
        """
        Query Name, then save STL
        """
        if (self.object):
            stlname = str(QFileDialog.getSaveFileName(self, 'STL File Name',  filter='*.stl'))
            if (stlname):
                self.object.toSTL(filename = stlname)
