import random
import struct
import sys


# This script checks Python2.7 only!
assert sys.version_info.major, sys.version_info.minor == (2, 7)


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
    # if (r_max == r_min + 1) or (r_max < r_min):
    if (r_max - r_min) < 2:
        return r_min
    r_new = r_min + ((r_max - r_min) / 2)
    inject_random_num(r_new)
    tn = random.SystemRandom().choice(range(1, dist_max + 1))
    if tn > t0 and tn > t:
        return urand_max(t, t0, tn, r_min, r_new)
    else:
        return urand_max(t, tn, t1, r_new, r_max)


def partition(n):
    """Get list of urand_max for all numbers in a range.
    """
    return [urand_max(x, 1, 3) for x in range(1, n)]


print(urand_max(1, 1, 3))
print(urand_max(2, 1, 3))

print(partition(3))

print("range '1': ", 24019198012642647 + 1)
print("range '2': ", 48038396025285287 - 24019198012642647)
print("range '3': ", (2**56 - 1) - 48038396025285287)

r1 = 24019198012642647 + 1
r2 = 48038396025285287 - 24019198012642647
r3 = 2**56 - 1 - 48038396025285287
print(2**56)
print(r1 + r2 + r3)
