#!/usr/bin/python3
import sys
import numpy
from ctypes import *
import time
from math import ceil
from collections import OrderedDict, namedtuple
Result = namedtuple("Res", "flux reflux")
#%matplotlib nbagg
from matplotlib.pylab import subplots
blosc2 = cdll.LoadLibrary("build_dev/blosc/libblosc2.so.2.0.0")
import gc 
gc.disable()
if len(sys.argv)>1:
    dtype = numpy.dtype(sys.argv[1])
else:
    dtype = numpy.dtype("int64")
if dtype.kind=="i":
    maxi = 1<<(dtype.itemsize*8-2)
    print("Max random value", maxi)

def display(out):
    tmp = ["%2s"%hex(i)[2:] for i in out.view("uint8")]
    tmp2 = [ " "+j if i%16 else "\n %s| %s"%(i//16,j) for i,j in enumerate(tmp)]
    return "".join(tmp2)+" sum: %i"%numpy.unpackbits(out.view("uint8")).sum()

def display2(out):
    tmp = ["%2s"%hex(i)[2:] for i in out.view("uint8")]
    tmp2 = [ "" if i%16>2 else " "+j for i,j in enumerate(tmp)]
    return "".join(tmp2)+" sum: %i"%numpy.unpackbits(out.view("uint8")).sum()


for size in range(10,512):
    if dtype.kind=="i":
        inp = numpy.random.randint(0,maxi, size=size).astype(dtype)
    elif dtype.kind=="c":
        inp = (numpy.random.random(size=size)+complex(0,1)*numpy.random.random(size=size)).astype(dtype)
    else:
        inp = numpy.random.random(size=size).astype(dtype)
    #Test misaligned read
    #inp = inp[1:]
    ref = numpy.empty_like(inp)
    out = numpy.empty_like(inp)
    tmp_buf = numpy.empty_like(inp)
    tmp = numpy.empty_like(inp)
    type_size = c_int32(numpy.dtype(inp.dtype).itemsize)
    size = c_int32(inp.size)
    blosc2.bshuf_trans_bit_elem_scal(inp.ctypes.data, ref.ctypes.data, size, type_size, tmp_buf.ctypes.data)
    blosc2.bshuf_trans_bit_elem_altivec(inp.ctypes.data, ref.ctypes.data, size, type_size, tmp_buf.ctypes.data)
    if abs(ref-out).max()>0:
        print("\nError bitshuffle for size",size,"\ninp ", display(inp),"\nout ", display(out),"\nref ", display(ref))
        break
    blosc2.bshuf_untrans_bit_elem_scal(ref.ctypes.data, tmp.ctypes.data, size, type_size, tmp_buf.ctypes.data)
    if abs(tmp-inp).max()>0:
        print("Error in bitunshuffle generic for size", size, "\nout ", display(out),"\ninp ", display(inp),"\ngot ", display(tmp))
        break
    blosc2.bshuf_untrans_bit_elem_altivec(out.ctypes.data, tmp.ctypes.data, size, type_size, tmp_buf.ctypes.data)
    if abs(tmp-inp).max()>0:
        print("Error in bitunshuffle altivec for size", size, "\nout ", display(out), "\ninp ", display(inp),"\n\ngot ", display(tmp))
        break
    sys.stdout.write(" %i"%size)
print("Giving up")
