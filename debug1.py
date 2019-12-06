from ctypes import * 
blosc2 = cdll.LoadLibrary("build_dev/blosc/libblosc2.so.2.0.0")                                                                                                                                                          
import time

def display2(out, cmt=""):
    if not isinstance(out, numpy.ndarray):
        out = numpy.array(out)
    tmp = ["%02x"%i for i in out.ravel().view("uint8")]
    tmp2 = [ "|\n|"+j if i%32==0 else "|"+j if i%8==0 else " "+j for i,j in enumerate(tmp)]
    print(cmt+"".join(tmp2)+"| Σ: %i"%numpy.unpackbits(out.view("uint8")).sum())

import numpy                                                                                                                                                                                               
import bitshuffle

for i in range(7, 30):
    size = 1<<i
    a = numpy.random.randint(0, 128, size=size).astype("uint8")
    #display2(a, "inp")
    
    #display2(ref, "ref")
    b = numpy.empty_like(a)
    t0 = time.time()
    ref = bitshuffle.bitunshuffle(a, a.size)
    t1 = time.time()
    blosc2.bitunshuffle1_altivec(a.ctypes.data, b.ctypes.data, c_size_t(a.size), c_size_t(1))
    t2=time.time()
    print("size: %s, ref: %.3fGB/s, obt: %.3fGB/s"%(size, size/(t1-t0)/1e9, size/(t2-t1)/1e9))
    #display2(b, "obt")
    #ref = bitshuffle.bitshuffle(a, 2*a.size)
    #display2(b)
    if (abs(ref -b).max()):
        print(size)
        display2(a, "inp")
        display2(b, "obt")
        display2(ref,"ref")
        print(abs(ref-b).max())
        print(numpy.where(ref - b))
        break
        
        
