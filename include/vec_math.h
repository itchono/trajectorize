/*
Trajectorize

Vector Math Library

This header file contains a library of math functions.
*/

#ifndef VEC_MATH_H
#define VEC_MATH_H

#include <stdbool.h>
#include "vec_math_types.h"

double vec_norm(Vector3 v);
double vec_dot(Vector3 v1, Vector3 v2);
Vector3 vec_cross(Vector3 v1, Vector3 v2);
Vector3 vec_normalized(Vector3 v);
Vector3 vec_zero();

Vector3 vec_add(Vector3 v1, Vector3 v2);
Vector3 vec_sub(Vector3 v1, Vector3 v2);
Vector3 vec_mul_scalar(double s, Vector3 v);

Matrix3 mat_identity();
Matrix3 mat_zero();
Matrix3 mat_transpose(Matrix3 m);
Matrix3 mat_mul_scalar(double s, Matrix3 m);
Matrix3 mat_mul_mat(Matrix3 m1, Matrix3 m2);

Vector3 mat_mul_vec(Matrix3 m, Vector3 v);

// Comparisons
bool vec_equal(Vector3 v1, Vector3 v2);
bool mat_equal(Matrix3 m1, Matrix3 m2);

// Output
void print_vec(Vector3 v);
void print_mat(Matrix3 m);

#endif // VEC_MATH_H