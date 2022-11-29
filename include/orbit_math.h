#ifndef _ORBIT_MATH_H
#define _ORBIT_MATH_H

#include <stdbool.h>

typedef union Vector3
{
    struct
    {
        double x;
        double y;
        double z;
    };
    double v[3];
} Vector3;

typedef union Matrix3
{
    struct
    {
        double m00, m01, m02;
        double m10, m11, m12;
        double m20, m21, m22;
    };
    double m[3][3];
} Matrix3;

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

#endif // _ORBIT_MATH_H_