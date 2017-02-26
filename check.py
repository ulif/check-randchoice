## DO NOT USE WITH PYTHON VERSIONS OTHER THAN 2.7.x

import random
import struct
from binascii import unhexlify, hexlify


def num_to_bytes(t, bytes_cnt=7):
    """Turn number t into a list of `bytes_cnt` bytes.

    representing the number.
    `bytes_cnt` must be <= 8.
    """
    bytes_list = [x for x in struct.pack("q", t)]
    return bytes_list[:bytes_cnt - 8]


class FakeURandom(object):

    bits = []

    def urandom(self, n):
        result = ""
        for x in range(n):
            if not len(self.bits):
                self.bits.append("\x00")
            result += self.bits.pop()
        return result


fake_random = FakeURandom()
random._urandom = fake_random.urandom


check1 = random.SystemRandom().random()
print("check1 %s" % check1)
assert check1 == 0.0


fake_random.bits = ["\xff", "\xff"]
check2 = random.SystemRandom().random()
print("check2 %s" % check2)
assert str(check2) == "0.999984741211"


num1_bits = num_to_bytes(2**56-1)
print(num1_bits)
fake_random.bits = num1_bits
check3 = random.SystemRandom().random()
print("check3 %s" % check3)
assert str(check3) == "1.0"

fake_random.bits = num_to_bytes(2**56 - 1)
check4 = random.SystemRandom().choice([1, 2, 3])
print("check4 %s" % check4)
assert check4 == 3

fake_random.bits = num_to_bytes(2**55 - 1)
check5 = random.SystemRandom().choice([1, 2, 3])
print("check5 %s" % check5)
assert check5 == 2

fake_random.bits = num_to_bytes(0)
check6 = random.SystemRandom().choice([1, 2, 3])
print("check6 %s" % check6)
assert check6 == 1

fake_random.bits = num_to_bytes(24019198012642647)
check7 = random.SystemRandom().choice([1, 2, 3])
print("check7 %s" % check7)
assert check7 == 1

fake_random.bits = num_to_bytes(24019198012642648)
check8 = random.SystemRandom().choice([1, 2, 3])
print("check8 %s" % check8)
assert check8 == 2


def part(t, t0, t1, r_min=0, r_max=2**56):
    if r_max == r_min + 1:
        return r_min, r_max
    r_new = r_min + ((r_max - r_min) / 2)
    fake_random.bits = num_to_bytes(r_new)
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
print(2**56L)
print(r1 + r2 + r3)
