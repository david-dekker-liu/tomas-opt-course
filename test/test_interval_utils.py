from datetime import datetime
from src.intervals import Interval, LinkedInterval
import src.interval_utils as interval_utils
import pytest


def d(x):
    return datetime.strptime(x, "%Y-%m-%d %H:%M:%S")


def s(x):
    return x.strftime("%Y-%m-%d %H:%M:%S")


def test_update_time_range_basic():
    linked_interval = LinkedInterval(
        start=d("2021-05-11 13:18:00"),
        end=d("2021-05-11 13:38:00"),
        orig_start=d("2021-05-11 12:00:00"),
        orig_end=d("2021-05-11 12:20:00"))

    new_start = d("2021-05-11 13:28:00")
    new_end = d("2021-05-11 13:33:00")

    updated_linked_interval = interval_utils.update_time_range(linked_interval, new_start, new_end)

    assert updated_linked_interval == LinkedInterval(
        start=d("2021-05-11 13:28:00"),
        end=d("2021-05-11 13:33:00"),
        orig_start=d("2021-05-11 12:10:00"),
        orig_end=d("2021-05-11 12:15:00")
    )


def test_update_time_range_date_boundary():
    linked_interval = LinkedInterval(
        start=d("2021-05-10 20:00:00"),
        end=d("2021-05-11 06:00:00"),
        orig_start=d("2021-05-09 04:10:12"),
        orig_end=d("2021-05-09 14:10:12"))

    new_start = d("2021-05-10 20:00:02")
    new_end = d("2021-05-11 03:15:00")

    updated_linked_interval = interval_utils.update_time_range(linked_interval, new_start, new_end)

    assert updated_linked_interval == LinkedInterval(
        start=d("2021-05-10 20:00:02"),
        end=d("2021-05-11 03:15:00"),
        orig_start=d("2021-05-09 04:10:14"),
        orig_end=d("2021-05-09 11:25:12")
    )


# Tests the linear interpolation of a time window when the corresponding window is shortened, with bad input
def test_update_time_range_bad_input():
    linked_interval = LinkedInterval(
        start=d("2021-05-10 20:00:00"),
        end=d("2021-05-11 06:00:00"),
        orig_start=d("2021-05-09 04:10:12"),
        orig_end=d("2021-05-09 14:10:12"))

    new_start = d("2021-05-10 19:59:58")
    new_end = d("2021-05-11 03:15:00")

    with pytest.raises(Exception):
        interval_utils.update_time_range(linked_interval, new_start, new_end)


def test_intersect_intervals():
    linked_interval_list = [
        LinkedInterval(
            d("2021-05-08 14:30:00"),
            d("2021-05-08 14:40:00"),
            d("2021-05-08 04:05:00"),
            d("2021-05-08 04:15:00")),
        LinkedInterval(
            d("2021-05-08 18:00:00"),
            d("2021-05-08 18:45:00"),
            d("2021-05-08 06:04:30"),
            d("2021-05-08 06:49:30")),
        LinkedInterval(
            d("2021-05-08 20:05:10"),
            d("2021-05-08 20:15:40"),
            d("2021-05-08 07:00:00"),
            d("2021-05-08 07:10:30"))]

    interval_list = [Interval(d("2021-05-08 14:00:00"), d("2021-05-08 15:00:00")),
                     Interval(d("2021-05-08 16:00:00"), d("2021-05-08 17:00:00")),
                     Interval(d("2021-05-08 18:00:00"), d("2021-05-08 18:12:00")),
                     Interval(d("2021-05-08 18:20:00"), d("2021-05-08 18:40:00")),
                     Interval(d("2021-05-08 18:40:00"), d("2021-05-08 20:10:00")),
                     Interval(d("2021-05-08 20:15:40"), d("2021-05-08 21:30:00"))]

    intersected_spaces = interval_utils.intersect_intervals(linked_interval_list, interval_list)

    assert len(intersected_spaces) == 5

    interval_1, interval_2, interval_3, interval_4, interval_5 = intersected_spaces

    assert interval_1 == LinkedInterval(
        start=d("2021-05-08 14:30:00"),
        end=d("2021-05-08 14:40:00"),
        orig_start=d("2021-05-08 04:05:00"),
        orig_end=d("2021-05-08 04:15:00"))

    assert interval_2 == LinkedInterval(d("2021-05-08 18:00:00"), d("2021-05-08 18:12:00"), d("2021-05-08 06:04:30"), d("2021-05-08 06:16:30"))
    assert interval_3 == LinkedInterval(d("2021-05-08 18:20:00"), d("2021-05-08 18:40:00"), d("2021-05-08 06:24:30"), d("2021-05-08 06:44:30"))
    assert interval_4 == LinkedInterval(d("2021-05-08 18:40:00"), d("2021-05-08 18:45:00"), d("2021-05-08 06:44:30"), d("2021-05-08 06:49:30"))
    assert interval_5 == LinkedInterval(d("2021-05-08 20:05:10"), d("2021-05-08 20:10:00"), d("2021-05-08 07:00:00"), d("2021-05-08 07:04:50"))
