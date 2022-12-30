#include "vec_math.h"

#include <math.h>
#include <stdio.h>

double vec_norm(Vector3 v)
{
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
}

double vec_dot(Vector3 a, Vector3 b)
{
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

Vector3 vec_cross(Vector3 a, Vector3 b)
{
    Vector3 result;
    result.x = a.y * b.z - a.z * b.y;
    result.y = a.z * b.x - a.x * b.z;
    result.z = a.x * b.y - a.y * b.x;
    return result;
}

Vector3 vec_normalized(Vector3 v)
{
    double n = vec_norm(v);
    Vector3 result;
    result.x = v.x / n;
    result.y = v.y / n;
    result.z = v.z / n;
    return result;
}

Vector3 vec_zero()
{
    Vector3 result;
    result.x = 0;
    result.y = 0;
    result.z = 0;
    return result;
}

Vector3 vec_add(Vector3 a, Vector3 b)
{
    Vector3 result;
    result.x = a.x + b.x;
    result.y = a.y + b.y;
    result.z = a.z + b.z;
    return result;
}

Vector3 vec_sub(Vector3 a, Vector3 b)
{
    Vector3 result;
    result.x = a.x - b.x;
    result.y = a.y - b.y;
    result.z = a.z - b.z;
    return result;
}

Vector3 vec_mul_scalar(double s, Vector3 v)
{
    Vector3 result;
    result.x = s * v.x;
    result.y = s * v.y;
    result.z = s * v.z;
    return result;
}

Matrix3 mat_identity()
{
    Matrix3 result;
    result.m[0][0] = 1.0;
    result.m[0][1] = 0.0;
    result.m[0][2] = 0.0;
    result.m[1][0] = 0.0;
    result.m[1][1] = 1.0;
    result.m[1][2] = 0.0;
    result.m[2][0] = 0.0;
    result.m[2][1] = 0.0;
    result.m[2][2] = 1.0;
    return result;
}

Matrix3 mat_zero()
{
    Matrix3 result;
    result.m[0][0] = 0.0;
    result.m[0][1] = 0.0;
    result.m[0][2] = 0.0;
    result.m[1][0] = 0.0;
    result.m[1][1] = 0.0;
    result.m[1][2] = 0.0;
    result.m[2][0] = 0.0;
    result.m[2][1] = 0.0;
    result.m[2][2] = 0.0;
    return result;
}

Matrix3 mat_transpose(Matrix3 m)
{
    Matrix3 result;
    result.m[0][0] = m.m[0][0];
    result.m[0][1] = m.m[1][0];
    result.m[0][2] = m.m[2][0];
    result.m[1][0] = m.m[0][1];
    result.m[1][1] = m.m[1][1];
    result.m[1][2] = m.m[2][1];
    result.m[2][0] = m.m[0][2];
    result.m[2][1] = m.m[1][2];
    result.m[2][2] = m.m[2][2];
    return result;
}

Matrix3 mat_mul_scalar(double s, Matrix3 m)
{
    Matrix3 result;
    result.m[0][0] = s * m.m[0][0];
    result.m[0][1] = s * m.m[0][1];
    result.m[0][2] = s * m.m[0][2];
    result.m[1][0] = s * m.m[1][0];
    result.m[1][1] = s * m.m[1][1];
    result.m[1][2] = s * m.m[1][2];
    result.m[2][0] = s * m.m[2][0];
    result.m[2][1] = s * m.m[2][1];
    result.m[2][2] = s * m.m[2][2];
    return result;
}

Matrix3 mat_mul_mat(Matrix3 m1, Matrix3 m2)
{
    Matrix3 result;
    result.m[0][0] = m1.m[0][0] * m2.m[0][0] + m1.m[0][1] * m2.m[1][0] + m1.m[0][2] * m2.m[2][0];
    result.m[0][1] = m1.m[0][0] * m2.m[0][1] + m1.m[0][1] * m2.m[1][1] + m1.m[0][2] * m2.m[2][1];
    result.m[0][2] = m1.m[0][0] * m2.m[0][2] + m1.m[0][1] * m2.m[1][2] + m1.m[0][2] * m2.m[2][2];

    result.m[1][0] = m1.m[1][0] * m2.m[0][0] + m1.m[1][1] * m2.m[1][0] + m1.m[1][2] * m2.m[2][0];
    result.m[1][1] = m1.m[1][0] * m2.m[0][1] + m1.m[1][1] * m2.m[1][1] + m1.m[1][2] * m2.m[2][1];
    result.m[1][2] = m1.m[1][0] * m2.m[0][2] + m1.m[1][1] * m2.m[1][2] + m1.m[1][2] * m2.m[2][2];

    result.m[2][0] = m1.m[2][0] * m2.m[0][0] + m1.m[2][1] * m2.m[1][0] + m1.m[2][2] * m2.m[2][0];
    result.m[2][1] = m1.m[2][0] * m2.m[0][1] + m1.m[2][1] * m2.m[1][1] + m1.m[2][2] * m2.m[2][1];
    result.m[2][2] = m1.m[2][0] * m2.m[0][2] + m1.m[2][1] * m2.m[1][2] + m1.m[2][2] * m2.m[2][2];
    return result;
}

Vector3 mat_mul_vec(Matrix3 m, Vector3 v)
{
    Vector3 result;
    result.x = m.m[0][0] * v.x + m.m[0][1] * v.y + m.m[0][2] * v.z;
    result.y = m.m[1][0] * v.x + m.m[1][1] * v.y + m.m[1][2] * v.z;
    result.z = m.m[2][0] * v.x + m.m[2][1] * v.y + m.m[2][2] * v.z;
    return result;
}

bool vec_equal(Vector3 v1, Vector3 v2)
{
    return v1.x == v2.x && v1.y == v2.y && v1.z == v2.z;
}

bool mat_equal(Matrix3 m1, Matrix3 m2)
{
    return m1.m[0][0] == m2.m[0][0] && m1.m[0][1] == m2.m[0][1] && m1.m[0][2] == m2.m[0][2] &&
           m1.m[1][0] == m2.m[1][0] && m1.m[1][1] == m2.m[1][1] && m1.m[1][2] == m2.m[1][2] &&
           m1.m[2][0] == m2.m[2][0] && m1.m[2][1] == m2.m[2][1] && m1.m[2][2] == m2.m[2][2];
}

void print_vec(Vector3 v)
{
    printf("[%f, %f, %f]\n", v.x, v.y, v.z);
}

void print_mat(Matrix3 m)
{
    printf("[%f, %f, %f]\n", m.m[0][0], m.m[0][1], m.m[0][2]);
    printf("[%f, %f, %f]\n", m.m[1][0], m.m[1][1], m.m[1][2]);
    printf("[%f, %f, %f]\n", m.m[2][0], m.m[2][1], m.m[2][2]);
};