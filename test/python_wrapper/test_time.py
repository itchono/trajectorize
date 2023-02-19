from trajectorize.ksp_time.time_conversion import (KSPTime, TimeType,
                                                   ut_to_ut_string)


def test_ut_to_kerbin_time():
    ut = 5091552  # expect Y1 D236 04:19:12

    ksp_time = KSPTime.from_ut(ut, TimeType.KERBIN_TIME)

    assert ksp_time.years == 0
    assert ksp_time.days == 235
    assert ksp_time.hours == 4
    assert ksp_time.minutes == 19
    assert round(ksp_time.seconds) == 12
    assert ksp_time.ut_string == "Y1 D236 04:19:12"


def test_ut_to_earth_time():
    ut = 5091552  # expect Y1 D59 22:19:12

    ksp_time = KSPTime.from_ut(ut, TimeType.EARTH_TIME)
    assert ksp_time.years == 0
    assert ksp_time.days == 58
    assert ksp_time.hours == 22
    assert ksp_time.minutes == 19
    assert round(ksp_time.seconds) == 12
    assert ksp_time.ut_string == "Y1 D59 22:19:12"


def test_kerbin_time_to_ut():
    ksp_time = KSPTime(TimeType.KERBIN_TIME, 0, 235, 4, 19, 12)
    ut = ksp_time.ut

    assert ut == 5091552


def test_earth_time_to_ut():
    ksp_time = KSPTime(TimeType.EARTH_TIME, 0, 58, 22, 19, 12)
    ut = ksp_time.ut

    assert ut == 5091552


def test_direct_ut_to_string():
    ut = 5091552

    s = ut_to_ut_string(ut, TimeType.KERBIN_TIME)
    assert s == "Y1 D236 04:19:12"
