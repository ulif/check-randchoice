import random
import struct
import sys


# This script checks Python2.7 only!
assert sys.version_info.major, sys.version_info.minor == (2, 7)


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
    fake_random.byte_vals = num_to_bytes(num)
    return fake_random


def part(t, t0, t1, r_min=0, r_max=2**56):
    if r_max == r_min + 1:
        return r_min, r_max
    r_new = r_min + ((r_max - r_min) / 2)
    inject_random_num(r_new)
    tn = random.SystemRandom().choice([1, 2, 3])
    if tn > t0 and tn > t:
        return part(t, t0, tn, r_min, r_new)
    else:
        return part(t, tn, t1, r_new, r_max)


print(part(1, 1, 3, 0, 2**56))
print(part(2, 1, 3, 0, 2**56))

print("range '1': ", 24019198012642647 + 1)
print("range '2': ", 48038396025285287 - 24019198012642647)
print("range '3': ", (2**56 - 1) - 48038396025285287)

r1 = 24019198012642647 + 1
r2 = 48038396025285287 - 24019198012642647
r3 = 2**56 - 1 - 48038396025285287
print(2**56)
print(r1 + r2 + r3)
