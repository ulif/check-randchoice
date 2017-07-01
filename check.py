import random
import struct
import sys


# This script checks Python2.7 only!
assert sys.version.startswith("2.7")


# The python 2.7.x SystemRandom.choice() function asks for 8 bytes from
# /dev/urandom
URAND_MIN = 0            # minimum 8 byte value
URAND_MAX = 2 ** 56 - 1  # maximum 8 byte value


def num_to_bytes(t, bytes_cnt=7):
    """Turn number t into a list of `bytes_cnt` bytes.

    representing the number.
    `bytes_cnt` must be <= 8.
    """
    bytes_list = [x for x in struct.pack("q", t)]
    return bytes_list[:bytes_cnt - 8]


class FakeURandom(object):

    bytes_list = []

    def urandom(self, n):
        result = ""
        for x in range(n):
            if not len(self.bytes_list):
                self.bytes_list.append("\x00")
            result += self.bytes_list.pop()
        return result


fake_random = FakeURandom()
random._urandom = fake_random.urandom


def inject_random_num(num):
    """Fake urandom results.

    Turn integer `num` into sequence of bytes, which will be output by patched
    urandom on upcoming requests.
    """
    fake_random = FakeURandom()
    random._urandom = fake_random.urandom
    fake_random.bytes_list = num_to_bytes(num)
    return fake_random


def urand_max(t, t0, t1, r_min=URAND_MIN, r_max=URAND_MAX + 1, dist_max=3):
    """Get max urandom number, for which `SystemRandom.choice()` returns `t`

    given, there is a choice from all integers in [`t0`...`t1`].
    """
    if (r_max - r_min) < 2:
        return r_min
    r_new = r_min + ((r_max - r_min) / 2)
    inject_random_num(r_new)
    tn = random.SystemRandom().choice(range(1, dist_max + 1))
    if tn > t0 and tn > t:
        return urand_max(t, t0, tn, r_min, r_new, dist_max=dist_max)
    else:
        return urand_max(t, tn, t1, r_new, r_max, dist_max=dist_max)


def partition(n):
    """Get list of urand_max for all numbers in a range.
    """
    return [urand_max(x, 1, n + 1, dist_max=n) for x in range(1, n + 1)]


def distribution(n):
    r_lower = -1
    result = []
    for p in partition(n):
        result.append(p - r_lower)
        r_lower = p
    return result


def min_max_diff(distribution):
    d_min = min(distribution)
    d_max = max(distribution)
    return d_max - d_min


N = 3

print(partition(N))
dist = distribution(N)

print(dist)
assert sum(dist) == 2 ** 56


for n in [2, 3, 4, 5, 6]:
    dist = distribution(n)
    print("n=%i: min_max_diff: %i, dists: %r" % (n,min_max_diff(dist), dist))
    assert sum(dist) == 2 ** 56
