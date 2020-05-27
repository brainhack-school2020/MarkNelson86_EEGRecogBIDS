#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  This script builds a SVR (Support Vector Regression) machine learning model from 
EEG data related to Oddball_Recog_2019 in order to predict object recognition
in phase 2 (recognition test) of the task from single trial EEG amplitude recorded 
in phase 1 (oddball, stimulus encoding). 

    Features:
        Single trial mean EEG amplitude
        RT? Also related to recognition
        
    Labels:
        Behavioral outcome (Recognized: 1, not-recognized: 0)
        
The following steps are performed:
    (1) load data dictionary: data['VP0001']['Novels']['nvl_1']['Elecs']["'Cz'"]['data']
    (2) Extract features

Created on Mon May 25 16:08:53 2020

@author: mheado86
"""

def dict_depth(a_dict, level = 1): 
    # Function to find depth of a dictionary  
    
    if not isinstance(a_dict, dict) or not a_dict: 
        return level 
    return max(dict_depth(a_dict[key], level + 1) for key in a_dict) 



import os.path 
import json                                                                     # json.load()
import nilearn

## Load data ##

filepath = '/Users/mheado86/Desktop/course-materials-2020/project/MarkNelson86_EEGRecogBIDS/data/'
EEG_file_name = 'subj_dict'
BHV_file_name = 'bhv_dict'
EEG_full_fn_json = os.path.join(filepath, EEG_file_name+'.json')
BHV_full_fn_json = os.path.join(filepath, BHV_file_name+'.json')

with open(EEG_full_fn_json) as file:
  data = json.load(file)
  
with open(BHV_full_fn_json) as file:
  BHV = json.load(file)
  

## Get keys from each level of dictionary ## (makes iterating dicts easier??)
# EEG dict
KZe = []
KZe.append(list(dict.keys(data)))
KZe.append(list(dict.keys(data['VP0001'])))
KZe.append(list(dict.keys(data['VP0001']['Novels'])))
KZe.append(list(dict.keys(data['VP0001']['Novels']['nvl_1'])))
KZe.append(list(dict.keys(data['VP0001']['Novels']['nvl_1']['Elecs'])))
KZe.append(list(dict.keys(data['VP0001']['Novels']['nvl_1']['Elecs']["'FCz'"])))

# EEG dict
KZb = []
KZb.append(list(dict.keys(BHV)))
KZb.append(list(dict.keys(BHV['VP0001'])))
KZb.append(list(dict.keys(BHV['VP0001']['INFO'])))
KZb.append(list(dict.keys(BHV['VP0001']['Novels'])))
KZb.append(list(dict.keys(BHV['VP0001']['Novels']['nvl_1'])))
KZb.append(list(dict.keys(BHV['VP0001']['Novels']['nvl_1']['behav_data'])))
  

## Include/exclude subs
VPi_exclude = []
VPname_exclude = []

for VPn in range(len(BHV)):
    try:
        man_exclud = BHV[KZb[0][VPn]]['INFO']['ManualExclusion']
        rec_acc_OLD = BHV[KZb[0][VPn]]['INFO']['RecognitionAccOld']
        if man_exclud == 1:
            VPi_exclude.append(VPn)
            VPname_exclude.append(BHV[KZb[0][VPn]]['ID'])
            
        elif rec_acc_OLD[0] <= .1 or rec_acc_OLD[0] >= .9:                                # Not enough of both outcomes
            VPi_exclude.append(VPn)
            VPname_exclude.append(BHV[KZb[0][VPn]]['ID'])
            
    except:
        VPi_exclude.append(VPn)
        VPname_exclude.append(BHV[KZb[0][VPn]]['ID'])
        print("loop failed at iteration: ", VPn, ", for: ", BHV[KZb[0][VPn]]['ID'] )


## Extract features ##
  
# Feature 1: Single trial EEG amplitude at Cz


## GUIDES: 
# to nested EEG dict:
# len(data[KZe[0][VPn]][KZe[1][0]]) --> # of novels
# data[KZe[0][VPn]][KZe[1][0]][KZe[2][i]][KZe[3][0]] --> trln

# to nested BHV dict:
# len(BHV[KZb[0][VPn]][KZb[1][2]]) --> # of novels
# BHV[KZb[0][VPn]][KZb[1][2]][KZb[3][n]][KZb[4][0]] --> BD for novel n
# BHV[KZb[0][VPn]][KZb[1][2]][KZb[3][n]][KZb[4][0]][KZb[5][1]] --> trln


## SCRATCH:

# Double checking trial numbers match up...
# THEY DON'T! EEGtrln < BHVtrln for later trials
# potential causes: 
#   (1) rej trials not reflected in BHVtrln?    IGNORE: GET MODEL WORKING: THEN GO TO SOURCE FILES
list_eegtrn = []
list_bhvtrn = []
for i in range(5):
    try:
        Leeg = len(data[KZe[0][i]][KZe[1][0]])
        Lbhv = len(BHV[KZb[0][i]][KZb[1][2]])
        
        if Leeg == Lbhv:
            list_eegtrn_temp = []
            list_bhvtrn_temp = []
            for j in range(Leeg):
                TRNeeg = data[KZe[0][i]][KZe[1][0]][KZe[2][j]][KZe[3][0]]
                TRNbhv = BHV[KZb[0][i]][KZb[1][2]][KZb[3][j]][KZb[4][0]][KZb[5][1]]
                list_eegtrn_temp.append(TRNeeg)
                list_bhvtrn_temp.append(TRNbhv)
                #if TRNeeg != TRNbhv:
                    #print("Mismatch in TRLn at VP: ", i+1, " , Novel: ", j+1)
        else:
            print("Mismatch in novel length at VP: ", i+1)
            
        list_eegtrn.append(list_eegtrn_temp)
        list_bhvtrn.append(list_bhvtrn_temp)
    except:
        print("VP ", i, " failed try block")