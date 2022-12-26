import numpy as np

from trajectorize._c_extension import ffi


def vec3_from_np_array(np_array: np.ndarray) -> ffi.CData:
    return ffi.new("Vector3*", {"v": np_array.tolist()})[0]
