import pytest
from returns import num_to_currency

def test_num_to_currency():
    assert num_to_currency(123) == '₹ 123.00'
    assert num_to_currency(123456) == '₹ 1.23L'
    assert num_to_currency(12345678) == '₹ 1.23Cr'
