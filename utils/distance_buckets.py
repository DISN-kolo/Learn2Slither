from enum import Enum


class DistanceBucket(Enum):
    # NEXT is nearby
    # CLOSE is 2..4
    # FAR is 5..8
    # VERY_FAR is 9..+inf
    NEXT = 0
    CLOSE = 1
    FAR = 2
    VERY_FAR = 3
