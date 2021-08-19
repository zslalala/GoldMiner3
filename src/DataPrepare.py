import numpy as np
import pandas as np

def DataPreprocess(data):
    data = data.rename(index=str, columns={"eob": "Date"})
    data = data.set_index(['Date'])
    return data