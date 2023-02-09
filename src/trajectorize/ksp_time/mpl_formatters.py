from matplotlib.ticker import Formatter

from trajectorize.ksp_time.time_conversion import TimeType, ut_to_ut_string


class UTFormatter(Formatter):

    def __init__(self, time_type: TimeType = TimeType.KERBIN_TIME,
                 day_only: bool = True):
        self.time_type = time_type
        self.day_only = day_only

    def __call__(self, x, pos=None):
        # Assume x is a float representing universal time
        return ut_to_ut_string(x, self.time_type, self.day_only)


class DeltaFormatter(Formatter):
    def __init__(self, time_type: TimeType = TimeType.KERBIN_TIME):
        self.time_type = time_type

    def __call__(self, x, pos=None):
        # Assume x is a float representing universal time
        if self.time_type == TimeType.KERBIN_TIME:
            return f"{x / 21600:.0f}d"
        else:
            return f"{x / 86400:.0f}d"
