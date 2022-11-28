#include "../../include/kerbol_system_bodies.h"

#define _USE_MATH_DEFINES
#include <math.h>

#define RADIANS(degrees) ((degrees)*M_PI / 180.0)

// All units are in SI base units [m, kg, s]
// Information was taken from the KSP wiki
// Distances are given wrt center of mass of the body rather than surface
// This differs from what is reported in-game (wrt equatorial surface)

const BodyParameters Kerbol = {
    KERBOL,
    KERBOL,
    1.7565459e28,
    1.1723328e18,
    261600000,
    600000,
    {0, 0, 0, 0, 0, 0},
    INFINITY};

const BodyParameters Moho = {
    MOHO,
    KERBOL,
    2.5263314e21,
    1.6860938e11,
    250000,
    0,
    {5263138304, 0.2, RADIANS(7), RADIANS(70), RADIANS(15), 3.14},
    9646663.0};

const BodyParameters Eve = {
    EVE,
    KERBOL,
    1.2243980e23,
    8.1717302e12,
    700000,
    90000,
    {9832684544, 0.01, RADIANS(2.1), RADIANS(150), 0, 3.14},
    85109365.0};

const BodyParameters Gilly = {
    GILLY,
    EVE,
    1.2420363e17,
    8289449.8,
    13000,
    0,
    {31500000, 0.55, RADIANS(12), RADIANS(80), RADIANS(10), 0.9},
    126123.27};

const BodyParameters Kerbin = {
    KERBIN,
    KERBOL,
    5.2915158e22,
    3.5316000e12,
    600000,
    70000,
    {13599840256, 0, 0, 0, 0, 3.14},
    84159286.0};

const BodyParameters Mun = {
    MUN,
    KERBIN,
    9.7599066e20,
    6.5138398e10,
    200000,
    0,
    {12000000, 0, 0, 0, 0, 1.7},
    2429559.1};

const BodyParameters Minmus = {
    MINMUS,
    KERBIN,
    2.6457580e19,
    1.7658000e9,
    60000,
    0,
    {47000000, 0, RADIANS(6), RADIANS(78), RADIANS(38), 0.9},
    2247428.4};

const BodyParameters Duna = {
    DUNA,
    KERBOL,
    4.5154270e21,
    3.0136321e11,
    320000,
    50000,
    {20726155264, 0.051, RADIANS(0.06), RADIANS(135.5), 0, 3.14},
    47921949.0};

const BodyParameters Ike = {
    IKE,
    DUNA,
    2.7821615e20,
    1.8568369e10,
    130000,
    0,
    {32000000, 0.03, RADIANS(0.2), 0, 0, 1.7},
    1049598.9};

const BodyParameters Dres = {
    DRES,
    KERBOL,
    3.2190937e20,
    2.1484489e10,
    138000,
    0,
    {40839348203, 0.145, RADIANS(5), RADIANS(280), RADIANS(90), 3.14},
    32832840};

const BodyParameters Jool = {
    JOOL,
    KERBOL,
    4.2332127e24,
    2.8252800e14,
    6000000,
    200000,
    {68773560320, 0.05, RADIANS(1.304), RADIANS(52), 0, 0.1},
    2.4559852e9};

const BodyParameters Laythe = {
    LAYTHE,
    JOOL,
    2.9397311e22,
    1.9620000e12,
    500000,
    50000,
    {27184000, 0, 0, 0, 0, 3.14},
    3723645.8};

const BodyParameters Vall = {
    VALL,
    JOOL,
    3.1087655e21,
    2.0748150e11,
    300000,
    0,
    {43152000, 0, 0, 0, 0, 0.9},
    2406401.4};

const BodyParameters Tylo = {
    TYLO,
    JOOL,
    4.2332127e22,
    2.8252800e12,
    600000,
    0,
    {68500000, 0, RADIANS(0.025), 0, 0, 3.14},
    10856518};

const BodyParameters Bop = {
    BOP,
    JOOL,
    3.7261090e19,
    2.4868349e9,
    65000,
    0,
    {128500000, 0.235, RADIANS(15), RADIANS(10), RADIANS(25), 0.9},
    1221060.9};

const BodyParameters Pol = {
    POL,
    JOOL,
    1.0813507e19,
    7.2170208e8,
    44000,
    0,
    {179890000, 0.171, RADIANS(4.25), RADIANS(2), RADIANS(15), 0.9},
    1042138.9};

const BodyParameters Eeloo = {
    EELOO,
    KERBOL,
    1.1149224e21,
    7.4410815e10,
    210000,
    0,
    {90118820000, 0.26, RADIANS(6.15), RADIANS(50), RADIANS(260), 3.14},
    1.1908294e8};