#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
from ui.mainwindow import MainWindow
from OCC.BRepPrimAPI import *

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Python script based CAD')
    parser.add_argument('inputfile',  nargs='?', default='')
    args = parser.parse_args()
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    ui.glWidget.InitDriver()
    ui.setup(args.inputfile)
    sys.exit(app.exec_())
