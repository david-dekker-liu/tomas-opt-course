class LinkedInterval:
    def __init__(self, start, end, orig_start, orig_end):
        self.start = start
        self.end = end
        self.orig_start = orig_start
        self.orig_end = orig_end


class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end
