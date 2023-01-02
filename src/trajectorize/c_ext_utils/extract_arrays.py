import numpy as np

from trajectorize._c_extension import ffi


def extract_double_array(c_ptr, shape: "tuple[int]") -> np.ndarray:
    '''
    Extracts and returns a copy of a C array of type double (float64)

    Parameters
    ----------
    c_ptr: cData
        cffi c pointer to array
    shape: tuple[int]
        shape of array

    Returns
    -------
    np.ndarray
        the processed array with the appropriate shape
    '''

    mem_size = 8 * np.prod(shape)

    arr = np.copy(np.frombuffer(ffi.buffer(c_ptr, mem_size), dtype=np.float64))

    arr.shape = shape

    return arr
