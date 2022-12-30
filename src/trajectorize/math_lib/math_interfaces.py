import numpy as np

from trajectorize._c_extension import ffi


def vec3_from_np_array(np_array: np.ndarray) -> ffi.CData:
    return ffi.new("Vector3*", {"v": np_array.tolist()})[0]


def np_array_from_vec3(vec3: ffi.CData) -> np.ndarray:
    return np.copy(np.frombuffer(ffi.buffer(vec3.v, 3 * 8), dtype=np.float64))
