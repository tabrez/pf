import numpy as np
import pandas as pd
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN.UTF-8')

LAKH = 100000.00
CRORE = 10000000.00
THOUSAND = 1000.00

def num_to_currency(num, add_letters=True):
    def format(mark, letters):
        print(mark)
        v = str(locale.currency(num / mark, grouping=True))
        if add_letters:
            print(letters)
            return v + letters
        return v

    if abs(num) > CRORE:
        return format(CRORE, 'Cr')
    elif abs(num) > LAKH:
        return format(LAKH, 'L')
    elif abs(num) > THOUSAND:
        return format(THOUSAND, 'K')
    return format(1, '')

def make_periods(start=5, end=41, step=5):
    return np.array([v * 12 for v in range(start, end, step)])

def make_df(col1, col2, headers):
    data = np.stack((col1, col2), axis=-1)
    return pd.DataFrame(data, columns=headers)

def to_currency_fmt(num):
    return list(map(num_to_currency, num))

def future_values(monthly, periods, rate=0.10, init=0, r=2):
  return np.round(np.fv(rate/12,
                                periods,
                                -1 * monthly,
                                init,
                                when='begin'), r)
  #return to_currency_fmt(final_amount)

def invested_amount(monthly=1000, start=5, end=41, step=10, r=2):
    amt_per_step = [monthly * 12 * step]
    return (np.round(np.cumsum(
        amt_per_step * len(range(start, end, step))), r))

def future_values_diff_rates(monthly, rates, periods, init=0, r=2):
    rates = [r/100 for r in rates]
    return [np.round(np.fv(rate/12,
                           periods,
                           -1 * monthly,
                           init,
                           when='begin'), r) for rate in rates]

def future_values_df(monthly=1000, rate=0.10, start=5, end=41, step=5, init=0, r=2):
  periods = np.array([iter * 12 for iter in range(start, end, step)])
  final_amount = np.round(np.fv(rate/12,
                                periods,
                                -1 * monthly,
                                init,
                                when='begin'), r)
  final_amount_str = list(map(num_to_currency, final_amount))

  invested_amount = (np.round(np.cumsum([monthly * 12 * step]
                                        * len(range(start, end, step))), r))
  invested_amount_str = list(map(num_to_currency, invested_amount))

  returns_amount = np.round(final_amount - invested_amount, r)
  returns_amount_str = list(map(num_to_currency, returns_amount))

  times_increased = np.round(final_amount / invested_amount, r)

  return np.stack((periods/12,
                   invested_amount_str,
                   returns_amount_str,
                   final_amount_str,
                   times_increased), axis=-1)

def try_future_values_df(monthly=1000):
    data = future_values_df(monthly)
    headers = ['Years',
               'Invested Amount',
               'Returns Amount',
               'Final Amount',
               'Times Increased']
    return pd.DataFrame(data, columns=headers)

def inflation_adjusted(init, periods, rate=-0.08, r=2):
    return np.round(np.fv(rate/12,
                          periods,
                          0,
                          -1 * init,
                          when='begin'), r)

def main():
  # return try_future_values(1000)
  # return try_future_values_df(1000)
  return try_inflation_adjusted(100000)
  # return try_future_values_diff_rates(20000)
  #  return None

def try_future_values(monthly=1000):
    periods = make_periods(5, 41, 5)
    values = to_currency_fmt(future_values(monthly, periods))
    return make_df(periods/12, values, ['Years', 'Final Amount'])

def try_inflation_adjusted(init=50000):
    #periods = np.array([iter for iter in range(start, end, step)])
    periods = make_periods(start=7, end=43, step=7)
    after_inflation = inflation_adjusted(init, periods)
    values = to_currency_fmt(after_inflation)
    headers = ['Years',
               'Future Value']
    data = make_df(periods, values, headers)
    return pd.DataFrame(data, columns=headers)

def try_future_values_diff_rates(monthly=1000):
    rates=[-8,3.5,4.62,5.6,7,7.5,10]
    (start, end, step) = (10, 31, 10)
    periods = make_periods(start, end, step)
    invested_amount_str = to_currency_fmt(invested_amount(monthly, start, end, step))
    future_values_dr = future_values_diff_rates(monthly, rates, periods)
    res = [to_currency_fmt(arr) for arr in future_values_dr]
    result = np.concatenate(([periods/12],
                             [invested_amount_str],
                             res), axis=0)
    data = result.transpose()
    headers = ['Years', 'Invested Amount'] + list(map(str, rates))
    return pd.DataFrame(data, columns=headers)

main()
