import numpy as np
import pytest
import re
from decimal import Decimal
from returns import *

def test_num_to_currency():
    assert re.match(r'₹[ ]?123.00', num_to_currency(123))
    assert re.match(r'-₹[ ]?1.23K', num_to_currency(-1230))
    assert re.match(r'₹[ ]?1.23L', num_to_currency(123456))
    assert re.match(r'₹[ ]?1.23Cr', num_to_currency(12345678))
    assert re.match(r'₹[ ]?1,23,456.79Cr', num_to_currency(1234567890123))

def test_make_periods():
    assert np.array_equal(make_periods(10, 41, 10),
                          np.array([120, 240, 360, 480]))

def test_to_currency_fmt_len():
    nums = [123, -125, 765432]
    assert len(to_currency_fmt(nums)) == 3

def test_to_currency_fmt_values():
    nums = [123, 1254, 765432]
    assert re.match(r'₹[ ]?123.00', to_currency_fmt(nums)[0])
    assert re.match(r'₹[ ]?1.25K', to_currency_fmt(nums)[1])
    assert re.match(r'₹[ ]?7.65L', to_currency_fmt(nums)[2])
