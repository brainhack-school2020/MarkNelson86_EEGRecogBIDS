#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  This script builds a SVR (Support Vector Regression) machine learning model from 
EEG data related to Oddball_Recog_2019 in order to predict object recognition
in phase 2 (recognition test) of the task from single trial EEG amplitude recorded 
in phase 1 (oddball, stimulus encoding). 

    Features:
        Single trial  EEG amplitude
        RT? Also related to recognition
        
    Labels:
        Behavioral outcome (Recognized: 1, not-recognized: 0)
        
The following steps are performed:
    (1) load data dictionary: data['VP0001']['Novels']['nvl_1']['Elecs']["'Cz'"]['data']
    (2) Extract features


THIS VERSION EXPANDS ON THE SECOND BY:
    (1) NOT SORTING DATA INTO SEPARATE VECTORS BY RECOG OUTCOME, BUT PUTTING ALL IN SAME VECTOR
    (2) SHUFFLING AND SPLITTING DATA IN SINGLE STEP USING sklearn.model_selection.train_test_split()

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
import statistics as st
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
  
# Feature 1: mean single trial EEG amplitude at 1 electrode across the interval 360-500ms
# Feature 2: trial number in encoding phase
# Feature 3: number of trials since last target
# Feature 4: number of trials since last oddball


        
Ename = "'Cz'"                                                                  # toggle electrode here
windowend = 70
features_all = []
labels_all = []
loop_fail_VPn = []
behav_outcome_classify_fail_VPn = {}

for VPn in [inc for inc in range(len(BHV)) if inc not in VPi_exclude]:          # iterate all except in list
    features_temp = []
    labels_temp = []
    
    try:
        VPID = BHV[KZb[0][VPn]]['ID']
        print("Sorting data for ", VPID)
#        loop_fail_tlrn = []
        behav_outcome_classify_fail_trln = []
        fail = 0
                
        for Nn in range(len(BHV[KZb[0][VPn]]['Novels'])):                       # loop to sort EEG data by behavioral outcome
            TRLID = KZb[3][Nn]
            recog = BHV[KZb[0][VPn]]['Novels'][TRLID]['behav_data']['OddRecognized'] # behavioral outcome
            eeg_trial = data[KZe[0][VPn]]['Novels'][TRLID]['Elecs'][Ename]['data'] # eeg data for trial Nn & VPn
            trialn = data[KZe[0][VPn]]['Novels'][TRLID]['Trln']
            trial_since_tar = data[KZe[0][VPn]]['Novels'][TRLID]['Trls_since_tar']
            trial_since_odd = data[KZe[0][VPn]]['Novels'][TRLID]['Trls_since_odd']
            
            if recog == 1 or recog == 0:
                features_temp.append([st.mean(eeg_trial[0:windowend]),trialn,trial_since_tar,trial_since_odd]) # add all features
                labels_temp.append(recog)
                
            else:
                print("Unable to classify data for ", VPID, " ", TRLID)
                behav_outcome_classify_fail_trln.append(TRLID)                  # Store failed trial indices in list 
                
                if fail == 0:
                    fail += 1
                    
                    
        if fail == 1:
            behav_outcome_classify_fail_VPn[VPID] = behav_outcome_classify_fail_trln
                
                
        features_all.append(features_temp)                                      #  add eeg data to  overall nested list
        labels_all.append(labels_temp)
        TRLID = 0                                                               # reset trial ID to make except printout clear
        
    except:
        print("loop fail for ", VPID, " ", TRLID)
        loop_fail_VPn.append(VPn)
        
# Check number of successful trials for both results:
recog_totaln = sum([labels_all[S].count(1) for S in range(len(labels_all))])
unrec_totaln = sum([labels_all[S].count(0) for S in range(len(labels_all))])
    
print("The total number of recognition trials successfully sorted is ", recog_totaln)
print("The total number of unrecognition trials successfully sorted is ", unrec_totaln)

del behav_outcome_classify_fail_trln
del rec_acc_OLD
del man_exclud
del recog
del TRLID
del VPID
del trial_since_odd
del trial_since_tar
del trialn
del eeg_trial
del features_temp
del labels_temp
del fail

#%% Modelling

## BUILD MODEL ##

# (1) Flatten out nested labels list, and bring 3 tier nested features list down one level
# no longer organized nest by SUB & trl, but only by trl

labels_all = [item for sublist in labels_all for item in sublist]
features_all = [item for sublist in features_all for item in sublist]


# (2) split data into training set & test set (70:30)

from sklearn.model_selection import train_test_split
    
X_train, X_val, y_train, y_val = train_test_split(
                                                    features_all,
                                                    labels_all,
                                                    test_size = 0.3, 
                                                    shuffle = True,
                                                    random_state = 123)         # same shuffle each time
                                                                       
    
# (3) Train model (SVM)

X_train_np = np.array(X_train)                                                  # Convert to np.array for modelling (n_samples x n_features)
y_train_char = ['R' if x != 0 else 'U' for x in y_train]                        # 1s = R, 0s = U (better for classifier?)
y_train_np = np.array(y_train_char)                                             # Convert to np.array

from sklearn import svm
    
model = svm.SVC()
#model = svm.NuSVC()
#model = svm.LinearSVC()                                                         # This worked!
model.fit(X_train_np, y_train_np)

    
# (4) Test model

X_val_np = np.array(X_val)                                                      # Convert to np.array for modelling (n_samples x n_features)
test_results = model.predict(X_val_np)             


# (5) Assess model

values, counts = np.unique(test_results, return_counts=True)

test_results = list(test_results)
test_results = [str(x) for x in test_results]                                   # to convert to list of strings
y_val_char = ['R' if x != 0 else 'U' for x in y_val]                            # convert validation labels to char for comparison

test_results_passfail = ['Pass' if i == j else 'Fail' for i, j in zip(test_results, y_val_char)]
print("Model accurracy: ", math.floor(test_results_passfail.count('Pass') / len(test_results_passfail) * 100), "%" )

