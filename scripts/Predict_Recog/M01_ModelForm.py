#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  This script builds a SVR (Support Vector Regression) machine learning model from 
EEG data related to Oddball_Recog_2019 in order to predict object recognition
in phase 2 (recognition test) of the task from single trial EEG amplitude recorded 
in phase 1 (oddball, stimulus encoding). 

    Features:
        Single trial mean EEG amplitude 
        
    Labels:
        Behavioral outcome (Recognized: 1, not-recognized: 0)
        
The following steps are performed:
    (1) load data dictionary: data['VP0001']['Novels']['nvl_1']['Elecs']["'Cz'"]['data']
    (2) Extract features

Created on Mon May 25 16:08:53 2020

@author: mheado86
"""

import os.path 
import json                                                                     # json.load()
import nilearn

## Load data ##

filepath = '/Users/mheado86/Desktop/course-materials-2020/project/MarkNelson86_EEGRecogBIDS/data/'
file_name = 'subj_dict'
full_fn_json = os.path.join(filepath, file_name+'.json')

with open(full_fn_json) as file:
  data = json.load(file)
  
  
## Extract features ##
  
# Feature 1: Single trial EEG amplitude at Cz

