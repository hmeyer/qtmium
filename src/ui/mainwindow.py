# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow
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
        obj = evaluator.safeEvaluate(str( self.sourceEdit.toPlainText() ), out)
        self.glWidget._display.EraseAll()        
        self.glWidget._display.DisplayShape(obj.shape,  update = True)
