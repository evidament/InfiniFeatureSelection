from cffi import FFI
import numpy as np

def compile_writer():
    ffibuilder = FFI()

    ffibuilder.cdef(
        """
            void write_data(float* iqr, float* sp, int size, int cols, float index);
        """)

    ffibuilder.set_source("_writer",
        """
            #include "writer.h"
        """,
        sources=['writer.c'])  
    ffibuilder.compile(verbose=True)


if __name__ == "__main__":
    compile_writer()
    from _writer import ffi, lib

    iqr = np.ones(2).astype(np.float32)
    sp = np.ones(2).astype(np.float32)
    iqr[0] = 5

    iqr = ffi.from_buffer(iqr)
    sp = ffi.from_buffer(sp)

    lib.write_data(iqr, sp, 2, 2, 1)