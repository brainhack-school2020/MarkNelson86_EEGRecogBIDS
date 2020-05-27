#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  This script reads in a nested array in .mat format and converts it to a nested dictionary.
    
    (1) Read in data: EEG data & Behavioral data (.mat files)
        - ~/Desktop/thesis/Data/ALLEEG_ODDSONLY.mat = 5 midline electrodes (AFz-Pz)
          for oddball trials only
        - ~/Desktop/thesis/Data/BHV_ALL.mat = behavioral data for all subs
          
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

# load .mat files
loadpath = '/Users/mheado86/Desktop/thesis/Data/'
fn_eeg = 'ALLEEG_ODDSONLY.mat'
fn_behave = 'BHV_ALL.mat'
data = loadmat(loadpath + fn_eeg)['S']                                          # load EEG data
BHV = loadmat(loadpath + fn_behave)['BHV']                                      # load behavioral data
Teegs = 380
Teege = 600

## Extract info  ##

#ID_Str = [np.array2string(x) for x in data[0][:]['ID']]                         # S(:).ID extracted
#Nvls_npy = [NVLS for NVLS in data[0][:]['Novels']]                              # S(:).Novels extracted

# Electrode info from EEG structure
Elec_Names = []
Elec_Numbs = []
for x in range(5):
    Elec_Names.append(np.array2string(data[0][0][1][0][0][6][0][x][0][0]))      # Electrode names
    Elec_Numbs.append(data[0][0][1][0][0][6][0][x][1][0][0])                    # Electrode numbers
    
# get EEG structure field names
FieldNames_Subj = get_labels(data.dtype.fields)
FieldNames_Nvls = get_labels(data[0][1][1].dtype.fields)
FieldNames_Elec = get_labels(data[0][900][1][0][40][6].dtype.fields)

# get BEHAVIORAL structure field names
FieldNames_BHV = get_labels(BHV.dtype.fields)
FieldNames_INFO = get_labels(BHV[0][990][1].dtype.fields)
FieldNames_BD = get_labels(BHV[0][990][2].dtype.fields)



## Create keys to access fieldnames within levels of structure ##

# index fieldnames at each level of EEG structure to ease access in loop
fn_N = FieldNames_Subj.index('Novels')                                          # main keys
fn_E = FieldNames_Nvls.index('Elecs')
fn_D = FieldNames_Elec.index('data')

fn_Trl = FieldNames_Nvls.index('Trln')
fn_TsT = FieldNames_Nvls.index('Trls_since_tar')
fn_TsO = FieldNames_Nvls.index('Trls_since_odd')

# index fieldnames at each level of BEHAVIORAL structure to ease access in loop
fn_ID = FieldNames_BHV.index('ID')                                              # main keys
fn_I = FieldNames_BHV.index('INFO')
fn_BD = FieldNames_BHV.index('BD')

#fn_LTSK = FieldNames_INFO.index('LogsForTasks')                                 # Tasks present or not
#fn_MANX = FieldNames_INFO.index('ManualExclusion')                              # pass/fail exclusion criteria
#fn_RGaO = FieldNames_INFO.index('RecognitionAccOld')                            # % of OLD oddballs recognized

#fn_TP = FieldNames_BD.index('Type')                                             # Trial type (2=tar, 3=odd)
#fn_Trlbv = FieldNames_BD.index('Trnr')                                          # Trial number
#fn_Rec = FieldNames_BD.index('OddRecognized')                                   # was the oddball later recognized or not
#fn_RT = FieldNames_BD.index('OddRecognizedRT')                                  # RT of that response


## LOOP THROUGH DATA STRUCTURES AND EXTRACT VALUES TO STORE IN NESTED DICTIONARY

# EEG data structure
subj_dict = {}
for VP in range(len(data[0])):                                                  # iterate through subjs
    
    novel_dict = {}
    
    for Nn in range(len(data[0][VP][fn_N][0])):                                 # iterate through novel trials
        
        elec_dict = {}
        
#        for e in range(len(data[0][VP][fn_N][0][Nn][fn_E][0])):                # iterate through electrodes
        for e in range(2):
        
            Delec = data[0][VP][fn_N][0][Nn][fn_E][0][e+2][fn_D][0][Teegs:Teege].tolist() # convert to type: list
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
    
# BHV structure
bhv_dict = {}

for VP in range(len(BHV[0])):                                                   # loop through subjects
    Subj_ID = BHV[0][VP][0][0].tolist()                                         # convert subject ID to .json friendly format (str)    
    
    if BHV[0][VP][fn_I][0].tolist() == "Missing":                               # if subj data missing
        bhv_dict["VP0627"] = {"ID" : Subj_ID, "INFO" : 'Missing', "BD" : 'Missing'} # SPECIAL CASE: NO DATA FOR VP0627
    
    else:
        INFO_dict = {}
        INFO_values = []
        Ifn_number = len(BHV[0][VP][fn_I][0][0])
        
        for Ifn in range(Ifn_number):                                           # loop through fieldnames in INFO structure       
            INFO_values.append(BHV[0][VP][fn_I][0][0][Ifn][0].tolist())         # convert all values to .json friendly format and add to list
        
        FieldNames_INFO_temp = get_labels(BHV[0][VP][fn_I].dtype.fields)
        
        for C in FieldNames_INFO_temp:
            
            if C == 'computer':                                                 # remove computer data entry (np.ndarray not .json compatible)
                rm_index = FieldNames_INFO_temp.index('computer')
                del INFO_values[rm_index]                                       # rm entry in both lists before zipping
                del FieldNames_INFO_temp[rm_index]
        
        INFO_dict = dict(zip(FieldNames_INFO_temp,INFO_values))                 # create INFO dictionary: keys = INFO struct fieldnames, values = extracted data for VPn
        odd_count = 0
        novel_dict = {}
        
        for Nn in range(len(BHV[0][VP][fn_BD][0])):                             # loop through novels in behavioral data
            trltyp_check = BHV[0][VP][fn_BD][0][Nn][0][0][0]
            
            if trltyp_check == 3:                                               # 3 = oddball trial, exclude targets
                novel_values = []
                BD_dict = {}
                odd_count += 1                                                  # count number of oddballs
                BDfn_number = len(BHV[0][VP][fn_BD][0][Nn])                     # number of fields in specific trial
                
                for BDfn in range(BDfn_number):                                 # loop through fieldnames in BD structure for VPn & Nn
                    novel_values.append(BHV[0][VP][fn_BD][0][Nn][BDfn][0][0].tolist()) # convert all values to .json friendly format and add to list
                
                FieldNames_BD_temp = get_labels(BHV[0][VP][fn_BD].dtype.fields)
                BD_dict = dict(zip(FieldNames_BD_temp,novel_values))            # create BD dictionary: keys = BD struct fieldnames, values = extracted data for VPn
                novel_dict['nvl_'+str(odd_count)] = {"behav_data" : BD_dict, "NonStandardStim_Count" : Nn+1} # Store in dictionary by novel
                    
        bhv_dict[Subj_ID] = {"ID" : Subj_ID, "INFO" : INFO_dict, "Novels" : novel_dict}
            
    

## Save dictionary objects 
import os.path
import json
save_path = '/Users/mheado86/Desktop/course-materials-2020/project/MarkNelson86_EEGRecogBIDS/data/'
EEG_file_name = 'subj_dict'
BHV_file_name = 'bhv_dict'

# save EEG dictionary as .json (numpy data types not compatible with json)
complete_name = os.path.join(save_path, EEG_file_name+'.json')
json = json.dumps(subj_dict)
f = open(complete_name,"w")
f.write(json)
f.close()

# save BHV dictionary as .json 
complete_name = os.path.join(save_path, BHV_file_name+'.json')
json = json.dumps(bhv_dict)
f = open(complete_name,"w")
f.write(json)
f.close()

# save EEG dictionary as .txt
complete_name = os.path.join(save_path, EEG_file_name+'.txt')
f = open(complete_name,"w")
f.write(str(subj_dict))
f.close()






## SCRATCH: HOW TO WORK WITH NESTED MATLAB STRUCTURES IN PYTHON???

# GUIDE: to BHV object
# BHV[0][VPn][0][0] --> VP_ID

# BHV[0][VPn][1][0][0] --> INFO structure
# BHV[0][VPn][1][0][0][n]  --> fieldnames of INFO structure (25)
# BHV[0][VPn][1][0][0][n]  --> to return value of fieldname n

# BHV[0][VPn][2][0][0]   --> BD (behavioral data) (180+ trials)
# BHV[0][VPn][2][0][Trln][n]  --> fieldnames of BD structure (21)
# BHV[0][VPn][2][0][Trln][n][0][0] --> to return value of fieldname n for BD_Trln & VPn
# BHV[0][VPn][2][0][BD_Trln][0][0][0] --> to return TrlType (1=stand,2=targ,3=odd)
# BHV[0][VPn][2][0][BD_Trln][1][0][0] --> to return Trln
# BHV[0][VPn][2][0][BD_Trln][18][0][0] --> to return RecogResult

    

## GUIDE to nested dictionary object: 
# subj_dict["VPn"]["Novels"]["nvl_n"]["Elecs"]["'Elec_name'"]["data"]
# keys_subj = dict.keys(subj_dict)

## Pandas DataFrame from nested dictionary: THIS DOESN'T MAKE SENSE FOR MY DATA??
#df_test = pd.DataFrame.from_dict({(i,j,k): subj_dict[i]["Novels"][j]["Elecs"][k] 
#                               for i in subj_dict.keys() 
#                               for j in subj_dict[i]["Novels"].keys()},
#                               orient='index')





# Convert data structure to a normal dictionary using dtypes as keys (NEED TO BUILD OUT FROM CORE)
# data_dict = {FieldNames_Subj[n]: value for n, value in enumerate(data)}
   
# data2['ID'][subn][Sfn][0][NVLn][NVLfn][0][En][Efn][0][Edata]
# data2['ID'][900][1][0][40][6][0][4][2][0][500]
# Can't access other keys (Novels, BFail)

# To coerce array-like values to be arrays: helpful?
# data3['ID'] = coerce_void(data_dict['ID'])



## GUIDE: to data object (S)
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

