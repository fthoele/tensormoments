import pandas as pd
import numpy as np
from operator import and_
from six import iteritems
from functools import reduce


def transformGroupToReal(dataframe):
    """ Takes a dataframe and transforms the groups in it to a real representation.

    Args:
        dataframe:

    Returns:
        A copy of the old dataframe, containing the transformed elements.

    """
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



def transform_to_real(dataframe):
    """ Improved version of the transformation. Takes dataframe, and transforms all pairs of (t, v) to their real representation.

    Args:
        dataframe:

    Returns:
        A dataframe with all pairs transformed to real.

    """
    columns = list(dataframe)
    columns.remove("t")
    columns.remove("value")
    grouped = dataframe.groupby(columns)

    realList = []
    for iframe, (name, group) in enumerate(grouped):
        newGroup = transform_group_to_real(group, columns, name)
        realList.extend(newGroup)
    realdf = pd.DataFrame(realList)
    return realdf


def transform_group_to_real(g, group_columns, group_values):
    """ Helper method that transforms one group of values.

    Args:
        g: The group dataframe obtained by the groupby operation.
        group_columns: The columns used for grouping.
        group_values: The values of the grouping columns for this transformation operation.

    Returns:
        A list of dicts, each dict containing a row in the dataframe.

    """
    prototype = {k: v for (k, v) in zip(group_columns, group_values)}
    mult = len(g)
    l = int((mult - 1) / 2)

    sorted_g = g.sort_values("t")
    sorted_values = sorted_g.value.as_matrix()

    results = []
    for m in range(-l, l + 1):
        valPositive = sorted_values[m + l]
        valNegative = sorted_values[-m + l]
        if m < 0:
            newValue = (valPositive - ((-1) ** m) * valNegative) * 1j / np.sqrt(2)
        elif m > 0:
            newValue = (valNegative + ((-1) ** m) * valPositive) * 1. / np.sqrt(2)
        else:
            newValue = valPositive

            # newValue = np.real(newValue)
        result_dict = prototype.copy()
        result_dict['value_real'] = np.real(newValue)
        result_dict['value_imag'] = np.imag(newValue)
        result_dict['t'] = m
        results.append(result_dict)

    return results


def insert_vectors_into_vesta(vectors, vesta_template_file, vector_scale=1.0,
                              template_string_vectt="{VECTT}", template_string_vectr="{VECTR}",
                              template_string_vects="{VECTS}"):
    """ Replaces template string in a vesta file with the correct representation for a number of vectors.

    Args:
        vectors:
        vesta_template_file:
        template_string_vectt:
        template_string_vectr:

    Returns:

    """
    vectors = np.array(vectors)
    if vectors.shape[1] < 3:
        raise ValueError("Not enough y dimensions in input data")

    vectr = ""
    vectt = ""
    for ivect, vector in enumerate(vectors, start=1):
        vectr += "   {} {} {} {} 0\n".format(ivect, *vector)
        vectr += "    {} 0 0 0 0\n".format(ivect)
        vectr += "0 0 0 0 0\n"

        vectt += "   {}  0.500 255  0 0 1\n".format(ivect)

    with open(vesta_template_file) as fp:
        text = fp.read()

    text = text.replace(template_string_vectr, vectr)
    text = text.replace(template_string_vectt, vectt)
    text = text.replace(template_string_vects, f"{vector_scale:8.3f}")

    return text