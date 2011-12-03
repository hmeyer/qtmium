from PyQt4 import QtCore, QtGui
from ui.mainwindow import MainWindow
#from qtmium import solid
from OCC.BRepPrimAPI import *


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    ui.glWidget.InitDriver()
    sys.exit(app.exec_())