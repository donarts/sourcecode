import datetime


def time_diff(start_t, end_t, t_format='%H:%M:%S'):
    # https://docs.python.org/ko/3/library/datetime.html
    start_dt = datetime.datetime.strptime(start_t, t_format)
    end_dt = datetime.datetime.strptime(end_t, t_format)
    ret = (end_dt - start_dt)
    return ret


if __name__ == "__main__":
    start = "09:00:01"
    end = "10:30:01"
    diff = time_diff(start, end)
    print("--------------------")
    print(type(diff))
    print(diff.days)
    print(diff.seconds)
    print(diff.microseconds)
    print(diff.seconds / 60.0)
    print("--------------------")
    # ISO FORMAT
    # YYYY-MM-DDTHH:MM:SS.ffffff
    # 1900-01-01T00:00:00.000
    diff = time_diff("2022-01-15T01:12:11.000", "2023-01-16T01:12:12.100", "%Y-%m-%dT%H:%M:%S.%f")
    print(diff.days)
    print(diff.seconds)
    print(diff.microseconds)
