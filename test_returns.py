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

def test_future_values():
    periods = make_periods(start=5, end=41, step=5)
    values = future_values(1000, periods)
    expected = [78082.38, 206552.02, 417924.27, 765696.91, 1337890.35,
                2279325.32, 3828276.7 , 6376780.24]
    assert np.all(np.isclose(values, expected))

def test_invested_amount():
    values = invested_amount(1000)
    assert np.allclose(values, [120000, 240000, 360000, 480000])

def test_inflation_adjusted():
    periods = make_periods(start=7, end=43, step=7)
    values = inflation_adjusted(100000, periods)
    expected = [57013.9 , 32505.85, 18532.86, 10566.31,  6024.26,  3434.67]
    assert np.allclose(values, expected)

def test_future_values_diff_rates():
    rates=[-8,3.5,4.62,5.6,7,7.5,10]
    periods = make_periods(start=10, end=31, step=10)
    values = future_values_diff_rates(1000, rates, periods)
    expected = [np.array([82229.08, 119078.15, 135591.21]),
                np.array([143850.86, 347880.97, 637266.03]),
                np.array([152751.53, 394990.71, 779142.77]),
                np.array([161118.44, 442816.87, 935336.58]),
                np.array([174094.47,  523965.4 , 1227087.49]),
                np.array([179042.41,  557191.54, 1355866.96]),
                np.array([206552.02,  765696.91, 2279325.32])]
    assert np.allclose(np.array(values).flatten(),
                       np.array(expected).flatten())

def test_fail():
    assert True
