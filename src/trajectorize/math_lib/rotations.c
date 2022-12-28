#include "rotations.h"

#include <math.h>

// All angles are in radians
Matrix3 rotation_x(double angle)
{
    Matrix3 result;
    result.m[0][0] = 1;
    result.m[0][1] = 0;
    result.m[0][2] = 0;
    result.m[1][0] = 0;
    result.m[1][1] = cos(angle);
    result.m[1][2] = -sin(angle);
    result.m[2][0] = 0;
    result.m[2][1] = sin(angle);
    result.m[2][2] = cos(angle);
    return result;
}

Matrix3 rotation_y(double angle)
{
    Matrix3 result;
    result.m[0][0] = cos(angle);
    result.m[0][1] = 0;
    result.m[0][2] = sin(angle);
    result.m[1][0] = 0;
    result.m[1][1] = 1;
    result.m[1][2] = 0;
    result.m[2][0] = -sin(angle);
    result.m[2][1] = 0;
    result.m[2][2] = cos(angle);
    return result;
}

Matrix3 rotation_z(double angle)
{
    Matrix3 result;
    result.m[0][0] = cos(angle);
    result.m[0][1] = -sin(angle);
    result.m[0][2] = 0;
    result.m[1][0] = sin(angle);
    result.m[1][1] = cos(angle);
    result.m[1][2] = 0;
    result.m[2][0] = 0;
    result.m[2][1] = 0;
    result.m[2][2] = 1;
    return result;
}

Matrix3 eci_to_perifocal(double raan, double i, double aop)
{
    Matrix3 result;
    result = mat_mul_mat(rotation_z(-aop), rotation_x(-i));
    result = mat_mul_mat(result, rotation_z(-raan));

    return result;
}

Matrix3 perifocal_to_eci(double raan, double i, double aop)
{
    Matrix3 result;
    result = mat_mul_mat(rotation_z(raan), rotation_x(i));
    result = mat_mul_mat(result, rotation_z(aop));
    return result;
}