import pandas as pd
import numpy as np
from operator import and_
from six import iteritems
from functools import reduce

def transformGroupToReal(dataframe):        
    mult = len(dataframe)
    l = int((mult-1)/2)
    newDataframe = dataframe.copy()
    for m in range(-l,l+1):        
        valPositive = dataframe.loc[dataframe.t == m, 'value'].values[0]
        valNegative = dataframe.loc[dataframe.t == -m, 'value'].values[0]
        if m < 0:                        
            newValue = (valPositive - ((-1)**m) *valNegative) * 1j/np.sqrt(2)            
        elif m > 0:
            newValue = (valNegative + ((-1)**m) * valPositive) * 1./np.sqrt(2)
        else:
            newValue = valPositive          
        newDataframe.loc[newDataframe.t == m, "value"] = newValue    
    return newDataframe

def filterTmoms(df, **kwargs):
    """ Returns all tensor moments to which the filter arguments in kwargs apply.
        Keys are: atom, species, nu, l1, l2, k, p, r, t
    """
    labels = list(df)
    filters = []
    for key, value in iteritems(kwargs):
        if key in labels:
            filters.append(df[key] == value)
    if filters:
        finalFilter = reduce(and_, filters)
        return df.loc[finalFilter]
    else:
        return df
    
def transformFrameToReal(dataframe):
    """ Transforms the given dataframe to the real spherical harmonic basis.
    """
    grouped = dataframe.groupby(['k','p','r', 'atom', 'species','nu', 'l1', 'l2'])
    realList = []
    for name, group in grouped:
        newGroup = transformGroupToReal(group)
        realList.append(newGroup)
    realdf = pd.concat(realList)
    return realdf
