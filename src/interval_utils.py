from intervals import LinkedInterval, Interval


# Restrict a linked interval to some new time window
def update_time_range(interval, new_start, new_end):
    if new_start < interval.start or new_end < interval.start or new_end > interval.end or new_start > interval.end or new_end < new_start:
        raise Exception("The new time window is not contained in the old one.")

    new_orig_start = interval.orig_start + ((new_start - interval.start).seconds / (interval.end - interval.start).seconds) * (interval.orig_end - interval.orig_start)
    new_orig_end = interval.orig_start + ((new_end - interval.start).seconds / (interval.end - interval.start).seconds) * (interval.orig_end - interval.orig_start)

    return LinkedInterval(new_start, new_end, new_orig_start, new_orig_end)


# Intersect a list of linked intervals with a general list of intervals
def intersect_intervals(linked_interval_list, interval_list):
    output = []

    for linked_interval in linked_interval_list:
        # Continue splitting this interval as long as to-be-intersected is not completely after it
        while len(interval_list) > 0 and interval_list[0].start < linked_interval.end:

            interval_for_intersection = interval_list[0]

            # If the linked interval is completely before the first interval in the second list, we discard it
            if interval_for_intersection.end < linked_interval.start:
                interval_list = interval_list[1:]
                continue

            #
            if interval_for_intersection.start <= linked_interval.start and interval_for_intersection.end <= linked_interval.end:

                output += [update_time_range(linked_interval, linked_interval.start, interval_for_intersection.end)]
                interval_list = interval_list[1:]

            elif interval_for_intersection.start <= linked_interval.start and interval_for_intersection.end > linked_interval.end:

                output += [linked_interval]
                interval_list = [Interval(linked_interval.end, interval_for_intersection.end)] + interval_list[1:]

            elif interval_for_intersection.end <= linked_interval.end:
                output += [update_time_range(linked_interval, interval_for_intersection.start, interval_for_intersection.end)]
                interval_list = interval_list[1:]

            else:
                output += [update_time_range(linked_interval, interval_for_intersection.start, linked_interval.end)]
                interval_list = [Interval(linked_interval.end, interval_for_intersection.end)] + interval_list[1:]

    return output
