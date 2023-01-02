#include "ksp_time.h"
#include <stdio.h>

KSPTime ksp_time_from_ut(double ut, enum TimeType time_type)
{
    // Turn seconds into [years, days, hours, minutes, seconds]

    // These two quantities will depend on whether we are
    // using Kerbin time or Earth time
    double seconds_per_day;
    double days_per_year;

    if (time_type == KERBIN_TIME)
    {
        seconds_per_day = 21600;
        days_per_year = 426;
    }
    else if (time_type == EARTH_TIME)
    {
        seconds_per_day = 86400;
        days_per_year = 365;
    }
    else
    {
        // This should never happen
        seconds_per_day = 0;
        days_per_year = 0;
    }
    int years = ut / (seconds_per_day * days_per_year);
    ut -= years * seconds_per_day * days_per_year;
    int days = ut / seconds_per_day;
    ut -= days * seconds_per_day;
    int hours = ut / 3600;
    ut -= hours * 3600;
    int minutes = ut / 60;
    ut -= minutes * 60;
    int seconds = ut;

    KSPTime ksp_time = {time_type, years, days, hours, minutes, seconds};

    return ksp_time;
}

double ut_from_ksp_time(KSPTime ksp_time)
{
    // These two quantities will depend on whether we are
    // using Kerbin time or Earth time
    double seconds_per_day;
    double days_per_year;

    if (ksp_time.time_type == KERBIN_TIME)
    {
        seconds_per_day = 21600;
        days_per_year = 426;
    }
    else if (ksp_time.time_type == EARTH_TIME)
    {
        seconds_per_day = 86400;
        days_per_year = 365;
    }
    else
    {
        // This should never happen
        seconds_per_day = 0;
        days_per_year = 0;
    }

    double ut = ksp_time.seconds;
    ut += ksp_time.minutes * 60;
    ut += ksp_time.hours * 3600;
    ut += ksp_time.days * seconds_per_day;
    ut += ksp_time.years * seconds_per_day * days_per_year;

    return ut;
}

void get_delta_time_string(KSPTime ksp_time, char *buffer, int buffer_size)
{
    // Return a formatted string similar to "1y, 2d, 3h, 4m, 5s"
    // Most useful for showing time deltas

    // Check if each field is zero, and if not, add it to the string
    // If the field is zero, don't add it to the string
    int i = 0;
    if (ksp_time.years > 0)
    {
        i += snprintf(buffer + i, buffer_size - i, "%dy, ", ksp_time.years);
    }
    if (ksp_time.days > 0)
    {
        i += snprintf(buffer + i, buffer_size - i, "%dd, ", ksp_time.days);
    }
    if (ksp_time.hours > 0)
    {
        i += snprintf(buffer + i, buffer_size - i, "%dh, ", ksp_time.hours);
    }
    if (ksp_time.minutes > 0)
    {
        i += snprintf(buffer + i, buffer_size - i, "%dm, ", ksp_time.minutes);
    }
    if (ksp_time.seconds > 0)
    {
        // round the seconds to the nearest integer
        int rounded_seconds = (int)(ksp_time.seconds + 0.5);
        i += snprintf(buffer + i, buffer_size - i, "%ds", rounded_seconds);
    }

    // If the string is empty, add "0s"
    if (i == 0)
    {
        snprintf(buffer, buffer_size, "0s");
    }
}

void get_ut_time_string(KSPTime ksp_time, char *buffer, int buffer_size)
{
    // Return a formatted string similar to "Y1 D2 03:04:05"
    // Most useful for showing absolute time

    // Display all fields, even if they are zero
    int i = 0;
    int display_year = ksp_time.years + 1; // KSP starts at year 1
    int display_day = ksp_time.days + 1;   // KSP starts at day 1

    i += snprintf(buffer + i, buffer_size - i, "Y%d D%d ", display_year, display_day);
    i += snprintf(buffer + i, buffer_size - i, "%02d:%02d:", ksp_time.hours, ksp_time.minutes);
    int rounded_seconds = (int)(ksp_time.seconds + 0.5);
    i += snprintf(buffer + i, buffer_size - i, "%02d", rounded_seconds);
}
