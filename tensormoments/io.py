import pandas as pd
import numpy as np

def readElkOutput(filename):
    with open(filename) as fp:
        lines = fp.readlines()

    d = {}
    species = -1
    atom = -1
    nu = -1
    l1 = -1
    l2 = -1
    k = -1
    p = -1
    r = -1
    t = -1
    for line in lines:
        words = line.split()
        if line.strip().startswith("Species"):
            species = int(words[2])
            atom = int(words[6])
        if line.strip().startswith("nu="):
            nu = int(words[1][:-1])
            l1 = int(words[4][:-1])
            l2 = int(words[7])
        if line.strip().startswith("k ="):
            k = int(words[2][:-1])
            p = int(words[5][:-1])
            r = int(words[8])
        if line.strip().startswith("t ="):
            t = int(words[2])
            v1 = float(words[4])
            v2 = float(words[5])
            value = v1 + 1j*v2
            addEntryToDict(d, species, atom, nu, l1, l2, k, p, r, t, value)
    return d

def addEntryToDict(d, species, atom, nu, l1, l2, k, p, r, t, value):
    entries = ["species", "atom", "nu", "l1", "l2", "k", "p", "r", "t", "value"]
    values = [species, atom, nu, l1, l2, k, p, r, t, value]
    for key, val in zip(entries, values):
        if key not in d:
            d[key] = []
        d[key].append(val)

def makeDataframe(d):
    return pd.DataFrame(d)
    

def dataframeFromFile(filename):
   """ Given a filename, returns a dataframe containing the tensor moments as they are read in.
   """
   data = readElkOutput(filename)
   return makeDataframe(data)
    
def readVaspOutput(filename):
   with open(filename) as fp:
      lines = fp.readlines()

   d = {}
   idx = [1,3,5,7, 9, 10, 11, 12]
   for line in lines:
      words = line.split()
      atom, nu, l1, l2, k, p, r , t = (int(words[i]) for i in idx)
      value = float(words[13]) + 1j*float(words[14])
      addEntryToDict(d, 1, atom, nu, l1, l2, k, p, r, t, value) 
   return d
