import numpy as np
import pandas as pd
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN.UTF-8')

LAKH = 100000.00
CRORE = 10000000.00
THOUSAND = 1000.00

def num_to_currency(num, letters=True):
    if num > CRORE:
        return str(locale.currency(num / CRORE, grouping=True)) + 'Cr'
    elif num > LAKH:
        return str(locale.currency(num / LAKH, grouping=True)) + 'L'
    elif num > THOUSAND:
        return str(locale.currency(num / THOUSAND, grouping=True)) + 'K'
    return locale.currency(num, grouping=True)

def future_values(monthly=1000, rate=0.10, start=5, end=41, step=5, init=0, r=2):
  periods = np.array([iter * 12 for iter in range(start, end, step)])
  final_amount = np.round(np.fv(rate/12,
                                periods,
                                -1 * monthly,
                                init,
                                when='begin'), r)
  final_amount_str = list(map(num_to_currency, final_amount))

  return np.stack((periods/12,
                   final_amount_str), axis=-1)

def try_future_values(monthly=1000):
    data = future_values(monthly)
    headers = ['Years',
               'Final Amount']
    return pd.DataFrame(data, columns=headers)

def future_values_diff_rates(monthly,
                             rates,
                             start=10,
                             end=21,
                             step=10,
                             init=0,
                             r=2):
    periods = np.array([iter * 12 for iter in range(start, end, step)])
    invested_amount = (np.round(np.cumsum([monthly * 12 * step]
                                          * len(range(start, end, step))), r))
    invested_amount_str = list(map(num_to_currency, invested_amount))

    rates = [r/100 for r in rates]
    res = []
    for rate in rates:
        final_amount = np.round(np.fv(rate/12,
                                      periods,
                                      -1 * monthly,
                                      init,
                                      when='begin'), r)
        final_amount_str = list(map(num_to_currency, final_amount))
        res.append(final_amount_str)
    result = np.concatenate(([periods/12],
                             [invested_amount_str],
                             res), axis=0)
    return result.transpose()

def try_future_values_diff_rates(monthly=1000):
    rates=[-8,3.5,4.62,5.6,7,7.5,10]
    data = future_values_diff_rates(monthly, rates)
    headers = ['Years', 'Invested Amount'] + list(map(str, rates))
    return pd.DataFrame(data, columns=headers)

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

def inflation_adjusted(init, rate=-0.08, start=7, end=43, step=7, r=2):
    periods = np.array([iter for iter in range(start, end, step)])
    print(periods)
    after_inflation = np.round(np.fv(rate,
                                   periods,
                                   0,
                                   -1 * init,
                                   when='begin'), r)
    after_inflation_str = list(map(num_to_currency, after_inflation))
    return np.stack((periods, after_inflation_str), axis=-1)

def try_inflation_adjusted(init=50000):
    data = inflation_adjusted(init)
    headers = ['Years',
               'Future Value']
    return pd.DataFrame(data, columns=headers)

def main():
  return try_future_values(1000)
  # return try_future_values_df(1000)
  # return try_inflation_adjusted(100000)
  # return try_future_values_diff_rates(20000)

main()
