from numba import jit, prange, types, cffi_support
import numpy as np
import time
import sys
from _writer import ffi, lib
import _writer
# from ._writer import ffi, lib
# from . import _writer


cffi_support.register_module(_writer)
write = _writer.lib.write_data

@jit((types.Array(types.float32, 2, "A"), types.int32), nopython=True, nogil=True, parallel=True, fastmath=True, cache=False)
def activity_score(a, buffer_size):
    """Calculate activity score for column pairs
    
    Args:
        a (np.array[np.float32]): 2d array with data
        combinations (np.array[np.int32]): array specifying combinations in format (index, col1_id, col2_id)
    
    Returns:
        np.array[np.float32]: 1D array with activity scores for each column pair
    """

    rows, cols = a.shape
    combinations_count = cols*cols
    returnable = False
    
    if combinations_count<buffer_size:
        buffer_size = combinations_count+1
        returnable = True

    iqr = np.zeros(cols, dtype=np.float32)
    rank_arr = np.zeros((cols, rows), dtype=np.float32)
    checkpoint = combinations_count//5

    for index_base in prange(0, combinations_count//buffer_size+1):
        max_iqr = np.zeros(buffer_size, dtype=np.float32)
        sp_coeff = np.zeros(buffer_size, dtype=np.float32)

        for i in range(buffer_size):
            index = index_base*buffer_size + i
            j = index//cols
            k = index%cols

            if index%checkpoint==0:
                percent = int(index/combinations_count*100)
                if index>combinations_count:
                    break
                print(percent, "%")

            if k<=j:
                continue

            col1 = a[:, j]
            col2 = a[:, k]
            if iqr[j]==0:
                iqr[j] = np.abs(np.quantile(col1, 0.75)-np.quantile(col1, 0.25))
            if iqr[k]==0:
                iqr[k] = np.abs(np.quantile(col2, 0.75)-np.quantile(col2, 0.25))

            if rank_arr[j][0]==0:
                temp = col1.argsort()
                rank_arr[j][temp] = np.arange(1, rows+1)
            if rank_arr[k][0]==0:
                temp = col2.argsort()
                rank_arr[k][temp] = np.arange(1, rows+1)

            m_iqr = np.max(np.array([iqr[j], iqr[k]]))

            sum_diff_sq = np.sum(np.power(np.subtract(rank_arr[j],rank_arr[k]),2))
            rho = 1 - ((6*sum_diff_sq/(rows*(rows**2-1))))
            max_iqr[i] = m_iqr
            sp_coeff[i] = 1-rho

        write(max_iqr.ctypes, sp_coeff.ctypes, buffer_size, cols, float(index_base))
        if returnable:
            return max_iqr, sp_coeff