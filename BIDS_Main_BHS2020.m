% BIDS-ify EEG-data related to AGF/MCN project 2018/19:


% addpath scripts
% addpath test_scripts
% addpath data
% addpath(genpath('test_scripts/BIDS/'));

% ismac           = 1;                                                        % input for Pathdefinitions
% BIDSfn          = 'BIDS_Main';
% BIDSfolder      = fileparts(which(BIDSfn)); 
% addpath(genpath(BIDSfolder))
% addpath(genpath('/Volumes/Samsung_T5/'));
% addpath(genpath('/Users/mheado86/Desktop/SCIENCE!/Programming/MATLAB/eeglab14_1_2b/functions/'));
% addpath(genpath('/Users/mheado86/Desktop/SCIENCE!/Programming/MATLAB/eeglab14_1_2b/plugins/'));


%% Define paths & directories
% TargetDir       = '/Volumes/SDUB/MarksData/BIDS/';                          % HDD paths
% rawEEGpath      = '/Volumes/SDUB/MarksData/EEG_00_raw/';
% fltEEGpath      = '/Volumes/SDUB/MarksData/EEG_01_filt/';                        
% icaEEGpath      = '/Volumes/SDUB/MarksData/EEG_02_ICclean/';

TargetDir       = 'data/BIDS_Sample/';                                      % Dropbox paths
rawEEGpath      = 'data/EEG_00_original/';
fltEEGpath      = 'data/EEG_01_filtered/';                                 
icaEEGpath      = 'data/EEG_02_icacleaned/';


%% Create central data object and sub-directories
%  ----------------------------------------------

% creation of central data structure "O"
O                 = [];
O.ProjectName     = 'ROGER_Open_Access';
O.TargetDir       = [TargetDir O.ProjectName];
O.RawEEGPath      = rawEEGpath;
O.FiltPath        = fltEEGpath;
O.BehPath         = 'data/BHV_01_processed/';
O.InfoPath        = 'data/BHV_02_info/';
O.ICAPath         = 'data/BHV_04_info_IC/';
O.LogPath         = 'data/LOG_oddball/';
O.CodeDir         = 'scripts/';
O.StimulusDir     = 'Task/1-Oddball_Neu/vis_tar/stimuli/';
O.EventInfo       = {};
O.General         = [];                                                   % general info from dataset_description.json
O.Participants    = {};                                                   % participant information for .tsv
O.PDesc           = [];                                                   % store participants json info
O.README          = 'Hello, welcome to the thunderdome!'; 
O.CHANGES         = 'Things change, that''s just the way it is...';
O.Stimuli         = {};

% delete directory if already existing
fprintf('Exporting data to %s...\n', O.TargetDir)
if exist(O.TargetDir, 'dir')
    disp('Deleting directory...')
    rmdir(O.TargetDir, 's');
end

% create sub-directories
mkdir( fullfile(O.TargetDir, 'code'    ))
mkdir( fullfile(O.TargetDir, 'stimuli' ))

%% Fill in task info
%  -----------------

% Define task info
Task.Name           = {'oddball' 'recog' 'varITI' };
Task.Description    = {'3-stim oddball with 10% Target & 10% Oddball'... 
                       'NEW and OLD oddballs presented in random sequence'... 
                       'Standards & Targets presented with variable Inter-Target-Interval'};
Task.Instructions   = {'Button press for all Targets'... 
                       'Button press: L for OLD & R for NEW'... 
                       'Button press for all Targets'};
        
% Fill structure                   
fnams  = fieldnames(Task);
for t = 1:size(fieldnames(Task),1)
    for fn = 1:size(Task.(fnams{t}),2)
        O.Tasks(t).(fnams{fn}) = Task.(fnams{fn}){t};
    end
end
        
% O.Tasks(1).Name                       = 'oddball';
% O.Tasks(1).Description                = 'Description of Task 1';
% O.Tasks(1).Instructions               = 'Task 1 instructions';
% O.Tasks(2).Name                       = 'recog';
% O.Tasks(2).Description                = 'Description of Task 2';
% O.Tasks(2).Instructions               = 'Task 2 instructions';
% O.Tasks(3).Name                       = 'varTTI';
% O.Tasks(3).Description                = 'Description of Task 3';
% O.Tasks(3).Instructions               = 'Task 3 instructions';

% Common task info
TInfo                               = [];
TInfo.InstitutionName               = 'Radboud University Nijmegen', 'University of Leipzig' ;
TInfo.InstitutionAddress            = 'Houtlaan 4, 6525 XZ Nijmegen, Netherlands', 'Augustusplatz 10, 04109 Leipzig, Germany' ;
TInfo.InstitutionDeptName           = ''; 									% @AGF?
TInfo.SamplingFrequency             = '500 Hz';
TInfo.EEGChannelCount               = '64';
TInfo.EOGChannelCount               = '4';
TInfo.ECGChannelCount               = '0';
TInfo.EMGChannelCount               = '1';                                  % @AGF: Is this the sternum electrode??
TInfo.EEGReference                  = 'A1 (L Mastoid)';
TInfo.PowerLineFrequency            = '50 Hz';
TInfo.EEGGround                     = 'Sternum';
TInfo.CogAtlasID                    = 'oddball task', 'memory encoding task';
TInfo.CogPOID                       = 'Stimulus: Modality = Visual, Type = explicit, object', 'Response: Modality = Hand, Type = Button Press', 'Instruction: Task1 = Respond to targets, Task2 = Respond to all stimuli by type, Task3 = Respond to targets '
TInfo.DeviceSerialNumber            = '';									% @AGF?
%TInfo.MiscChannelCount             = ''; 									% @AGF?					
%TInfo.TriggerChannelCount          = ''; 									% @AGF?
TInfo.EEGPlacementScheme            = 'extended 10-20 system';
TInfo.Manufacturer                  = 'Brain Products';
TInfo.ManufacturersModelName        = 'BrainAmp MR plus';
TInfo.CapManufacturer               = 'Brain Products';
TInfo.CapManufacturersModelName     = 'EasyCap';
TInfo.HardwareFilters               = ''; 									% @AGF?
TInfo.RecordingDuration             = ''; 									% @AGF?
TInfo.RecordingType                 = 'continuous';
TInfo.EpochLength                   = 'n/a';								% @AGF?
TInfo.SoftwareVersions              = ''; 									% @AGF?
TInfo.SubjectArtefactDescription    = '';

% software filter info
TInfo.SoftwareFilters.pop_eegfilt.HighPass          = 1;
TInfo.SoftwareFilters.pop_eegfilt.LowPass           = 90;
TInfo.SoftwareFilters.pop_iirfilt.Notch             = 'n/a';
TInfo.SoftwareFilters.pop_cleanline.LineFrequency   = 50;


%% write dataset_description.json
%  ------------------------------

dataset_label                   = 'dataset_description.json';
dataset_description_json_name   = fullfile(O.TargetDir, dataset_label);

% Fill in dataset description object
DSjson.Name                = O.ProjectName;                                 % name of the dataset
DSjson.Authors             = {'Adrian Georg Fischer',...
                              'Mark Cameron Nelson',...
                              'Some Other Guy'};                            % Who created/curated dataset

DSjson.BIDSVersion         = '1.3.1';                                       % The version of the BIDS standard that was used
DSjson.License             = '';                                            % what license is this dataset distributed under? 
DSjson.Acknowledgements    = '';                                            % who should be acknowledge in helping to collect the data
DSjson.HowToAcknowledge    = '';                                            % How to cite this dataset
DSjson.Funding             = {'','',''};                                    % sources of funding (grant numbers)
DSjson.ReferencesAndLinks  = {'','',''};                                    % references to publication that contain information on the dataset
DSjson.DatasetDOI          = '';                                            % the Document Object Identifier of the dataset
O.General                = DSjson;                                          

% Write JSON
%json_options.indent             = '    ';                                   % makes it look prettier when opened in a text editor
disp('Writing dataset_description.json...')
savejson('', DSjson, dataset_description_json_name);
% jsonwrite(dataset_description_json_name, opt.General, json_options)

%% write participant.tsv 
%  ---------------------

sub_label               = 'participants.tsv';
participants_tsv_name   = fullfile(O.TargetDir, sub_label);

% Fill participant data structure using subject-specific files (ODD_INFO)
SubFiles                = dir( [O.InfoPath '*.mat'] );                      % directory of participant info files
Subs(length(SubFiles))  = struct();

for iSubj = 1:length(SubFiles)
    load([O.InfoPath SubFiles(iSubj).name]);                                % load participant specific info structure (ODD_INFO)
    
    Subs(iSubj).Participant_id          = [sprintf('sub-%3.3d',iSubj) '       ']; % subject id field
    
    if ODD_INFO.Age ~= 0
        Subs(iSubj).Age                 = ODD_INFO.Age;                     % subject age
    else
        Subs(iSubj).Age                 = 'n/a';
    end
    
    switch ODD_INFO.Gender                                
        case 1   ; Subs(iSubj).Sex      = ' M '; 
        case 2   ; Subs(iSubj).Sex      = ' F '; 
        otherwise; Subs(iSubj).Sex      = 'n/a'; 
    end
        
    switch ODD_INFO.Hand                                                    
        case 1   ; Subs(iSubj).Hand     = ' R  ';
        case 2   ; Subs(iSubj).Hand     = ' A  ';
        case 3   ; Subs(iSubj).Hand     = ' L  ';
        otherwise; Subs(iSubj).Hand     = 'n/a '; 
    end
end

% Write .tsv file
% opt.Participants    = Subs;
t                   = struct2table(Subs);
disp('Writing participants.tsv...')
writetable(t, participants_tsv_name, 'FileType', 'text', 'Delimiter', '\t');

%% write participants.json
%  -----------------------

sub_label                           = 'participants.json';
participants_json_name              = fullfile(O.TargetDir, sub_label);

% Fill in participant description object  
Pjson                               = [];
Pjson.participant_id.LongName       = 'Participant ID';
Pjson.participant_id.Description    = 'Participant identification tag';
Pjson.age.LongName                  = 'age'; 
Pjson.age.Description               = 'age of the participant';
Pjson.age.Units                     = 'Years';
Pjson.sex.LongName                  = 'Gender';                                        
Pjson.sex.Description               = 'Gender';
Pjson.sex.Levels.M                  = 'Male';
Pjson.sex.Levels.F                  = 'Female';
Pjson.Handedness.LongName           = 'Handedness';                                
Pjson.Handedness.Description        = 'Dominant hand of participant';
Pjson.Handedness.Levels.L           = 'Left';
Pjson.Handedness.Levels.R           = 'Right';
Pjson.Handedness.Levels.A           = 'Ambidextrous';
O.PDesc                           =  Pjson;                                 % store in central structure

% Write JSON
%json_options.indent         = '    ';                                      % makes it look prettier when opened in a text editor
disp('Writing participants.json...')
savejson('', Pjson, participants_json_name);

%% Write README and CHANGES files
%  ------------------------------

if ~isempty(O.README)                                                       % check for string in central data structure
    if ~exist(O.README, 'file')                                             % check for existence of file in directory
        fid = fopen(fullfile(O.TargetDir, 'README'), 'w');                  % create empty file
        if fid == -1, error('Cannot write README file'); end
        fprintf(fid, '%s', O.README);                                       % print README string into new file
        fclose(fid);
    else
        copyfile(O.README, fullfile(O.TargetDir, 'README'));                % copy file if existing
    end
end

if ~isempty(O.CHANGES)                                                      % check for string in central data structure
    if ~exist(O.CHANGES, 'file')                                            % check for existence of file in directory
        fid = fopen(fullfile(O.TargetDir, 'CHANGES'), 'w');                 % create empty file
        if fid == -1, error('Cannot write README file'); end
        fprintf(fid, '%s', O.CHANGES);                                      % print CHANGES string into new file
        fclose(fid);
    else
        copyfile(O.CHANGES, fullfile(O.TargetDir, 'CHANGES'));              % copy file if existing
    end
end

%% write code files
%  ----------------

O.CodeFiles       = dir([O.CodeDir '*.m']);                                 % load script files in code dir into structure
if ~isempty(O.CodeFiles)
    for iFile = 1:length(O.CodeFiles)
        [~,FileName,Ext] = fileparts(O.CodeFiles(iFile).name);
        if ~isempty(dir([O.CodeDir O.CodeFiles(iFile).name]))
            copyfile([O.CodeDir O.CodeFiles(iFile).name],... 
                      fullfile(O.TargetDir, 'code', [ FileName Ext ]));
        else
            fprintf('Warning: cannot find code file %s\n',... 
                     O.CodeFiles(iFile).name)
        end
    end
end

%% write stimulus files
%  --------------------

O.StimulusFiles = dir([O.StimulusDir '*.bmp']);                             % load stimulus files into structure
if ~isempty(O.StimulusFiles)
    %if size(opt.StimuliDir,1) == 1, opt.StimuliFiles = dir(opt.Stimuli'; end
    for iStim = 1:length(O.StimulusFiles)
        [~,FileName,Ext] = fileparts(O.StimulusFiles(iStim).name);
        if ~isempty(dir([O.StimulusDir O.StimulusFiles(iStim).name]))
            if iStim < (length(O.StimulusFiles)-1)                          % Rename stimulus files
                FileName = ['Oddball_' sprintf('%03d',str2double(FileName))];
            elseif iStim == (length(O.StimulusFiles)-1)
                FileName = 'Standard';
            else
                FileName = 'Target';
            end
            copyfile([O.StimulusDir O.StimulusFiles(iStim).name],... 
                      fullfile(O.TargetDir, 'stimuli', [ FileName Ext ]));
        else
            fprintf('Warning: cannot find stimulus file %s\n', O.StimulusFiles(iStim).name);
        end
    end
end

%% Write common channels.tsv file (Inheritance Principle)
%  ------------------------------------------------------

load('data/data/OddballChanlocs.mat');                                      % load common electrode/channel file
channels_label          = 'channels.tsv';                                   % create file label
channels_tsv_name       = fullfile(O.TargetDir, channels_label);            % create channels.tsv file name
Cinfo                   = OddballChanlocs;
Chans(length(Cinfo))    = struct('Name',[],'Type',[],'Units',[],...
                                 'Description',[],'Sampling_Frequency',[]); % initialize channel info structure
     
for iChan = 1:length(Chans)
    Chans(iChan).Name                   = Cinfo(iChan).labels;              % channel name  
    Chans(iChan).Units                  = '  uV  ';                         % channel units
    Chans(iChan).Sampling_Frequency     = '       500        ';             % sampling frequency
                                                                            % channel type & description
    if     iChan == 60 || iChan == 61;  Chans(iChan).Type = 'VEOG';  Chans(iChan).Description = ' Vertical  ';
    elseif iChan == 62 || iChan == 63;  Chans(iChan).Type = 'HEOG';  Chans(iChan).Description = 'Horizontal ';
    elseif iChan == 64;                 Chans(iChan).Type = 'EEG ';  Chans(iChan).Description = ' R Mastoid ';
    else                                Chans(iChan).Type = 'EEG ';  Chans(iChan).Description = '    n/a    '; 
    end
end

% write .tsv file
O.ChannelsInfo    = Chans;
t                   = struct2table(Chans);                                  % write cell to table
disp('Writing channels.tsv...')
writetable(t, channels_tsv_name, 'FileType', 'text', 'Delimiter', '\t');    % write table to .tsv file

    
%% Write common electrodes.tsv (Inheritance Principle)
%  ---------------------------------------------------

electrodes_label                = 'electrodes.tsv';                         % create label
electrodes_tsv_name             = fullfile(O.TargetDir, electrodes_label);  % file name
Elecs(length(Cinfo))            = struct('Name',[],'X',[],'Y',[],'Z',[],...
                                         'Electrode_Type',[],'Material',[]);% Initialize electrode info structure

for iElec = 1:(length(Cinfo)+2)                                             % CAN I ALIGN THEM BY DECIMAL POINT?
    if iElec <= length(Cinfo)
        Elecs(iElec).Name           = [Cinfo(iElec).labels ' '];            % electrode name  
        Elecs(iElec).X              = sprintf('%.4f',round(Cinfo(iElec).X,3)); % electrode x coord   DOES IT MAKE SENSE TO ROUND COORDINATES TO 3 DIGITS?  *AGF*  --> if this is not a bids requirement, I would use 5 digits (i.e, 0.9511)
        Elecs(iElec).Y              = sprintf('%.4f',round(Cinfo(iElec).Y,3)); % electrode y coord
        Elecs(iElec).Z              = sprintf('%.4f',round(Cinfo(iElec).Z,3)); % electrode z coord
        Elecs(iElec).Electrode_Type = ' Elastic Cap  ';                     % electrode type
        Elecs(iElec).Material       = 'Ag/AgCl ';                           % electrode material
    else
        switch iElec 
            case length(Cinfo)+1
                Elecs(iElec).Name           = 'A1  ';                       % electrode name
%                Elecs(iElec).X              = sprintf('%.3f',round(Cinfo(64).X,3)); % electrode x coord
%                Elecs(iElec).Y              = sprintf('%.3f',round(Cinfo(64).Y,3)); % electrode y coord  WHAT WOULD YOU PUT FOR THE REFERENCE ELECTRODE COORDINATES? *AGF* --> Should be:  X: -0.2728 Y: 0.8397 Z: -0.4695
%                Elecs(iElec).Z              = sprintf('%.3f',round(Cinfo(64).Z,3)); % electrode z coord
                Elecs(iElec).X              = '-0.2728'; 							% electrode x coord
                Elecs(iElec).Y              = '0.8397'; 							% electrode y coord
                Elecs(iElec).Z              = '-0.4695'; 							% electrode z coord
                Elecs(iElec).Electrode_Type = ' Elastic Cap  '; 					% electrode type
                Elecs(iElec).Material       = 'Ag/AgCl '; 							% electrode material
            case length(Cinfo)+2
                Elecs(iElec).Name           = 'Grnd';                       % electrode name
                Elecs(iElec).X              = 'sternum';                    % electrode x coord
                Elecs(iElec).Y              = 'sternum';                    % electrode y coord   WHAT WOULD YOU PUT FOR THE GROUND COORDINATES? *AGF*  --> do not think there are coordinates for grnd
                Elecs(iElec).Z              = 'sternum';                    % electrode z coord
                Elecs(iElec).Electrode_Type = ' Elastic Cap  ';             % electrode type
                Elecs(iElec).Material       = 'Ag/AgCl';                    % electrode material
        end % switch
    end % if statement
end % loop

% write .tsv file
O.ElectrodesInfo  = Elecs;
t                   = struct2table(Elecs);                                  % write strcture to table
disp('Writing electrodes.tsv...')
writetable(t, electrodes_tsv_name, 'FileType', 'text', 'Delimiter', '\t'); % write table to .tsv file
    
%% Write common coordsystem.json (Inheritance Principle)
%  -----------------------------------------------------

coordsystem_label       = 'coordsystem.json';
coordsystem_json_name   = fullfile(O.TargetDir, coordsystem_label);

% Fill in object
Cjson                                 = [];
Cjson.IntendedFor                     = 'sub-ALL_ses-ALL_task-ALL_eeg';
Cjson.EEGCoordinateSystem             = ''; 							% @AGF
Cjson.EEGCoordinateUnits              = 'mm'; 							% @AGF (right?)
Cjson.EEGCoordinateSystemDescription  = '';

% Write JSON
% json_options.indent         = '    ';                                       % makes it look prettier when opened in a text editor
disp('Writing coordsystem.json...')
savejson('', Cjson, coordsystem_json_name);


%% Write task-specific events.json
%  -------------------------------

for iTask               = 1:length(O.Tasks)
    json_label          = ['task-' O.Tasks(iTask).Name '_events.json'];
    events_json_name    = fullfile(O.TargetDir, json_label);
    
    % Fill in events object 
    Ejson                           = [];
    Ejson.onset.Description         = 'Time point marking the beginning of the event relative to start of recording (t=0)';
    Ejson.onset.Units               = 'Seconds';
    Ejson.duration.Description      = 'Length of time of event';
    Ejson.duration.Units            = 'Seconds';
    Ejson.trial_type.Description    = 'Class or nature of trial';
    switch iTask
        case 1
            Ejson.trial_type.Levels.Standard    = 'Standard stimulus presentation (common)';
            Ejson.trial_type.Levels.Target      = 'Target stimulus presentation (rare)';
            Ejson.trial_type.Levels.Oddball_000 = 'Oddball stimulus presentation (rare), Number cooresponds to stimulus id';
            Ejson.trial_type.Levels.Response    = 'Button press in response to target recognition';
            Ejson.trial_type.Levels.Ready       = 'Button press indicating participant is ready to begin task';
            Ejson.trial_type.Levels.Miss        = '' ;
            
        case 2
            Ejson.trial_type.Levels.Oddball_000_OLD  = 'Presentation of Oddball previously shown in Task 1, Number cooresponds to stimulus id';
            Ejson.trial_type.Levels.Oddball_000_NEW  = 'Presentation of novel Oddball (NOT previously shown in Task 1), Number cooresponds to stimulus id';
            Ejson.trial_type.Levels.Response1        = '';    % <---- @AGF L or R  button press?
            Ejson.trial_type.Levels.Response2        = '';
            Ejson.trial_type.Levels.Response_Ready   = 'Button press indicating participant is ready to begin task';
            Ejson.trial_type.Levels.Feedback_Miss    = 'Response not registered in alotted time window (2 sec)';
            Ejson.trial_type.Levels.Feedback_Correct = 'Oddball correctly identified as OLD or NEW';
            Ejson.trial_type.Levels.Feedback_Incorre = 'Oddball incorrectly identified as OLD or NEW';
            
        case 3
            Ejson.trial_type.Levels.Standard   = 'Standard stimulus presentation (common)';
            Ejson.trial_type.Levels.Target00   = 'Target stimulus presentation (rare), Number corresponds to quantity of standard stimuli presented since previous target';
            Ejson.trial_type.Levels.Response   = 'Button press in response to target recognition';
            Ejson.trial_type.Levels.Ready      = 'Button press indicating participant is ready to begin task';
            Ejson.trial_type.Levels.Miss       = 'Incorrect or missing response';
    end
    
    % Write JSON
    %json_options.indent         = '    ';                                    % makes it look prettier when opened in a text editor
    fprintf('Writing %s...\n', json_label)
    savejson('', Ejson, events_json_name);

end

%% Write task-specific eeg.json
%  ----------------------------
        
for iTask               = 1:length(O.Tasks)
    eeg_label           = ['task-' O.Tasks(iTask).Name '_eeg.json'];
    eeg_json_name       = fullfile(O.TargetDir, eeg_label);
    Tjson               = [];
    
    % Fill in object
    Tjson.Name                          = O.Tasks(iTask).Name;
    Tjson.Description                   = O.Tasks(iTask).Description;
    Tjson.Instructions                  = O.Tasks(iTask).Instructions;
    Tjson.InstitutionName               = TInfo.InstitutionName;
    Tjson.InstitutionAddress            = TInfo.InstitutionAddress;
    Tjson.InstitutionDepartmentName     = TInfo.InstitutionDeptName;
    Tjson.SamplingFrequency             = TInfo.SamplingFrequency;
    Tjson.EEGChannelCount               = TInfo.EEGChannelCount;
    Tjson.EOGChannelCount               = TInfo.EOGChannelCount;
    Tjson.ECGChannelCount               = TInfo.ECGChannelCount;
    Tjson.EMGChannelCount               = TInfo.EMGChannelCount;
    Tjson.EEGReference                  = TInfo.EEGReference;
    Tjson.PowerLineFrequency            = TInfo.PowerLineFrequency;
    Tjson.EEGGround                     = TInfo.EEGGround;
    Tjson.CogAtlasID                    = TInfo.CogAtlasID;
    Tjson.CogPOID                       = TInfo.CogPOID;
    Tjson.DeviceSerialNumber            = TInfo.DeviceSerialNumber;
    Tjson.MiscChannelCount              = TInfo.MiscChannelCount;
    Tjson.TriggerChannelCount           = TInfo.TriggerChannelCount;
    Tjson.EEGPlacementScheme            = TInfo.EEGPlacementScheme;
    Tjson.Manufacturer                  = TInfo.Manufacturer;
    Tjson.ManufacturersModelName        = TInfo.ManufacturersModelName;
    Tjson.CapManufacturer               = TInfo.CapManufacturer;
    Tjson.CapManufacturersModelName     = TInfo.CapManufacturersModelName;
    Tjson.HardwareFilters               = TInfo.HardwareFilters;
    Tjson.SoftwareFilters               = TInfo.SoftwareFilters;
    Tjson.RecordingDuration             = TInfo.RecordingDuration;
    Tjson.RecordingType                 = TInfo.RecordingType;
    Tjson.EpochLength                   = TInfo.EpochLength;
    Tjson.SoftwareVersions              = TInfo.SoftwareVersions;
    Tjson.SubjectArtefactDescription    = TInfo.SubjectArtefactDescription;
    
    % Write JSON
%     json_options.indent         = '    ';                                   % makes it look prettier when opened in a text editor
    fprintf('Writing %s...\n', eeg_label)
    savejson('', Tjson, eeg_json_name);
end

%% ------------------------------------------------------------------------
%%%%%%%% Write subject- & task-specific files (behavioral & EEG) %%%%%%%%%%
%--------------------------------------------------------------------------

Subjn            = 3;
for iSubj        = 1:Subjn 
    OldSubjStr   = sprintf('VP%3.4d', iSubj);
    NewSubjStr   = sprintf('sub-%3.3d', iSubj);
    PartDir      = [O.TargetDir '/' NewSubjStr '/eeg/'];
    mkdir(fullfile([O.TargetDir], [NewSubjStr '/eeg']));                    % create subject-specific folder

    
    % index available data for each participant
    Tasks = [0 0 0];
    if     exist([O.LogPath OldSubjStr '_1a-vis_tar_exp1a.log'  ],'file'); Tasks(1)=1;end
    if     exist([O.LogPath OldSubjStr '_1aa-vis_tar_reco_a.log'],'file'); Tasks(2)=1;
    elseif exist([O.LogPath OldSubjStr '_1ab-vis_tar_reco_b.log'],'file'); Tasks(2)=2;end
    if     exist([O.LogPath OldSubjStr '_2a-vis_tar_exp2a.log'  ],'file'); Tasks(3)=1;end 
    
    %% copy raw eeg files
    %  ------------------
    
    disp('Copying raw EEG files...')
                                                                                % are these file endings correct BIDS format?
                                                                                % _eeg.eeg?
    % task 1
    switch Tasks(1)
        case 1
            copyfile([O.RawEEGPath OldSubjStr '_1a.eeg'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(1).Name '.eeg']);
            copyfile([O.RawEEGPath OldSubjStr '_1a.vhdr'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(1).Name '.vhdr']);
            copyfile([O.RawEEGPath OldSubjStr '_1a.vmrk'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(1).Name '.vmrk']);
        otherwise
            fprintf('No Task 1 data found for %s...\n', NewSubjStr)
    end
         
    % task 2 (variants a & b)
    switch Tasks(2)
        case 1
            copyfile([O.RawEEGPath OldSubjStr '_1aa.eeg'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(2).Name '_a.eeg']);
            copyfile([O.RawEEGPath OldSubjStr '_1aa.vhdr'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(2).Name '_a.vhdr']);
            copyfile([O.RawEEGPath OldSubjStr '_1aa.vmrk'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(2).Name '_a.vmrk']);
        case 2
            copyfile([O.RawEEGPath OldSubjStr '_1ab.eeg'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(2).Name '_b.eeg']);
            copyfile([O.RawEEGPath OldSubjStr '_1ab.vhdr'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(2).Name '_b.vhdr']);
            copyfile([O.RawEEGPath OldSubjStr '_1ab.vmrk'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(2).Name '_b.vmrk']);
        otherwise
            fprintf('No Task 2 data found for %s...\n', NewSubjStr)
    end

    % task 3
    switch Tasks(3)
        case 1
            copyfile([O.RawEEGPath OldSubjStr '_2a.eeg'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(3).Name '.eeg']);
            copyfile([O.RawEEGPath OldSubjStr '_2a.vhdr'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(3).Name '.vhdr']);
            copyfile([O.RawEEGPath OldSubjStr '_2a.vmrk'],...
                     [PartDir NewSubjStr '_task-' O.Tasks(3).Name '.vmrk']);
        otherwise
            fprintf('No Task 3 data found for %s...\n', NewSubjStr)
    end   
        
    %% read in event info & write events.tsv (behavioral data)
    %  -------------------------------------------------------
    
    % Task 1
    if Tasks(1) == 1
        fend1           = '_1a-vis_tar_exp1a.log';                          % behavioral data filename
        fend2           = '_events.tsv'; 
        events_label    = [NewSubjStr '_task-' O.Tasks(1).Name fend2];      % label for events.tsv file
        events_tsv_name = fullfile(PartDir, events_label);                  % events.tsv file name
        path            = 1;                                                % path 1 = Task 1
        Events          = BIDS_EventRead([O.LogPath OldSubjStr fend1], path); % call to custom function
        t               = struct2table(Events);                             % write structure to table
        fprintf('Writing %s...\n', events_label)
        writetable(t, events_tsv_name, 'FileType', 'text', 'Delimiter', '\t'); % write table to .tsv file
    end
        
    
    % Task 2
    if Tasks(2) ~= 0
        switch Tasks(2)
            case 1; fend1 = '_1aa-vis_tar_reco_a.log'; fend2 = '_a_events.tsv';
            case 2; fend1 = '_1ab-vis_tar_reco_b.log'; fend2 = '_b_events.tsv';
        end 
        events_label    = [NewSubjStr '_task-' O.Tasks(2).Name fend2];      % label for events.tsv file
        events_tsv_name = fullfile(PartDir, events_label);                  % events.tsv file name
        path            = 2;                                                % path 2 = task 2
        Events          = BIDS_EventRead([O.LogPath OldSubjStr fend1],path); % call to custom function
        t               = struct2table(Events);                             % write structure to table
        fprintf('Writing %s...\n', events_label)
        writetable(t, events_tsv_name, 'FileType', 'text', 'Delimiter', '\t'); % write table to .tsv file
    end
    
    
    % Task 3
    if Tasks(3) == 1
        fend1           = '_2a-vis_tar_exp2a.log';                          % behavioral data filename
        fend2           = '_events.tsv';
        events_label    = [NewSubjStr '_task-' O.Tasks(3).Name fend2];      % label for events.tsv file
        events_tsv_name = fullfile(PartDir, events_label);                  % events.tsv file name
        path            = 3;                                                % path 3 = Task 3
        Events          = BIDS_EventRead([O.LogPath OldSubjStr fend1],path);% call to custom function
        t               = struct2table(Events);                             % write structure to table
        fprintf('Writing %s...\n', events_label)
        writetable(t, events_tsv_name, 'FileType', 'text', 'Delimiter', '\t'); % write table to .tsv file
    end
end % loop over participants

%-------------------------------------------------------------------------------------------------------------------------------------
%% BIDS DERIVATIVES
%-------------------------------------------------------------------------------------------------------------------------------------

O.D.PipelineName  = 'Pipeline01';
O.D.TargetDir     = [O.TargetDir '/derivatives/' O.D.PipelineName];
O.D.README        = 'Never Eat Soggy Waffles';
O.D.General       = [];                                                     % store derivative dataset_description.json here

mkdir([O.TargetDir '/derivatives/' O.D.PipelineName])

%% Derivatives dataset_description.json
%  ------------------------------------

dataset_label                   = 'dataset_description.json';
dataset_description_json_name   = fullfile(O.D.TargetDir, dataset_label);

% Fill in dataset description object
D.PipelineDescription.Name      = O.D.PipelineName;                         % name of the pipeline
D.PipelineDescription.Version   = '';
D.SourceDatasets                = '';
O.D.General                     = D;                                        % store in central structure

% Write JSON
disp('Writing derivatives dataset_description.json...')
savejson('', D, dataset_description_json_name);

%% Write README
%  ------------

if ~isempty(O.D.README)                                                     % check for string in central data structure
    if ~exist(O.D.README, 'file')                                           % check for existence of file in directory
        fid = fopen(fullfile(O.D.TargetDir, 'README'), 'w');                % create empty file
        if fid == -1, error('Cannot write README file'); end
        fprintf(fid, '%s', O.D.README);                                     % print README string into new file
        fclose(fid);
    else
        copyfile(O.D.README, fullfile(O.D.TargetDir, 'README'));            % copy file if existing
    end
end

%% ------------------------------------------------------------------------
%%%%%%%%%%%%%%%  Write subject-specific derivative files  %%%%%%%%%%%%%%%%%
%--------------------------------------------------------------------------

% create labels for mixing.tsv
comps = {};
chans = {};
for i = 1:length(OddballChanlocs)
    comps{i} = ['Comp' num2str(i)];
    chans{i} = ['       ' OddballChanlocs(i).labels '       '];
    if i == 60; chans{i} = 'Vplus'; end                                     % V+ doesn't work
end

Subjn            = 3;
fname            = '_task-merged_desc-filtered_';

for iSubj        = 1:Subjn 
    OldSubjStr   = sprintf('VP%3.4d', iSubj);
    NewSubjStr   = sprintf('sub-%3.3d', iSubj);
    DPartDir     = [O.D.TargetDir '/' NewSubjStr '/eeg/'];
    mkdir(fullfile([O.D.TargetDir], [NewSubjStr '/eeg']));                  % create subject-specific folder

    % copy derivative files to BIDS directory
    if exist([O.FiltPath OldSubjStr '.set'],'file') 
        copyfile([O.FiltPath OldSubjStr '.set'],...
                 [DPartDir NewSubjStr fname 'eeg.set']); 
    end
    if exist([O.FiltPath OldSubjStr '.fdt'],'file') 
        copyfile([O.FiltPath OldSubjStr '.fdt'],...
                 [DPartDir NewSubjStr fname 'eeg.fdt']); 
    end
    
    %% Create derivatives .json sidecar
    %  --------------------------------
    
    D_label       = [NewSubjStr fname 'eeg.json'];
    D_json_name   = fullfile(DPartDir, D_label);

    % create json object
    Djson                   = [];                                          
    Djson.Description       = 'This file represents the filtered & merged datasets from all 3 tasks';
    Djson.Sources.Task1     = [O.ProjectName '/' NewSubjStr '/eeg/' [NewSubjStr '_task-' O.Tasks(1).Name '.eeg']];
    Djson.Sources.Task2     = [O.ProjectName '/' NewSubjStr '/eeg/' [NewSubjStr '_task-' O.Tasks(2).Name '.eeg']];
    Djson.Sources.Task3     = [O.ProjectName '/' NewSubjStr '/eeg/' [NewSubjStr '_task-' O.Tasks(3).Name '.eeg']];
    
    % Software filter
    Djson.SoftwareFilters.pop_eegfilt.FilterType        = '';               %<--          % **AGF: CAN YOU FINISH THIS SECTION PLEASE
    Djson.SoftwareFilters.pop_eegfilt.FilterOrder       = '';               %<--
    Djson.SoftwareFilters.pop_eegfilt.HighPass          = TInfo.SoftwareFilters.pop_eegfilt.HighPass;
    Djson.SoftwareFilters.pop_eegfilt.LowPass           = TInfo.SoftwareFilters.pop_eegfilt.LowPass;
    Djson.SoftwareFilters.pop_iirfilt.FilterType        = 'notch';
    Djson.SoftwareFilters.pop_iirfilt.FilterOrder       = '';               %<--
    Djson.SoftwareFilters.pop_iirfilt.Notch             = TInfo.SoftwareFilters.pop_iirfilt.Notch;
    Djson.SoftwareFilters.pop_cleanline.FilterType      = 'notch';
    Djson.SoftwareFilters.pop_cleanline.FilterOrder     = '';               %<--
    Djson.SoftwareFilters.pop_cleanline.LineFrequency   = TInfo.SoftwareFilters.pop_cleanline.LineFrequency;
    Djson.Detrending                                    = 'none';                                     
    Djson.SamplingFrequency                             = TInfo.SamplingFrequency;
    Djson.IsDownsampled                                 = 'False';                      % **AGF: IS THERE ANYTHING ELSE VITAL FOR THEM TO KNOW ABOUT OUR FILTRATION PROCESS?
                                                                                         
    
    % Write JSON
    fprintf('Writing %s...\n', D_label)
    savejson('', Djson, D_json_name);
    
    %% Create 2 mixing.tsv for icasphere and icaweights (2 files per participant)
    %  ------------------------------------------------
    
    sphere_mixing_label     = [NewSubjStr '_task-merged_desc-sphere_mixing.tsv']; % create file label
    weight_mixing_label     = [NewSubjStr '_task-merged_desc-weight_mixing.tsv']; % create file label
    sphere_mixing_tsv_name  = fullfile(DPartDir, sphere_mixing_label);      % create channels.tsv file name
    weight_mixing_tsv_name  = fullfile(DPartDir, weight_mixing_label);      % create channels.tsv file name
    
    % load ICA info (ODD_INFO) & read into table                                                                                          
    load([O.ICAPath OldSubjStr '.mat'])
    
    ts = array2table(ODD_INFO.AMICA_icasphere,  'VariableNames', chans, 'RowNames', comps); 
    tw = array2table(ODD_INFO.AMICA_icaweights, 'VariableNames', chans, 'RowNames', comps);
    
    % write .tsv files
    fprintf('Writing %s & %s...\n',sphere_mixing_label, weight_mixing_label)
    writetable(ts, sphere_mixing_tsv_name, 'FileType', 'text', 'Delimiter', '\t'); % write table to .tsv file
    writetable(tw, weight_mixing_tsv_name, 'FileType', 'text', 'Delimiter', '\t'); % write table to .tsv file

end % loop over participants