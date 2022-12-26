/*
Trajectorize

Math Library

This header file contains a library of math functions.
*/

#ifndef ORBIT_MATH_H
#define ORBIT_MATH_H

#include <stdbool.h>
#include "orbit_math_types.h"

double norm(Vector3 v);
double dot(Vector3 v1, Vector3 v2);
Vector3 cross(Vector3 v1, Vector3 v2);
Vector3 normalize(Vector3 v);
Vector3 vec_zero();

Vector3 add_vec(Vector3 v1, Vector3 v2);
Vector3 sub_vec(Vector3 v1, Vector3 v2);
Vector3 mul_scalar_vec(double s, Vector3 v);

Matrix3 identity();
Matrix3 mat_zero();
Matrix3 transpose(Matrix3 m);
Matrix3 mul_scalar_mat(double s, Matrix3 m);
Matrix3 mul_mat(Matrix3 m1, Matrix3 m2);

Vector3 mul_mat_vec(Matrix3 m, Vector3 v);

// Comparisons
bool vec_equal(Vector3 v1, Vector3 v2);
bool mat_equal(Matrix3 m1, Matrix3 m2);

// Output
void print_vec(Vector3 v);
void print_mat(Matrix3 m);

#endif // ORBIT_MATH_H