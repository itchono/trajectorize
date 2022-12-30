#include "vec_math.h"

#ifndef _ROTATIONS_H
#define _ROTATIONS_H

// Defined using active rotations

// Principal rotation axes

Matrix3 rotation_x(double angle);
Matrix3 rotation_y(double angle);
Matrix3 rotation_z(double angle);

// Perifocal to ECI rotations
// Using 3-1-3 Euler angles
Matrix3 eci_to_perifocal(double raan, double i, double aop);
Matrix3 perifocal_to_eci(double raan, double i, double aop);

#endif // _ROTATIONS_H