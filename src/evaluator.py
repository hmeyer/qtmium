from RestrictedPython import compile_restricted, PrintCollector, Guards
import sys
import cadmium

def safe_cadmium():
    return dict(
                Box = cadmium.Box, 
                Cone = cadmium.Cone, 
                Cylinder = cadmium.Cylinder, 
                Sphere = cadmium.Sphere, 
                Text = cadmium.Text, 
                Torus = cadmium.Torus, 
                Wedge = cadmium.Wedge, 
                X_axis = cadmium.X_axis, 
                Y_axis = cadmium.Y_axis, 
                Z_axis = cadmium.Z_axis
                )

def safeEvaluate(src, stdout=sys.__stdout__, stderr=sys.__stderr__):
    """
    function allowing the safe evaluation of untrusted python code
    """
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
        _getattr_ = getattr)
        
    restricted_globals = dict(restricted_globals.items() + safe_cadmium().items())

    code = compile_restricted( src, '<string>', 'exec')
    (ostdout, ostderr) = (sys.stdout,  sys.stderr)
    (sys.stdout,  sys.stderr) = (stdout, stderr)
    exec( code ) in restricted_globals
    (sys.stdout,  sys.stderr) = (ostdout, ostderr)

    if 'result' in restricted_globals:
        return restricted_globals['result']
    else:
        return None
