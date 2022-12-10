#include "stumpuff_functions.h"

#include <math.h>

// Path: trajectorize/math_lib/stumpuff_functions.c

double stumpS(double z)
{
    if (z > 0)
    {
        return (sqrt(z) - sin(sqrt(z))) / pow(sqrt(z), 3);
    }
    else if (z < 0)
    {
        return (sinh(sqrt(-z)) - sqrt(-z)) / pow(sqrt(-z), 3);
    }
    else
    {
        return 1.0 / 6.0;
    }
}

double stumpC(double z)
{
    if (z > 0)
    {
        return (1 - cos(sqrt(z))) / z;
    }
    else if (z < 0)
    {
        return (cosh(sqrt(-z)) - 1) / (-z);
    }
    else
    {
        return 1.0 / 2.0;
    }
}