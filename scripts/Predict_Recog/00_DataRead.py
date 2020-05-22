#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  This script is a first attempt at developing a machine learning algorithm to
predict subsequent novel recognition from single trial EEG amplitude recorded
at stimulus encoding. This data comes from the ROGER dataset related to my
master thesis (2019). The steps are as follows:
    
    (1) Read in EEG data 
        - ~/Desktop/thesis/Data/ALLEEG_ODDSONLY.mat = 5 midline electrodes (AFz-Pz)
          for oddball trials only
          
    (2) 

Created on Wed May 20 14:03:00 2020

@author: mheado86
"""
## Useful functions for .mat to pd.DataFrame
def coerce_void(value):
    """
    Converts `value` to `value.dtype`

    Parameters
    ----------
    value : array_like

    Returns
    -------
    value : dtype
        `Value` coerced to `dtype`
    """

    if np.squeeze(value).ndim == 0:
        return value.dtype.type(value.squeeze())
    else:
        return np.squeeze(value)


def get_labels(fields):
    """
    Helper function to get .mat struct keys from `fields`

    Parameters
    ----------
    fields : dict_like

    Returns
    -------
    labels : list
        Struct keys
    """
    labels = [k for k, v in sorted(fields.items(),
                                   key=lambda x: x[-1][-1])]
    return labels

# Define .mat file
loadpath = '/Users/mheado86/Desktop/thesis/Data/'
fn = 'ALLEEG_ODDSONLY.mat'


# Convert data structure to a normal dictionary using dtypes as keys
from scipy.io import loadmat
data = loadmat(loadpath + fn)['S']

# Accessing values                      
# data[0][subn][Sfn][0][NVLn][NVLfn][0][En][Efn][0][Edata]
# data[0][990][1][0][40][6][0][4][2][0][500] = S(991).Novels(41).Elecs(5).data(501)

Subj_labels = get_labels(data.dtype.fields)
Novels_labels = get_labels(data[0][1][1].dtype.fields)
Elec_labels = get_labels(data[0][900][1][0][40][6].dtype.fields)

data2 = {labels[n]: value for n, value in enumerate(data)}           # conversion to dict
# data2['ID'][subn][Sfn][0][NVLn][NVLfn][0][En][Efn][0][Edata]
# data2['ID'][900][1][0][40][6][0][4][2][0][500]
# Can't access other keys (Novels, BFail)

# To coerce array-like values to be arrays
 data['ID'] = coerce_void(data['ID'])

## HOW TO WORK WITH NESTED MATLAB STRUCTURES IN PYTHON???


# Interpreting object loaded by scipy.io
# dict.keys(S)                                      # dict_keys(['__header__', '__version__', '__globals__', 'S'])
# type(S['S'])                                      # numpy.ndarray
# S['S'].shape                                      # (1, 1000) = ALL SUBS!
# type(S['S'][0][0])                                # numpy.void ???
# S['S'][0][0].shape                                # () ???

# Accessing values in nested structure
# S['S'][0][0]['ID']                                # array(['VP0001'], dtype='<U6')
# S['S'][0][1]['ID']                                # array(['VP0002'], dtype='<U6')
# S['S'][0][1]['Novels']                            # !! Too large to see in console
# type(S['S'][0][1]['Novels'])                      # numpy.ndarray
# S['S'][0][1]['Novels'].shape                      # (1, 48) = all novels for VP0002!

# Extracting values from nested structure
# ID_Vec = [ID for ID in S['S'][0][:]['ID']]        # Stores IDs in a list, but as individual Numpy arrays...
# AllSubNvls = [D for D in S['S'][0][:]['Novels']]  # Values stored! But difficult to handle...
# type(AllSubNvls)                                  # list
# len(AllSubNvls)                                   # 1000 = novels for all subs!
# type(AllSubNvls[0])                               # numpy.ndarray
# AllSubNvls[0].shape                               # (1, 49) = novels for VP0001

# Novel1 = [NVL for NVL in AllSubNvls[0][0]]
# type(Novel1)                                      # list
# len(Novel1)                                       # 49  = all novels for VP0001 as list of Numpy arrays

# Converting numpy arrays
# import numpy as np
# ID_Vec = [np.array2string(x) for x in S['S'][0][:]['ID']] # IDs in list as strings!

# Converting numpy arrays to pandas dataframe
import numpy as np
import pandas as pd

#### Extraction by level & variable
ID_Str = [np.array2string(x) for x in S['S'][0][:]['ID']]         # S(:).ID extracted
Nvls_npy = [NVLS for NVLS in S['S'][0][:]['Novels']]              # S(:).Novels extracted

column_names = ['Type', 'Trln', 'Time_since_tar', 'Trls_since_tar', 'Time_since_odd', 'Trls_since_odd']
X = pd.DataFrame(Nvls_npy, columns=column_names) 


# Extracting Trln values for all Novels for VP0001 (Could turn this into a nested list for all subs!)
# Trln_nmpy_VP0001 = Nvls_npy[0]['Trln']                            # S(1).Novels(1).Trln(:)
#                                                                                       # Trln_list_VP0001 = Trln_nmpy_VP0001.tolist() 
#                                                                                       # Trln_VP0001_nestlist = [x.tolist() for x in Trln_list_VP0001[0][:]]
# Trln_VP0001_values = []
# for i in range(0,len(Trln_nmpy_VP0001[0])):
#    Trln_VP0001_values.append(Trln_nmpy_VP0001[0][i][0][0])

# nested list extracting trln for all subs
Trln_Vals_All = []
for SUB in range(0, len(Nvls_npy)):
    Trln_nmpy_SUBn = Nvls_npy[SUB]['Trln']
    TempList = []
    
    for NVL in range(0, len(Trln_nmpy_SUBn[0])):
        TempList.append(Trln_nmpy_SUBn[0][NVL][0][0])
        
    Trln_Vals_All.append(TempList)
    
# nested list extracting Trls_since_tar for all subs
TrlsSncTar_Vals_All = []
for SUB in range(0, len(Nvls_npy)):
    TrlsSncTar_nmpy_SUBn = Nvls_npy[SUB]['Trls_since_tar']
    TempList = []
    
    for NVL in range(0, len(TrlsSncTar_nmpy_SUBn[0])):
        TempList.append(TrlsSncTar_nmpy_SUBn[0][NVL][0][0])
        
    TrlsSncTar_Vals_All.append(TempList)
    
# Extracting electrodes
Elecs_AllNvl_VP0001 = Nvls_npy[0]['Elecs']
Data_Nvl1_VP0001 = Elecs_AllNvl_VP0001[0][0]['data']
Data_Elec1_Nvl1_VP0001 = Data_Nvl1_VP0001[0][0]
Data_Elec2_Nvl1_VP0001 = Data_Nvl1_VP0001[0][1]

