#include <stdio.h>
#include "transfer_orbit.h"
#include "kerbol_system_bodies.h"
#include "delta_v_estimate.h"
#include "vec_math.h"

int main(int argc, char *argv[])
{
    Body kerbin = kerbol_system_bodies[KERBIN];
    Body duna = kerbol_system_bodies[DUNA];
    double t1 = 5091552;
    double t2 = 10679760;
    KeplerianElements transfer_orbit = planetary_transfer_orbit(
        kerbin, duna, t1, t2);
    Vector3 excess_velocity_at_kerbin = excess_velocity_at_body(
        kerbin, transfer_orbit, t1);
    double r_pe = 70000 + kerbin.radius;
    double delta_v = delta_v_req(kerbin, vec_norm(excess_velocity_at_kerbin), r_pe);

    printf("Delta-v to eject from Kerbin: %.2f m/s\n", delta_v);
    printf("Time of transfer: %.0f seconds\n", t2 - t1);
    return 0;
}
