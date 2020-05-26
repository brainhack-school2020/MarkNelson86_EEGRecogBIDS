#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  This script reads in a nested array in .mat format and converts it to a nested dictionary.
    
    (1) Read in EEG data (.mat file)
        - ~/Desktop/thesis/Data/ALLEEG_ODDSONLY.mat = 5 midline electrodes (AFz-Pz)
          for oddball trials only
          
    (2) Convert to nested dictionary: subj_dict[<VPn>]["Novels"][<nvl_n>]["Elecs"][<'Elec_name'>]["data"]
        * Don't forget extra '' around electrode name
        * need to convert numpy file types to be json compatible
        
    (3) Save nested dictionary to json file in /MarkNelson86_EEGRecogBIDS/data/

Created on Wed May 20 14:03:00 2020

@author: mheado86
"""

import numpy as np
from scipy.io import loadmat

## Useful functions for .mat conversion
#def coerce_void(value):
#    """
#    Converts `value` to `value.dtype`
#
#    Parameters
#    ----------
#    value : array_like
#
#    Returns
#    -------
#    value : dtype
#        `Value` coerced to `dtype`
#    """
#
#    if np.squeeze(value).ndim == 0:
#        return value.dtype.type(value.squeeze())
#    else:
#        return np.squeeze(value)


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

# load .mat file
loadpath = '/Users/mheado86/Desktop/thesis/Data/'
fn = 'ALLEEG_ODDSONLY.mat'
data = loadmat(loadpath + fn)['S']
Teegs = 380
Teege = 600

## Extract info  ##
#ID_Str = [np.array2string(x) for x in data[0][:]['ID']]                         # S(:).ID extracted
#Nvls_npy = [NVLS for NVLS in data[0][:]['Novels']]                              # S(:).Novels extracted

# Electrode info
Elec_Names = []
Elec_Numbs = []
for x in range(5):
    Elec_Names.append(np.array2string(data[0][0][1][0][0][6][0][x][0][0]))      # Electrode names
    Elec_Numbs.append(data[0][0][1][0][0][6][0][x][1][0][0])                    # Electrode numbers
    
# get structure field names
FieldNames_Subj = get_labels(data.dtype.fields)
FieldNames_Nvls = get_labels(data[0][1][1].dtype.fields)
FieldNames_Elec = get_labels(data[0][900][1][0][40][6].dtype.fields)

# index fieldnames at each level to be accessed in loop
fn_N = FieldNames_Subj.index('Novels')
fn_E = FieldNames_Nvls.index('Elecs')
fn_D = FieldNames_Elec.index('data')
fn_Trl = FieldNames_Nvls.index('Trln')
fn_TsT = FieldNames_Nvls.index('Trls_since_tar')
fn_TsO = FieldNames_Nvls.index('Trls_since_odd')

# loop through data structure levels and store values in nested dictionary
subj_dict = {}
for VP in range(len(data[0])):                                                   # iterate through subjs
    
    novel_dict = {}
    
    for Nn in range(len(data[0][VP][fn_N][0])):                                 # iterate through novel trials
        
        elec_dict = {}
        
#        for e in range(len(data[0][VP][fn_N][0][Nn][fn_E][0])):                 # iterate through electrodes
        for e in range(2):
        
            Delec = data[0][VP][fn_N][0][Nn][fn_E][0][e+2][fn_D][0][Teegs:Teege].tolist()      # convert to type: list
            Enum = Elec_Numbs[e+2].tolist()
            Ename = Elec_Names[e+2]
            elec_dict[Ename] = {"name" : Ename, "number" : Enum, "data" : Delec} # Build Elec dict
        
        # Build dictionary for novels each with enclosed electrode dictionary
        Trln = data[0][VP][fn_N][0][Nn][fn_Trl][0][0].tolist()                  # convert to type: int
        TrlSncTar = data[0][VP][fn_N][0][Nn][fn_TsT][0][0].tolist()
        TrlSncOdd = data[0][VP][fn_N][0][Nn][fn_TsO][0][0].tolist()
        novel_dict['nvl_'+str(Nn+1)] = {"Trln": Trln, "Trls_since_tar": TrlSncTar, "Trls_since_odd": TrlSncOdd, "Elecs" : elec_dict}

    # Build dictionary for subjects each with enclosed novels & electrodes dictionaries
    Subj_ID = data[0][VP][0][0]
    subj_dict[Subj_ID] = {"Novels" : novel_dict}
    
    

## Save dictionary object 
import os.path
import json
save_path = '/Users/mheado86/Desktop/course-materials-2020/project/MarkNelson86_EEGRecogBIDS/data/'
file_name = 'subj_dict'

# save as .json (numpy data types not compatible with json)
complete_name = os.path.join(save_path, file_name+'.json')
json = json.dumps(subj_dict)
f = open(complete_name,"w")
f.write(json)
f.close()

# save as .txt
complete_name = os.path.join(save_path, file_name+'.txt')
f = open(complete_name,"w")
f.write(str(subj_dict))
f.close()

## GUIDE to nested dictionary object: subj_dict["VPn"]["Novels"]["nvl_n"]["Elecs"]["'Elec_name'"]["data"]
# keys_subj = dict.keys(subj_dict)

## Pandas DataFrame from nested dictionary: THIS DOESN'T MAKE SENSE FOR MY DATA??
#df_test = pd.DataFrame.from_dict({(i,j,k): subj_dict[i]["Novels"][j]["Elecs"][k] 
#                               for i in subj_dict.keys() 
#                               for j in subj_dict[i]["Novels"].keys()},
#                               orient='index')







## SCRATCH: HOW TO WORK WITH NESTED MATLAB STRUCTURES IN PYTHON???
    
# Convert data structure to a normal dictionary using dtypes as keys (NEED TO BUILD OUT FROM CORE)
# data_dict = {FieldNames_Subj[n]: value for n, value in enumerate(data)}
    
# data2['ID'][subn][Sfn][0][NVLn][NVLfn][0][En][Efn][0][Edata]
# data2['ID'][900][1][0][40][6][0][4][2][0][500]
# Can't access other keys (Novels, BFail)

# To coerce array-like values to be arrays: helpful?
# data3['ID'] = coerce_void(data_dict['ID'])

# Accessing values directly in numpy void object: long form                      
# data[0][subn][Sfn][0][NVLn][NVLfn][0][En][Efn][0][Edata]
# data[0][990][1][0][40][6][0][4][2][0][500] = S(991).Novels(41).Elecs(5).data(501)

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



#### Extraction by level & variable
#ID_Str = [np.array2string(x) for x in S['S'][0][:]['ID']]         # S(:).ID extracted
#Nvls_npy = [NVLS for NVLS in S['S'][0][:]['Novels']]              # S(:).Novels extracted

#column_names = ['Type', 'Trln', 'Time_since_tar', 'Trls_since_tar', 'Time_since_odd', 'Trls_since_odd']
#X = pd.DataFrame(Nvls_npy, columns=column_names) 


# Extracting Trln values for all Novels for VP0001 (Could turn this into a nested list for all subs!)
# Trln_nmpy_VP0001 = Nvls_npy[0]['Trln']                            # S(1).Novels(1).Trln(:)
#                                                                                       # Trln_list_VP0001 = Trln_nmpy_VP0001.tolist() 
#                                                                                       # Trln_VP0001_nestlist = [x.tolist() for x in Trln_list_VP0001[0][:]]
# Trln_VP0001_values = []
# for i in range(0,len(Trln_nmpy_VP0001[0])):
#    Trln_VP0001_values.append(Trln_nmpy_VP0001[0][i][0][0])

# nested list extracting trln for all subs
#Trln_Vals_All = []
#for SUB in range(0, len(Nvls_npy)):
#    Trln_nmpy_SUBn = Nvls_npy[SUB]['Trln']
#    TempList = []
#    
#    for NVL in range(0, len(Trln_nmpy_SUBn[0])):
#        TempList.append(Trln_nmpy_SUBn[0][NVL][0][0])
#        
#    Trln_Vals_All.append(TempList)
    
# nested list extracting Trls_since_tar for all subs
#TrlsSncTar_Vals_All = []
#for SUB in range(0, len(Nvls_npy)):
#    TrlsSncTar_nmpy_SUBn = Nvls_npy[SUB]['Trls_since_tar']
#    TempList = []
#    
#    for NVL in range(0, len(TrlsSncTar_nmpy_SUBn[0])):
#        TempList.append(TrlsSncTar_nmpy_SUBn[0][NVL][0][0])
#        
#    TrlsSncTar_Vals_All.append(TempList)
    
## Extracting electrodes
#Elecs_AllNvl_VP0001 = Nvls_npy[0]['Elecs']
#Data_Nvl1_VP0001 = Elecs_AllNvl_VP0001[0][0]['data']
#Data_Elec1_Nvl1_VP0001 = Data_Nvl1_VP0001[0][0]
#Data_Elec2_Nvl1_VP0001 = Data_Nvl1_VP0001[0][1]
#
#
### Convert using DataRead_CAT.py
#from DataRead_CAT import CatsReader as cr

