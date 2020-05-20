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

loadpath = '/Users/mheado86/Desktop/thesis/Data/'
fn = 'ALLEEG_ODDSONLY.mat'


from scipy.io import loadmat
S = loadmat(loadpath + fn)                                        # load data

## HOW TO WORK WITH NESTED MATLAB STRUCTURES IN PYTHON???

# Interpreting object loaded by scipy.io
# dict.keys(S)
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