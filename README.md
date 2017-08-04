# check-randchoice
Check distribution of `random.choice()` in Python2.7

The distribution of values generated by `random.choice()` is not completely
equal.

This script helps to determine the deviations from strict distributions
experimentally.

It works for Python version 2.7 only! In Python 3.x the problem is fixed.


## background

In fact `random.choice()` picks values by mapping a random number generated
from several bytes to one of the values given in a sequence. But even if these
bytes are completely random, their possible values cannot be distributed
equally over all values of all sequences.

For instance we cannot distribute 256 values (1 byte) over 3-item sequences.

The Python 2.7 `choice` function in fact maps each of 2^56 values to the
iterable of possible values passed in:

    random.choice([0, 1])

will map 2^55 possible random values to result in ``0``, while the remaining
2^55 values will be mapped to result ``1``. If each of the 2^56 possible
values appears with the same probability, then this distribution is perfectly
fair.

But when we want to pick one of

    random.choice([0, 1, 2])

then we cannot distribute all 2^56 values equally over these three values
(at least as long as we require the result in one draw). This is what happens
in real in Python 2.7. Some values get a slightly higher probability to appear
compared to others. The exact amount of this difference is computed with the.


## results

Running ``check.py`` with Python 2,7 we get:

    n=2: min_max_diff: 0, dists: [36028797018963968, 36028797018963968]
    n=3: min_max_diff: 8, dists: [24019198012642648, 24019198012642640, 24019198012642648]
    ...

That means: for n=2 elements we get a fair distribution of 2^55 'hits' for
each of the both values, summing up to 2^56.

For n=3 elements, however, we get not an equal distribution. The second element
was picked 8 times less than the first and last element.


## conclusions


