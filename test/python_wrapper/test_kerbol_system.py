import pytest

from trajectorize.ephemeris.kerbol_system import (Body, BodyEnum,
                                                  state_vector_at_time)

# Taken from https://raw.githubusercontent.com/qsantos/spyce/master/spyce/kerbol.json
validation_set = \
    {
        "Bop": {
            "gravitational_parameter": 2486834944.414907,
            "orbit": {
                "argument_of_periapsis": 0.4363323129985824,
                "eccentricity": 0.235,
                "inclination": 0.2617993877991494,
                "longitude_of_ascending_node": 0.174532925199433,
                "mean_anomaly_at_epoch": 0.9,
                "primary": "Jool",
                "semi_major_axis": 128500000
            },
            "radius": 65000
        },
        "Dres": {
            "gravitational_parameter": 21484488600,
            "orbit": {
                "argument_of_periapsis": 1.570796326794897,
                "eccentricity": 0.145,
                "inclination": 0.08726646259971647,
                "longitude_of_ascending_node": 4.886921905584122,
                "mean_anomaly_at_epoch": 3.14,
                "primary": "Kerbol",
                "semi_major_axis": 40839348203
            },
            "radius": 138000,
            "rotational_period": 34800
        },
        "Duna": {
            "gravitational_parameter": 301363211975.0977,
            "orbit": {
                "argument_of_periapsis": 0,
                "eccentricity": 0.051,
                "inclination": 0.001047197527789909,
                "longitude_of_ascending_node": 2.364921136452316,
                "mean_anomaly_at_epoch": 3.14,
                "primary": "Kerbol",
                "semi_major_axis": 20726155264
            },
            "pressure_at_sea_level": 20265,
            "pressure_scale_height": 3000,
            "radius": 320000,
            "rotational_period": 65517.859375
        },
        "Eeloo": {
            "gravitational_parameter": 74410814527.04958,
            "orbit": {
                "argument_of_periapsis": 4.537856055185257,
                "eccentricity": 0.26,
                "inclination": 0.1073377489976513,
                "longitude_of_ascending_node": 0.8726646259971648,
                "mean_anomaly_at_epoch": 3.14,
                "primary": "Kerbol",
                "semi_major_axis": 90118820000
            },
            "radius": 210000,
            "rotational_period": 19460
        },
        "Eve": {
            "gravitational_parameter": 8171730229210.874,
            "orbit": {
                "argument_of_periapsis": 0,
                "eccentricity": 0.01,
                "inclination": 0.03665191262740527,
                "longitude_of_ascending_node": 0.2617993877991494,
                "mean_anomaly_at_epoch": 3.14,
                "primary": "Kerbol",
                "semi_major_axis": 9832684544
            },
            "pressure_at_sea_level": 506625,
            "pressure_scale_height": 7000,
            "radius": 700000,
            "rotational_period": 80500
        },
        "Gilly": {
            "gravitational_parameter": 8289449.814716354,
            "orbit": {
                "argument_of_periapsis": 0.174532925199433,
                "eccentricity": 0.55,
                "inclination": 0.2094395102393195,
                "longitude_of_ascending_node": 1.396263401595464,
                "mean_anomaly_at_epoch": 0.9,
                "primary": "Eve",
                "semi_major_axis": 31500000
            },
            "radius": 13000,
            "rotational_period": 28255
        },
        "Ike": {
            "gravitational_parameter": 18568368573.14401,
            "orbit": {
                "argument_of_periapsis": 0,
                "eccentricity": 0.03,
                "inclination": 0.00349065855600352,
                "longitude_of_ascending_node": 0,
                "mean_anomaly_at_epoch": 1.7,
                "primary": "Duna",
                "semi_major_axis": 3200000
            },
            "radius": 130000
        },
        "Jool": {
            "gravitational_parameter": 282528004209995.3,
            "orbit": {
                "argument_of_periapsis": 0,
                "eccentricity": 0.05,
                "inclination": 0.02275909379554594,
                "longitude_of_ascending_node": 0.9075712110370514,
                "mean_anomaly_at_epoch": 0.1,
                "primary": "Kerbol",
                "semi_major_axis": 68773560320
            },
            "pressure_at_sea_level": 1519875,
            "pressure_scale_height": 10000,
            "radius": 6000000,
            "rotational_period": 36000
        },
        "Kerbin": {
            "gravitational_parameter": 3531600000000,
            "orbit": {
                "argument_of_periapsis": 0,
                "eccentricity": 0,
                "inclination": 0,
                "longitude_of_ascending_node": 0,
                "mean_anomaly_at_epoch": 3.14,
                "primary": "Kerbol",
                "semi_major_axis": 13599840256
            },
            "pressure_at_sea_level": 101325,
            "pressure_scale_height": 5000,
            "radius": 600000,
            "rotational_period": 21549.42518308983
        },
        "Kerbol": {
            "gravitational_parameter": 1.172332794832491e+18,
            "radius": 261600000,
            "rotational_period": 432000
        },
        "Laythe": {
            "gravitational_parameter": 1962000029236.078,
            "orbit": {
                "argument_of_periapsis": 0,
                "eccentricity": 0,
                "inclination": 0,
                "longitude_of_ascending_node": 0,
                "mean_anomaly_at_epoch": 3.14,
                "primary": "Jool",
                "semi_major_axis": 27184000
            },
            "pressure_at_sea_level": 81060,
            "pressure_scale_height": 4000,
            "radius": 500000
        },
        "Minmus": {
            "gravitational_parameter": 1765800026.312472,
            "orbit": {
                "argument_of_periapsis": 0.6632251157578452,
                "eccentricity": 0,
                "inclination": 0.1047197551196598,
                "longitude_of_ascending_node": 1.361356816555577,
                "mean_anomaly_at_epoch": 0.9,
                "primary": "Kerbin",
                "semi_major_axis": 47000000
            },
            "radius": 60000,
            "rotational_period": 40400
        },
        "Moho": {
            "gravitational_parameter": 168609378654.5095,
            "orbit": {
                "argument_of_periapsis": 0.2617993877991494,
                "eccentricity": 0.2,
                "inclination": 0.1221730476396031,
                "longitude_of_ascending_node": 1.221730476396031,
                "mean_anomaly_at_epoch": 3.14,
                "primary": "Kerbol",
                "semi_major_axis": 5263138304
            },
            "radius": 250000,
            "rotational_period": 1210000
        },
        "Mun": {
            "gravitational_parameter": 65138397520.7807,
            "orbit": {
                "argument_of_periapsis": 0,
                "eccentricity": 0,
                "inclination": 0,
                "longitude_of_ascending_node": 0,
                "mean_anomaly_at_epoch": 1.7,
                "primary": "Kerbin",
                "semi_major_axis": 12000000
            },
            "radius": 200000
        },
        "Pol": {
            "gravitational_parameter": 721702080.0000001,
            "orbit": {
                "argument_of_periapsis": 0.2617993877991494,
                "eccentricity": 0.17085,
                "inclination": 0.07417649320975901,
                "longitude_of_ascending_node": 0.03490658503988659,
                "mean_anomaly_at_epoch": 0.9,
                "primary": "Jool",
                "semi_major_axis": 179890000
            },
            "radius": 44000
        },
        "Tylo": {
            "gravitational_parameter": 2825280042099.953,
            "orbit": {
                "argument_of_periapsis": 0,
                "eccentricity": 0,
                "inclination": 0.00043633231950044,
                "longitude_of_ascending_node": 0,
                "mean_anomaly_at_epoch": 3.14,
                "primary": "Jool",
                "semi_major_axis": 68500000
            },
            "radius": 600000
        },
        "Vall": {
            "gravitational_parameter": 207481499473.751,
            "orbit": {
                "argument_of_periapsis": 0,
                "eccentricity": 0,
                "inclination": 0,
                "longitude_of_ascending_node": 0,
                "mean_anomaly_at_epoch": 0.9,
                "primary": "Jool",
                "semi_major_axis": 43152000
            },
            "radius": 300000
        }
    }


@pytest.mark.parametrize("body_name", validation_set.keys())
def test_body_parameters(body_name):
    body = Body.from_name(body_name)

    assert body.name == body_name
    assert body.mu == pytest.approx(
        validation_set[body_name]["gravitational_parameter"])
    assert body.radius == pytest.approx(validation_set[body_name]["radius"])

    if "orbit" in validation_set[body_name]:
        assert body.orbit.semi_major_axis == pytest.approx(
            validation_set[body_name]["orbit"]["semi_major_axis"])
        assert body.orbit.eccentricity == pytest.approx(
            validation_set[body_name]["orbit"]["eccentricity"])
        assert body.orbit.inclination == pytest.approx(
            validation_set[body_name]["orbit"]["inclination"])
        assert body.orbit.longitude_of_ascending_node == pytest.approx(
            validation_set[body_name]["orbit"]["longitude_of_ascending_node"])
        assert body.orbit.argument_of_periapsis == pytest.approx(
            validation_set[body_name]["orbit"]["argument_of_periapsis"])
        assert body.orbit.mean_anomaly_at_epoch == pytest.approx(
            validation_set[body_name]["orbit"]["mean_anomaly_at_epoch"])


def test_ephemeris_1():
    initial_kerbin_State = state_vector_at_time(0, BodyEnum.KERBOL,
                                                BodyEnum.KERBIN)

    assert initial_kerbin_State.time == 0
