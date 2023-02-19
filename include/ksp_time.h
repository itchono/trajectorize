/*
Trajectorize

KSP time conversions

This file defines types and methods for representing time in KSP.
*/

#include <stdbool.h>

enum TimeType
{
    EARTH_TIME, // 86400s days, 365d years
    KERBIN_TIME // 21600s days, 426d years
};

typedef struct KSPTime
{
    // The time type used to represent this time
    // Time is stored as years, days, hours, minutes, seconds
    // only the seconds is stored as a floating point value; the rest are integers
    enum TimeType time_type;
    int years;
    int days;
    int hours;
    int minutes;
    double seconds;
} KSPTime;

// Convert between KSP time and universal time (seconds since epoch)
KSPTime ksp_time_from_ut(double ut, enum TimeType time_type);
double ut_from_ksp_time(KSPTime ksp_time);

void get_delta_time_string(KSPTime ksp_time, char *buffer, int buffer_size);
void get_ut_time_string(KSPTime ksp_time, char *buffer, int buffer_size, bool day_only);
