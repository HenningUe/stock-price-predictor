import pandas as pd


def normalize_stock_price(stock_price_0, stock_price_x):
    CHANGE_AVERAGE = 0.1
    sp0 = stock_price_0
    spx = stock_price_x
    val = (spx - sp0) / sp0 * (0.5 / CHANGE_AVERAGE) + 0.5
    return val


def main():
    # List of Tuples
    matrix = [(222, 34, 23),
              (230, 31, 11),
              (228, 16, 21),
              (237, 32, 22),
              (239, 33, 27),
              (241, 35, 11)
             ]
        # Create a DataFrame object
    dfObj = pd.DataFrame(matrix, columns=list('abc'))
    stock_price_0 = dfObj.a[0]
    dfObj['norm'] = normalize_stock_price(stock_price_0, dfObj.a)
    x = 1


main()
