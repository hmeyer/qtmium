# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow,  QFileDialog,  QAction,  QMessageBox,  QLabel
from PyQt4.QtCore import pyqtSignature, Qt
from PyQt4 import Qsci,  QtCore

from Ui_mainwindow import Ui_MainWindow
from OCC.Display.qtDisplay import qtViewer3d

from collections import deque
from os import path

from evaluator import evaluator
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
        self.statuslabel = QLabel("")
        self.statusbar.addWidget(self.statuslabel)        
        self.filename = None
        self.changed = False
        self.object = None
        self.sourceEdit.setLexer(Qsci.QsciLexerPython())
        self.sourceEdit.setAutoIndent(True)
        self.sourceEdit.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)
        self.sourceEdit.setIndentationGuides(True)
        self.markerNumber = self.sourceEdit.markerDefine( Qsci.QsciScintilla.Circle)
        self.sourceEdit.setMarkerBackgroundColor( Qt.red,  self.markerNumber )
    
    def setup(self,  inputfile=''):
        h = self.size().height()
        self.splitterV.setSizes([h*4/5,  h/5])
        w = self.size().width()
        self.splitterH.setSizes([w/2,  w/2])
        self.glWidget._display.SetOrthographic(False)
        self.glWidget._display.EnableAntiAliasing()
        if inputfile!='':
            self.loadFile(inputfile)
        
    
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
            return self.on_actionSave_as_activated()
        else:
            with open(self.filename, 'w') as f:
                f.write(str( self.sourceEdit.text() ))
                self.changed = False
                self.statusbar.showMessage("{0} saved".format(self.filename),  2000)
                self.add_current_to_recent()
                self.updateTitle()
                return True
        return False
    
    @pyqtSignature("")
    def on_actionSave_as_activated(self):
        """
        Query Name, then save Object Code
        """
        self.filename = QFileDialog.getSaveFileName(self, 'Object File Name',  filter='*.py')
        if (self.filename):
            return self.on_action_Save_activated()
        return False
    
    @pyqtSignature("")
    def on_action_Open_activated(self):
        """
        Query Name, then open Object Code
        """
        if self.check_saved():
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
                self.statusbar.showMessage("STL exported",  2000)
    
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
            if self.check_saved():
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
        fn = str(self.filename)
        indicator = ''
        if self.changed: indicator = '*'
        self.setWindowTitle('qtmium - '+path.basename(fn) + indicator)

    @pyqtSignature("")
    def loadFile(self,  fname):
        """
        open Object Code
        """
        self.filename = str(fname)
        with open(fname, 'r') as f:
            self.sourceEdit.setText( f.read() )
            self.changed = False
            self.statusbar.showMessage("{0} loaded".format(self.filename),  2000)
        self.add_current_to_recent()
        self.updateTitle()
    
    def add_current_to_recent(self):
        settings = QtCore.QSettings()
        files = settings.value("recentFileList").toStringList()
        files.removeAll(self.filename)
        files.prepend(self.filename);
        while len(files) > MAX_RECENT_FILES:
            files = files[:-1]
        settings.setValue("recentFileList", files)
        settings.sync()
        self.updateRecentFileActions()
    
    @pyqtSignature("int, int")
    def on_sourceEdit_cursorPositionChanged(self, line, pos):
        self.statuslabel.setText("L:{0} C:{1}".format(line, pos))
        return True

    @pyqtSignature("")
    def on_sourceEdit_textChanged(self):
        if not self.changed:
            self.changed = True
            self.updateTitle()
        return True
    
    def check_saved(self):
        if self.changed:
            ret = QMessageBox.warning(self,  'Application', 
                "The Object has been modified.\nDo you want to save your changes?", 
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.on_action_Save_activated()
            elif ret == QMessageBox.Cancel:
                return False
        return True

    def closeEvent(self,  event):
        if self.check_saved():
            event.accept()
        else:
            event.ignore()
