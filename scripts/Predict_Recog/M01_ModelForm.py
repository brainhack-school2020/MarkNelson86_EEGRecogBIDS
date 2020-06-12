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

#%% Import & load

def dict_depth(a_dict, level = 1): 
    # Function to find depth of a dictionary  
    
    if not isinstance(a_dict, dict) or not a_dict: 
        return level 
    return max(dict_depth(a_dict[key], level + 1) for key in a_dict) 



import os.path 
import json                                                                     # json.load()
import random as rnd
import math
import numpy as np
#import nilearn as nl

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
  
#%% Prepare data for model

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

# Guide:
# len(data['VP0001']['Novels']['nvl_1']['Elecs']["'Cz'"]['data'])  -- > 220
# dict.keys(BHV['VP0001']['INFO'])
# dict.keys(BHV['VP0001']['Novels']['nvl_1']['behav_data'])
# BHV['VP0001']['Novels']['nvl_1']['behav_data']['Type']
  

## Include/exclude subs
VPi_exclude = []
VPname_exclude = []

for VPn in range(len(BHV)):
    try:
        man_exclud = BHV[KZb[0][VPn]]['INFO']['ManualExclusion']
        rec_acc_OLD = BHV[KZb[0][VPn]]['INFO']['RecognitionAccOld']
        if man_exclud == 1:
            print('Manual exclusion: ', BHV[KZb[0][VPn]]['ID'])
            VPi_exclude.append(VPn)
            VPname_exclude.append(BHV[KZb[0][VPn]]['ID'])
            
        elif rec_acc_OLD[0] <= .1 or rec_acc_OLD[0] >= .9:                      # Not enough of both outcomes
            print('Recog accuracy exclusion: ', BHV[KZb[0][VPn]]['ID'])
            VPi_exclude.append(VPn)
            VPname_exclude.append(BHV[KZb[0][VPn]]['ID'])
            
    except:
        VPi_exclude.append(VPn)
        VPname_exclude.append(BHV[KZb[0][VPn]]['ID'])
        print("loop failed at iteration: ", VPn, ", for: ", BHV[KZb[0][VPn]]['ID'] )


## Extract features ##
  
# Feature 1: Single trial EEG amplitude at 1 electrode (CAN I FEED IT THE WHOLE INTERVAL?)
# Extract all data (Each entry in final list is 220 EEG samples in time window )
        
Ename = "'Cz'"                                                                  # toggle electrode here
EEG_Recog_Cz = []
EEG_Unrec_Cz = []
loop_fail_VPn = []
behav_outcome_classify_fail_VPn = {}
novel_number_mismatch = []

for VPn in [inc for inc in range(len(BHV)) if inc not in VPi_exclude]:          # iterate all except in list
    EEG_Recog_Cz_temp = []
    EEG_Unrec_Cz_temp = []
    
    try:
        VPID = BHV[KZb[0][VPn]]['ID']
        print("Sorting data for ", VPID)
#        loop_fail_tlrn = []
        behav_outcome_classify_fail_trln = []
        fail = 0
        
#        if len(BHV[KZb[0][VPn]]['Novels']) != len(data[KZe[0][VPn]]['Novels']): # Sanity check
#            print("Quantity of novels in BHV & data don't match for ", VPID)    # Unecessary: all match
#            novel_number_mismatch.append(VPID)
        
        for Nn in range(len(BHV[KZb[0][VPn]]['Novels'])):                       # loop to sort EEG data by behavioral outcome
            TRLID = KZb[3][Nn]
            recog = BHV[KZb[0][VPn]]['Novels'][TRLID]['behav_data']['OddRecognized'] # behavioral outcome
            eeg_trial = data[KZe[0][VPn]]['Novels'][TRLID]['Elecs'][Ename]['data'] # eeg data for trial Nn & VPn
            
            if recog == 1:
                EEG_Recog_Cz_temp.append(eeg_trial)
                
            elif recog == 0:
                EEG_Unrec_Cz_temp.append(eeg_trial)
                
            else:
                print("Unable to classify data for ", VPID, " ", TRLID)
                behav_outcome_classify_fail_trln.append(TRLID)                  # Store failed trial indices in list 
                
                if fail == 0:
                    fail += 1
                    
                    
        if fail == 1:
            behav_outcome_classify_fail_VPn[VPID] = behav_outcome_classify_fail_trln
                
                
        EEG_Recog_Cz.append(EEG_Recog_Cz_temp)                                  #  add eeg data to  overall nested list
        EEG_Unrec_Cz.append(EEG_Unrec_Cz_temp)
        TRLID = 0                                                               # reset trial ID to make except printout clear
        
    except:
        print("loop fail for ", VPID, " ", TRLID)
        loop_fail_VPn.append(VPn)
        
# Check number of successful trials for both results:
recog_trl_totaln = 0
unrec_trl_totaln = 0

for SUB in range(len(EEG_Recog_Cz)):
    recog_trl_totaln += len(EEG_Recog_Cz[SUB])
    unrec_trl_totaln += len(EEG_Unrec_Cz[SUB])
    
print("The total number of recognition trials successfully sorted is ", recog_trl_totaln)
print("The total number of unrecognition trials successfully sorted is ", unrec_trl_totaln)

del EEG_Recog_Cz_temp
del EEG_Unrec_Cz_temp
del fail

#%% Modelling

## BUILD MODEL ##

# (1) Create training list (linear/unnested)

EEG_Recog_Cz_Train = []
EEG_Unrec_Cz_Train = []

for SUB in range(len(EEG_Recog_Cz)):
    
    for TRL in range(len(EEG_Recog_Cz[SUB])):
        EEG_Recog_Cz_Train.append(EEG_Recog_Cz[SUB][TRL])
        
for SUB in range(len(EEG_Unrec_Cz)):                                            # separate loop in case dimensions non-identicle
    
    for TRL in range(len(EEG_Unrec_Cz[SUB])):
        EEG_Unrec_Cz_Train.append(EEG_Unrec_Cz[SUB][TRL])

# (2) split data into training set & test set (75:25)

EEG_Recog_Cz_Test = []
EEG_Unrec_Cz_Test = []

for TRL in range(math.ceil(len(EEG_Recog_Cz_Train) * .25)):                     # at least 25% of total trials
    rnd_trli = rnd.randint(0,len(EEG_Recog_Cz_Train)-1)                         # randomly index trial
    EEG_Recog_Cz_Test.append(EEG_Recog_Cz_Train.pop(rnd_trli))                  # pop trial at index out into test set


for TRL in range(math.ceil(len(EEG_Unrec_Cz_Train) * .25)):                     # at least 25% of total trials
    rnd_trli = rnd.randint(0,len(EEG_Unrec_Cz_Train)-1)                         # randomly index trial
    EEG_Unrec_Cz_Test.append(EEG_Unrec_Cz_Train.pop(rnd_trli))                  # pop trial at index out into test set
    
    
# SANITY CHECK: plot ERPS Rec vs Unrec
    
EEG_mean_Recog_Cz = [sum(x)/len(x) for x in zip(*EEG_Recog_Cz_Train)]
EEG_mean_Unrec_Cz = [sum(x)/len(x) for x in zip(*EEG_Unrec_Cz_Train)]


import matplotlib.pyplot as plt

plt.plot(range(360,800,2),EEG_mean_Recog_Cz, label="Recog")
plt.plot(range(360,800,2),EEG_mean_Unrec_Cz, label="Unrec")
plt.ylabel('EEG amplitude (microvolts)')
plt.xlabel('time (ms)')
plt.title('Grand avg ERPS: Recognized vs unrecognized oddballs')
plt.legend()
plt.show()                                                                      # ERPs look good

    
# (3) Train model (SVM)

X = EEG_Recog_Cz_Train + EEG_Unrec_Cz_Train                                     # Concatenate lists to single data vector
X = np.array(X)                                                                 # Convert to np.array for modelling (n_samples x n_features)
Y = list(np.ones(len(EEG_Recog_Cz_Train))) + list(np.zeros(len(EEG_Unrec_Cz_Train))) # vector of 0s & 1s corresponding to unrec & recog
Y = ['R' if x != 0 else 'U' for x in Y]                                         # 1s = R, 0s = U (better for classifier?)
#Y = np.array(Y)                                                                 # COnvert to np.array??

from sklearn import svm
    
model = svm.SVC()
model.fit(X, Y)                             # Switch X & Y? Does it matter?  Behave measures should be Y...

    
# (4) Test model

X_test = EEG_Recog_Cz_Test + EEG_Unrec_Cz_Test
X_test = np.array(X_test)
test_results = model.predict(X_test)             
values, counts = np.unique(test_results, return_counts=True)                    # test results yield all 1s! WHY??
values = list(values)                                                           # convert to list so indexable
nRecog_Predict = counts[values.index('R')]                                      # number of predicted recognized


print("The number of predicted Recognized novles is ", nRecog_Predict)
print("out of ", len(EEG_Recog_Cz_Test), " possible...")
print("This corresponds to a prediction accurracy of ", )

#%% SCRATCH

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