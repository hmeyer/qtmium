#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
from ui.mainwindow import MainWindow
from OCC.BRepPrimAPI import *


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    ui.glWidget.InitDriver()
    ui.setup()
    sys.exit(app.exec_())
