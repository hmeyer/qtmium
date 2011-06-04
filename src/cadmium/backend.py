# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

from ctypes import *

libcsg = cdll.LoadLibrary('build/libcsgop.so')

csgop = libcsg.csgop
csgop_simple = libcsg.csgop_simple

ERR_NOT_SIMPLE = libcsg.ERR_NOT_SIMPLE
OP_UNION = libcsg.OP_UNION
OP_INTERSECTION = libcsg.OP_INTERSECTION
OP_SUBTRACTION = libcsg.OP_SUBTRACTION

PDOUBLE = POINTER(c_double)
PPDOUBLE = POINTER(PDOUBLE)
PINT = POINTER(c_int)
PPINT = POINTER(PINT)
DBLARR = c_double * 3
INTARR = c_int * 3

# Function prototype
csgop.argtypes = [ 
  PPDOUBLE, c_int, c_int, PPINT, c_int, c_int,
  PPDOUBLE, c_int, c_int, PPINT, c_int, c_int, c_int ]

# Function return data type
PPDOUBLE = POINTER(POINTER(c_double))
PPINT = POINTER(POINTER(c_int))

class PolyPack(Structure):
  _fields_ = [
              ('error', c_int),
              ('num_vertices', c_int),
              ('num_faces', c_int),
              ('vertices', PPDOUBLE),
              ('faces', PPINT),
              ]

csgop.restype = POINTER(PolyPack)

csgop_simple.argtypes = [ c_char_p, c_char_p, c_int ]
csgop_simple.restype = c_int

free_ppack = libcsg.free_ppack
free_ppack.argtypes = [ POINTER(PolyPack) ]
free_ppack.restype = None
