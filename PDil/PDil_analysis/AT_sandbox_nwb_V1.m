%add github w/ nwb package to path

% dat = nwb.acquisition.get('channel_9').data.load

%picking up 6/3/20; have run through 'importing pt 01 POD2 data, tutorial
%day 2 and 3' and 'importing pt 01 POD4 data, tutorial day 2 and 3' on
%jupyter; and then downloaded the nwb files from 'files' on jupyter to
%local computer

%notes - 'acquisition' is their ephys data

generateCore()

nwb = nwbRead('/Users/andytek/Downloads/PO_Day_02.nwb');

%note EC has put the data under 'processing', 
dat = nwb.acquisition.get('wire_14_electrode_5').data.load;
trials = nwb.intervals_trials.loadAll;

size(dat)

figure()
plot(dat(1:10000))




% dat = nwb.acquisition.('wire_14_electrode_5').data.load
% 
% 
% 
% 
% nwb.acquisition['wire_14_electrode_5']
% 'wire_14_electrode_5