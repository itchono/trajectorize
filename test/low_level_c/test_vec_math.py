import pytest
import numpy as np

from trajectorize.math_lib.math_interfaces import vec3_from_np_array, \
    np_array_from_vec3
from trajectorize._c_extension import ffi, lib


# initialize some test vectors
# a = [1, 2, 3]
# b = [4, 5, 6]
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
a_c = vec3_from_np_array(a)
b_c = vec3_from_np_array(b)


def test_dot_product():
    dot_product = lib.vec_dot(a_c, b_c)

    assert dot_product == pytest.approx(a @ b)


def test_cross_product():
    cross_product = lib.vec_cross(a_c, b_c)
    cross_product_np = np.cross(a, b)

    assert cross_product_np == pytest.approx(np_array_from_vec3(cross_product))


def test_norm():
    norm = lib.vec_norm(a_c)
    norm_np = np.linalg.norm(a)

    assert norm_np == pytest.approx(norm)


def test_normalize():
    a_normalized = lib.vec_normalized(a_c)
    a_normalized_np = a / np.linalg.norm(a)

    assert a_normalized_np == pytest.approx(np_array_from_vec3(a_normalized))


def test_vec3_from_np_array():
    assert a_c.x == a[0]
    assert a_c.y == a[1]
    assert a_c.z == a[2]


def test_vec_add():
    c_c = lib.vec_add(a_c, b_c)
    c = np_array_from_vec3(c_c)

    assert c == pytest.approx(a + b)


def test_vec_sub():
    c_c = lib.vec_sub(a_c, b_c)
    c = np_array_from_vec3(c_c)

    assert c == pytest.approx(a - b)
