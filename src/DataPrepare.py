import numpy as np
import pandas as np

def DataPreprocess(price_Data,fundamental_Data):
    price_Data = price_Data.rename(index=str, columns={"eob": "Date"})
    fundamental_Data = fundamental_Data.rename(index=str, columns={"end_date": "Date"})

    price_Data["Date"] = price_Data["Date"].dt.date
    fundamental_Data["Date"] = fundamental_Data["Date"].dt.date

    price_Data = price_Data.set_index(['Date'])
    fundamental_Data = fundamental_Data.set_index(['Date'])

    #增加一列index列
    ll = list(price_Data['close'])
    length = len(ll)
    ll2 = [i for i in range(1, length + 1)]
    price_Data['itx'] = ll2

    return price_Data,fundamental_Data