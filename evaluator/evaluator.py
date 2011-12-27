from RestrictedPython import compile_restricted, PrintCollector, Guards
from operator import getitem
import sys
import cadmium
import traceback
import re
import math

def safe_cadmium():
    return dict(
                Box = cadmium.Box, 
                Cone = cadmium.Cone, 
                Cylinder = cadmium.Cylinder, 
                Sphere = cadmium.Sphere, 
                Text = cadmium.Text, 
                Torus = cadmium.Torus, 
                Wedge = cadmium.Wedge, 
                Union = cadmium.Union, 
                X_axis = cadmium.X_axis, 
                Y_axis = cadmium.Y_axis, 
                Z_axis = cadmium.Z_axis, 
                )

def inplacevar_wrapper(op, x, y):
 	     globs = {'x': x, 'y': y}
 	     exec 'x'+op+'y' in globs
 	     return globs['x']

def safeEvaluate(src, stdout=sys.__stdout__, stderr=sys.__stderr__):
    """
    function allowing the safe evaluation of untrusted python code
    """
    try:
        code = compile_restricted( src, '<string>', 'exec')
    except SyntaxError as e:
        if len(e.args)==2:
            e.args = e.args + (e.args[0],  e.args[1][1],  e.args[1][2] )
        else:
            m = re.search('^Line (\d+): (.*)$',  e.args[0])
            if m:
                e.args = e.args + (m.group(2),  int(m.group(1)),  -1)
        return e

    class GeneralNonCollector:
        '''Redirect text to stdout'''
        def __init__(self):
            self.buffer = str()
        def write(self, text):
            self.buffer += text
            if text[-1] == "\n":
                stdout.write(self.buffer[:-1])
                self.buffer = str()

    restricted_globals = dict(__builtins__ = Guards.safe_builtins, 
        _print_ = GeneralNonCollector, 
        _getiter_ = list.__iter__ ,
        _write_ = Guards.full_write_guard, 
        _getattr_ = getattr,
        _getitem_ = getitem,
        _inplacevar_ = inplacevar_wrapper, 
        list = list, 
        dict = dict, 
        enumerate = enumerate, 
        math = math, 
        reduce = reduce, 
        map = map, 
        sum = sum)
    restricted_globals = dict(restricted_globals.items() + safe_cadmium().items())


    (ostdout, ostderr) = (sys.stdout,  sys.stderr)
    (sys.stdout,  sys.stderr) = (stdout, stderr)
    ex = None
    try:
        exec( code ) in restricted_globals
    except (AttributeError, NameError, TypeError,  ImportError) as e:
        (typ, val, tb) = sys.exc_info()
        e.args = e.args + (e.args[0],  traceback.extract_tb(tb)[-1][1], -1)
        ex = e
    finally:
        (sys.stdout,  sys.stderr) = (ostdout, ostderr)
    if ex:
        return ex

    if 'result' in restricted_globals:
        return restricted_globals['result']
    else:
        return None
