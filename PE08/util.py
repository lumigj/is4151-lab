import pandas as pd



def set_default_pandas_options(max_columns=10, max_rows=2000, width=1000, max_colwidth=50):
    
    pd.set_option('display.max_columns', max_columns)
    pd.set_option('display.max_rows', max_rows)
    pd.set_option('display.width', width)
    pd.set_option('max_colwidth', max_colwidth)
