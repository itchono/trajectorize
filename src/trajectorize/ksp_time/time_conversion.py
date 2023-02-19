from dataclasses import dataclass
from enum import IntEnum

from trajectorize._c_extension import ffi, lib


class TimeType (IntEnum):
    '''
    Enum for the different types of time.
    '''
    EARTH_TIME = lib.EARTH_TIME
    KERBIN_TIME = lib.KERBIN_TIME


@dataclass
class KSPTime:
    time_type: TimeType
    years: int
    days: int
    hours: int
    minutes: int
    seconds: float

    @classmethod
    def from_c_data(cls, cdata):
        return cls(cdata.time_type,
                   cdata.years,
                   cdata.days,
                   cdata.hours,
                   cdata.minutes,
                   cdata.seconds)

    @classmethod
    def from_ut(cls, ut: float, time_type: TimeType):
        c_data = lib.ksp_time_from_ut(ut, time_type)
        return cls.from_c_data(c_data)

    @property
    def c_data(self):
        return ffi.new('struct KSPTime *', self.__dict__)[0]

    @property
    def ut(self) -> float:
        return lib.ut_from_ksp_time(self.c_data)

    @property
    def delta_string(self) -> str:
        # use library function

        # create string buffer to hold result
        buf = ffi.new('char[]', 100)
        lib.get_delta_time_string(self.c_data, buf, 100)

        return ffi.string(buf).decode('utf-8')

    @property
    def ut_string(self) -> str:
        # use library function

        # create string buffer to hold result
        buf = ffi.new('char[]', 100)
        lib.get_ut_time_string(self.c_data, buf, 100, False)

        return ffi.string(buf).decode('utf-8')


def interval_to_delta_string(
        interval: float,
        time_type: TimeType = TimeType.KERBIN_TIME) -> str:
    '''
    Convert a time interval in seconds into a formatted string.

    Parameters
    ----------
    interval: float
        time interval in seconds
    time_type: TimeType
        Kerbin time or Earth time
    '''
    # create string buffer to hold result
    buf = ffi.new('char[]', 100)
    lib.get_delta_time_string(lib.ksp_time_from_ut(interval, time_type),
                              buf, 100)

    return ffi.string(buf).decode('utf-8')


def ut_to_ut_string(ut: float, time_type: TimeType = TimeType.KERBIN_TIME,
                    day_only: bool = False) -> str:
    '''
    Convert a universal timestamp in seconds to a formatted string.

    Parameters
    ----------
    ut: float
        universal time in seconds
    time_type: TimeType
        Kerbin time or Earth time
    day_only: bool
        whether to print the full time string (e.g. Y1 D1 12:34:56 or just Y1 D1)
    '''
    # For faster conversion

    # create string buffer to hold result
    buf = ffi.new('char[]', 100)
    lib.get_ut_time_string(lib.ksp_time_from_ut(
        ut, time_type), buf, 100, day_only)

    return ffi.string(buf).decode('utf-8')
