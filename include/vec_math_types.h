/*
Trajectorize

Math Types

This header file contains typedefs and initializers
for the various math types used in Trajectorize.
*/

#ifndef VEC_MATH_TYPES_H
#define VEC_MATH_TYPES_H

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

#endif // VEC_MATH_TYPES_H