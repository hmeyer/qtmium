# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow,  QFileDialog,  QAction
from PyQt4.QtCore import pyqtSignature, Qt
from PyQt4 import Qsci,  QtCore

from Ui_mainwindow import Ui_MainWindow
from OCC.Display.qtDisplay import qtViewer3d

from collections import deque
from os import path

import evaluator
import exceptions
import sys
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

MAX_RECENT_FILES = 5

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.errorMarker  = None
        self.setupUi(self)
        self.create_recentFileActs()
        self.create_exampleActs()
        self.updateRecentFileActions()
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
            else:
                self.displayError(result)
    
    def displayError(self, e):
        d = e.args[-3]
        line = e.args[-2]
        self.errorMarker = self.sourceEdit.markerAdd(line-1, self.markerNumber)
        col = e.args[-1]
        if not col == -1:
            self.consoleEdit.setPlainText('Error in line {0}, column {1}: {2}'.format(line,  col, d))
            self.sourceEdit.setCursorPosition(line-1,  col-1)
        else:
            self.consoleEdit.setPlainText('Error in line {0}: {1}'.format(line,  d))
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
        self.loadFile(QFileDialog.getOpenFileName(self, 'Object File Name',  filter='*.py'))
    
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

    @pyqtSignature("")
    def on_open_menu_file(self):
        """
        open recent/example file
        """
        action = self.sender()
        if action:
            self.loadFile( action.data().toString() )

    @pyqtSignature("")
    def create_recentFileActs(self):
        """
        Create Actions to open recent files
        """
        self.recentFileActs = deque()
        for i in range(MAX_RECENT_FILES):
            a = QAction(self)
            a.setVisible(False)
            QtCore.QObject.connect(a, QtCore.SIGNAL(_fromUtf8("triggered()")), self.on_open_menu_file)
            self.menuRecent.addAction(a)
            self.recentFileActs.append(a)

    def create_exampleActs(self):
        """
        Create Actions to open example files
        """
        exdir = None
        self.menuExamples.menuAction().setVisible(False)
        bpath = sys.path[0] + os.sep
        for p in ['../share/openscadpy/examples',
            '../../share/openscadpy/examples',
            '../../examples','../examples','examples']:
            exdir = bpath + p
            if os.access(exdir,  os.R_OK ):
                break
            else:
                exdir = None
        if not exdir:
            return
        
        for e in sorted(os.listdir(exdir)):
            if e[-3:] == '.py':
                fname = exdir + os.sep + e
                a = QAction(self)
                QtCore.QObject.connect(a, QtCore.SIGNAL(_fromUtf8("triggered()")), self.on_open_menu_file)
                a.setText(e)
                a.setData(fname)
                self.menuExamples.addAction(a)
                self.menuExamples.menuAction().setVisible(True)
        

    @pyqtSignature("")
    def updateRecentFileActions(self):
        """
        Update the list of recent Files
        """ 
        settings = QtCore.QSettings()
        files = settings.value("recentFileList").toStringList()
        
        for i,  f in enumerate(files):
            self.recentFileActs[i].setText(path.basename(str(f)))
            self.recentFileActs[i].setData(f)
            self.recentFileActs[i].setVisible(True)
        
        for i in range(len(files), MAX_RECENT_FILES):
            self.recentFileActs[i].setVisible(False)
            
        self.menuRecent.menuAction().setVisible(len(files)>0)

    @pyqtSignature("")
    def updateTitle(self):
        self.setWindowTitle('qtmium - '+path.basename(self.filename))

    @pyqtSignature("")
    def loadFile(self,  fname):
        """
        open Object Code
        """
        self.filename = str(fname)
        with open(fname, 'r') as f:
            self.sourceEdit.setText( f.read() )

        settings = QtCore.QSettings()
        files = settings.value("recentFileList").toStringList()
        
        files.removeAll(fname)
        files.prepend(fname);
        while len(files) > MAX_RECENT_FILES:
            files = files[:-1]
        settings.setValue("recentFileList", files)
        settings.sync()
        self.updateRecentFileActions()
        self.updateTitle()
