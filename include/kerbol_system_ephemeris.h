/*
Trajectorize

Kerbol System Ephemeris

This file contains methods for evaluating the position of kerbol
system bodies at a certain universal time.
*/

#ifndef KERBOL_SYSTEM_EPHEMERIS_H
#define KERBOL_SYSTEM_EPHEMERIS_H

#include "state_vector_types.h"
#include "kerbol_system_types.h"

StateVector get_rel_state_at_time(double t, enum BodyEnum parent_id, enum BodyEnum child_id);

#endif // KERBOL_SYSTEM_EPHEMERIS_H