import numpy as np

from trajectorize._c_extension import ffi, lib


def process_sva_buffer(sva_struct, length: int) -> np.ndarray:
    # Process memory buffer
    # Format: [x, y, z, vx, vy, vz, t] x n
    arr = np.frombuffer(ffi.buffer(sva_struct.mem_buffer, 7 *
                                   8 * length), dtype=np.float64)
    arr.shape = (length, 7)
    copied_arr = np.copy(arr)

    # Free memory
    lib.free_StateVectorArray(sva_struct)

    return copied_arr
