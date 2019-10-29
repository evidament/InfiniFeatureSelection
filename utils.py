from numba import jit, prange, types, cffi_support
import numpy as np
import time
import sys
from _writer import ffi, lib
import _writer

BUFFER_SIZE = 100000

cffi_support.register_module(_writer)
write = _writer.lib.write_data

@jit((types.Array(types.float32, 2, "A"), types.Array(types.float32, 2, "A")), nopython=True, nogil=True, parallel=True, fastmath=True, cache=True)
def activity_score(a, _):
    """Calculate activity score for column pairs
    
    Args:
        a (np.array[np.float32]): 2d array with data
        combinations (np.array[np.int32]): array specifying combinations in format (index, col1_id, col2_id)
    
    Returns:
        np.array[np.float32]: 1D array with activity scores for each column pair
    """
    rows, cols = a.shape
    combinations_count = cols*cols

    iqr = np.zeros(cols, dtype=np.float32)
    rank_arr = np.zeros((cols, rows), dtype=np.float32)
    checkpoint = combinations_count//5

    for index_base in prange(0, cols*cols//BUFFER_SIZE):
        max_iqr = np.zeros(BUFFER_SIZE, dtype=np.float32)
        sp_coeff = np.zeros(BUFFER_SIZE, dtype=np.float32)

        for i in range(BUFFER_SIZE):
            index = index_base*BUFFER_SIZE + i

            j = index//cols
            k = index%cols

            if index%checkpoint==0:
                percent = int(index/combinations_count*100)
                print(percent, "%")

            if k<=j:
                continue

            col1 = a[:, j]
            col2 = a[:, k]
            if iqr[j]==0:
                iqr[j] = np.quantile(col1, 0.75)-np.quantile(col1, 0.25)
            if iqr[k]==0:
                iqr[k] = np.quantile(col2, 0.75)-np.quantile(col2, 0.25)

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

        res_iqr = ffi.from_buffer(max_iqr)
        res_sp = ffi.from_buffer(sp_coeff)
        write(res_iqr, res_sp, BUFFER_SIZE, float(index_base))