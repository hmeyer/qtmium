#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
from ui.mainwindow import MainWindow
from OCC.BRepPrimAPI import *
import sys
    

def generateSTL(inputfilename,  outputfilename,  precision):
    with open(inputfilename, 'r') as f:
        input = f.read()
        from evaluator import evaluator
        result = evaluator.safeEvaluate(input, sys.stdout)
        if result:
            import cadmium
            if isinstance(result, cadmium.solid.Solid):
                result.toSTL(filename = outputfilename,  deflection=precision)    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Python script based CAD')
    parser.add_argument('inputfile',  nargs='?', default='')
    parser.add_argument('-x', '--export',  nargs=1,  help='export STL to file')
    parser.add_argument('-p', '--precision',  nargs=1,  help='smallest error',  default=[0.01])
    args = parser.parse_args()
    if args.export:
        generateSTL(args.inputfile,  args.export[0],  float(args.precision[0] ) )
        exit()
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    ui.glWidget.InitDriver()
    ui.setup(args.inputfile)
    sys.exit(app.exec_())

