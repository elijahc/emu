%AT 12/9/19 creating script for PD challenge in the EMU

function [rsp] = PDilemma_V1()

dbstop if error


%VOICE is 'daisy' from http://www.fromtexttospeech.com/, medium paced



% t = timer('TimerFcn', 'stat=false; disp('    'Timer!'')',... 
% 'StartDelay',100);
% start(t)
% stat=true;
% dispTime = 1;
% while(stat==true)
%   disp(dispTime)
%   pause(1)
% dispTime = dispTime + 1; 
% end

% 
%  Datapixx('Open'); 
%  DatapixxAOttl() %FOR TTL 

%The script OSXCompositorIdiocyTest() is a "must run" for OSX users, to make sure their system doesn't have the OSX compositor bug, especially on OSX 10.8 and later. If that test fails then visual stimulation timing must be considered not trustworthy.
%The script VBLSyncTest() allows you to assess the timing of Psychtoolbox on your specific setup in a variety of conditions. It expects many parameters and displays a couple of plots at the end, so there is no way around reading the 'help VBLSyncTest' if you want to use it.
wholetrial = tic;
opening = tic;

%note: some of the sounds need to be doubled up for stereo, some don't -
%depends on the mp3 file
%% loading in audio files (not all used. depends)
%130Hz
[data, fs] = audioread('audiocheck.net_sin_130.8Hz_-3dBFS_1s.wav'); 
tone1_fs = fs;
data_conc = data';
tone1_sound = [data_conc;data_conc];
clear data;clear data_conc;clear fs
%233Hz
[data, fs] = audioread('audiocheck.net_sin_233Hz_-3dBFS_1s.wav');
tone2_fs = fs;
data_conc = data';
tone2_sound = [data_conc;data_conc];
clear data;clear data_conc;clear fs
%261.6Hz
[data, fs] = audioread('audiocheck.net_sin_261.6Hz_-3dBFS_1s.wav'); 
tone3_fs = fs;
data_conc = data';
tone3_sound = [data_conc;data_conc];
clear data;clear data_conc;clear fs
%293Hz
[data, fs] = audioread('audiocheck.net_sin_293Hz_-3dBFS_1s.wav');
tone4_fs = fs;
data_conc = data';
tone4_sound = [data_conc;data_conc];
clear data;clear data_conc;clear fs
%523Hz
[data, fs] = audioread('audiocheck.net_sin_523Hz_-3dBFS_1s.wav');
tone5_fs = fs;
data_conc = data';
tone5_sound = [data_conc;data_conc];
clear data;clear data_conc;clear fs
%Go Beep, 2 sin wave @ 523 and 130Hz
[data, fs] = audioread('audiochecknet_130Hz_-7dBFS_523Hz_-7dBFS_05s.wav');
gobeep_fs = fs;
data_conc = data';
gobeep_sound = [data_conc;data_conc];
clear data;clear data_conc;clear fs
%hellomynameisdaisy
[data, fs] = audioread('hellomynameisdaisy.mp3');
sound_hellomynameisdaisy_fs = fs;
data_conc = data';
sound_hellomynameisdaisy = [data_conc;data_conc];
clear data;clear data_conc;clear fs
%pleasebeginafterthefollowingtone
[data, fs] = audioread('whenyouareready_.mp3');
sound_whenyouareready_fs = fs;
data_conc = data';
sound_whenyouareready = [data_conc;data_conc];
clear data;clear data_conc;clear fs
%next
[data, fs] = audioread('next_.mp3');
sound_next_fs = fs;
data_conc = data';
sound_next = [data_conc;data_conc];
clear data;clear data_conc;clear fs
%correctbeep
[data, fs] = audioread('correctbeep.mp3');
sound_correctbeep_fs = fs;
data_conc = data';
sound_correctbeep = data_conc;
%incorrectbeep
[data, fs] = audioread('incorrectbeep.mp3');
sound_incorrectbeep_fs = fs;
data_conc = data';
sound_incorrectbeep = [data_conc;data_conc];
clear data;clear data_conc;clear fs
%pleasecontinuetoholduntil
[data, fs] = audioread('pleasecontinuetoholduntil.mp3');
sound_pleasecontinuetoholduntil_fs = fs;
data_conc = data';
sound_pleasecontinuetoholduntil = [data_conc;data_conc];
clear data;clear data_conc;clear fs
%then
% [data, fs] = audioread('then.mp3');
% sound_then_fs = fs;
% data_conc = data';
% sound_then = [data_conc;data_conc];
% clear data;clear data_conc;clear fs
%% load('input_matrix_rndm.mat')
% load('input_matrix_rndm_Nov13th.mat', 'input_matrix_rndm') %full input
input_matrix_rndm = [1,2,301,302,4,5]'; %abridged input
% input_matrix_rndm = [1,2,301,302,4,5,301,301,301,301,301,301,1,2,301,302,4,5]'; %abridged input
% load('inputshorten.mat', 'inputshorten') %
% input_matrix_rndm = inputshorten;

input_fss = zeros(length(input_matrix_rndm),1);
input_tones =  cell(length(input_matrix_rndm),1);
input_correct = zeros(length(input_matrix_rndm),1);
s = struct('in',input_matrix_rndm,'fs',input_fss,'tones',input_tones,'correct',input_correct);
% extending input_matrix_rndm variable into a structure we will subsequently pull from
for i = 1:length(input_matrix_rndm)
    if input_matrix_rndm(i,1) == 1
        s(i).in = input_matrix_rndm(i);
        s(i).fs = tone1_fs;
        s(i).tones = mat2cell(tone1_sound,2,44101);
        s(i).correct = 1;%means left is correct response
        %input_fss(i) = tone1_fs; %keeping these just as example of another
        %way to execute code if need be
        %tone1_holder = mat2cell(tone1_sound,2,44101);
        %input_tones(i) = {tone1_holder};
        %input_correct(i) = 1; 
    elseif input_matrix_rndm(i,1) == 2
        s(i).in = input_matrix_rndm(i);s(i).fs = tone2_fs;s(i).tones = mat2cell(tone2_sound,2,44101);s(i).correct = 1;
    elseif input_matrix_rndm(i,1) == 301
        s(i).in = input_matrix_rndm(i);s(i).fs = tone3_fs;s(i).tones = mat2cell(tone3_sound,2,44101);s(i).correct = 1;
    elseif input_matrix_rndm(i,1) == 302
        s(i).in = input_matrix_rndm(i);s(i).fs = tone3_fs;s(i).tones = mat2cell(tone3_sound,2,44101);s(i).correct = 2;
    elseif input_matrix_rndm(i,1) == 4
        s(i).in = input_matrix_rndm(i);s(i).fs = tone4_fs;s(i).tones = mat2cell(tone4_sound,2,44101);s(i).correct = 2;
    elseif input_matrix_rndm(i,1) == 5
        s(i).in = input_matrix_rndm(i);s(i).fs = tone5_fs;s(i).tones = mat2cell(tone5_sound,2,44101);s(i).correct = 2;
    end
end
%% call arduino
a = arduino();
addrs = scanI2CBus(a);
nC1 = i2cdev(a, char(addrs) , 'bus' , 0);

joyXoffset = 127;
joyYoffset = 128;
%acceloffset = 512;
%%
%ListenChar(2); %turns keyboard output to command window off 'ListenChar(0)' turns it on
KbName('UnifyKeyNames');
InitializePsychSound
repetitions = 1;
%Screen('Preference', 'SkipSyncTests', 1); %messy workaround, timing is prob off, turn 1 to 0 to make screen timing accurtate
Screen('Preference', 'SkipSyncTests', 0); %messy workaround, timing is prob off, turn 1 to 0 to make screen timing accurtate
PsychDefaultSetup(2);
% screens = Screen('Screens'); might want to query OR computer
% screenNumber = 1; %should be 1 for use in OR, 0 for use on home PC
screenNumber = 0;

black = BlackIndex(screenNumber);
white = WhiteIndex(screenNumber);
% grey = white / 2;

pahandle = PsychPortAudio('Open',[],[],0,sound_hellomynameisdaisy_fs, 2);%0 is for no latency
PsychPortAudio('FillBuffer', pahandle, sound_hellomynameisdaisy);
PsychPortAudio('Start', pahandle, repetitions, 0, 1); % Start audio playback for 'repetitions' repetitions of the sound data,start it immediately (0) and wait for the playback to start, return onset timestamp.
%WaitSecs(length(sound_hellomynameisdaisy)/sound_hellomynameisdaisy_fs);
PsychPortAudio('Stop', pahandle, 3); %0 tells fx to stop as soon as convenient (as quickly as possible w/out artifact) but a '3' would mean run until completion and then stop audio playback
PsychPortAudio('Close', pahandle);

rez = Screen('Resolution',screenNumber);
width = (rez.width)/3;
height = (rez.height)/3;
newrect = [0,0,width,height];

[window, ~] = PsychImaging('OpenWindow', screenNumber, white, newrect);
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');
[~, screenYpixels] = Screen('WindowSize', window);
% [xCenter, yCenter] = RectCenter(windowRect);
  
rsp = struct();

% DatapixxAOttl() %FOR TTL 
%LeftArrow = KbName('leftarrow');RighArrow = KbName('rightarrow');UpArrow = KbName('uparrow');
Opening = toc(opening);

%% below starts more active code
for i = 1:length(input_matrix_rndm)
%     DatapixxAOttl() %FOR TTL
    start_loop = tic;
    responsedelay_base = 0.25; %want things clustered around 0.5 seconds for response delay
    startrndm = responsedelay_base*(0.9);
    endrndm = responsedelay_base*(1.1);
    lineup = linspace(startrndm, endrndm);
    lineup_RNDM = lineup(randperm(length(lineup)));
    hatpick = lineup_RNDM(1); %kept this simplified in case there's reason to give responses some type of distribution (gaussian or something)
    responsedelay = hatpick; 
    rsp(i).responsedelay = hatpick;

        if i == 1
        pahandle = PsychPortAudio('Open',[],[],0,sound_whenyouareready_fs, 2);%0 is for no latency
        PsychPortAudio('FillBuffer', pahandle, sound_whenyouareready);
        PsychPortAudio('Start', pahandle, repetitions, 0, 1);
        WaitSecs(length(sound_whenyouareready)/sound_whenyouareready_fs);
        PsychPortAudio('Stop', pahandle, 3); %0 tells fx to stop as soon as convenient (as quickly as possible w/out artifact) but a '3' would mean run until completion and then stop audio playback
        PsychPortAudio('Close', pahandle);
        elseif i ~= 1
        pahandle = PsychPortAudio('Open',[],[],0,sound_next_fs, 2);%0 is for no latency
        PsychPortAudio('FillBuffer', pahandle, sound_next);
        PsychPortAudio('Start', pahandle, repetitions, 0, 1); % Start audio playback for 'repetitions' repetitions of the sound data,start it immediately (0) and wait for the playback to start, return onset timestamp.
        WaitSecs(length(sound_next)/sound_next_fs);
        PsychPortAudio('Stop', pahandle, 3); %0 tells fx to stop as soon as convenient (as quickly as possible w/out artifact) but a '3' would mean run until completion and then stop audio playback
        PsychPortAudio('Close', pahandle);
        end
    

    percentcomplete = floor(100*(i/length(input_matrix_rndm)));
    linea = 'Push up to start.';
    lineb = ([' TIME:  ' num2str(toc(wholetrial)) ' seconds elapsed']); %
    linec = ([' Percent complete:   ' num2str(percentcomplete)]); %
    Screen('TextSize', window, 35);
    DrawFormattedText(window, [linea lineb linec],...
        'center', screenYpixels * 0.25, black);
    Screen('Flip', window)
    
 
%% HERE ADD ARDUINO QUERY: some kind of for loop like:
%while xx = 1;
    %if (arduino for up) == 127; 
        %x = 2;
        %PsychPortAudio('Stop', pahandle);
        %PsychPortAudio('Close', pahandle);
        %WaitSecs(.2)
        %break
    %elseif arduinoforup ~= 127;
        %xx = 1;
        %WaitSecs(0.001)
        %end
        check = 1;
        while check == 1
%             WaitSecs(0.001) %AT commented out on 4/3/18 

            writeread_up1 = tic; %AT added 4/3/18
            write(nC1, 0, 'uint8');
            data = read(nC1, 6, 'uint8');
            writeread_UP1 = toc(writeread_up1); 
            joyYval = int16(data(2)) - int16(joyYoffset);
            if  (joyYval == 127)
                writeread_up2 = tic; %AT added 4/3/18
                write(nC1, 0, 'uint8');
                data = read(nC1, 6, 'uint8');
                writeread_UP2 = toc(writeread_up2); 
                joyYval = int16(data(2)) - int16(joyYoffset);
                if  (joyYval == 127)
                    %                     WaitSecs(0.001)%                 PsychPortAudio('Stop', pahandle);
                    %                 PsychPortAudio('Close', pahandle);
%                     DatapixxAOttl() %FOR TTL
                    break
                end
%             elseif joyYval ~= 127
%                 check = 1;
            end
        end
%% below is fine and all, but prob unnecessary
%     t2wait = 10; %how long before audio prompts them
    % get the time stamp at the start of waiting for key input 
%     tStart = GetSecs;
%     timedout = false;
%     rsptemp.RT = NaN; rsptemp.keyCode = []; rsptemp.keyName = [];
    %WILL NEED TO CHANGE ABOVE FOR CONTROLLER, and below. basically keycode and
    %keyname should be substituted out for whatever axis we use for start
    %position and Kbcheck subbed for 'read'

%         while ~timedout
%          % check if a key is pressed
%         % only keys specified in activeKeys are considered valid
%         [ keyIsDown, keyTime, keyCode ] = KbCheck; 
%           if(keyIsDown)
%           PsychPortAudio('Stop', pahandle);
%           PsychPortAudio('Close', pahandle);
%           WaitSecs(.2);
%           break; 
%           end
%       
%          if( (keyTime - tStart) > t2wait) 
%          pahandle = PsychPortAudio('Open',[],[],0,sound_whenyouareready_fs, 2);%0 is for no latency
%          PsychPortAudio('FillBuffer', pahandle, sound_whenyouareready);
%          PsychPortAudio('Start', pahandle, repetitions, 0, 1);
%          timedout = true; 
%          KbPressWait
%          end
%         end
         % store code for key pressed and reaction time (not saving it out at the
         % moment)
%      if(~timedout)
%          rsptemp.RT      = keyTime - tStart;
%          rsptemp.keyCode = keyCode;
%          rsptemp.keyName = KbName(rsptemp.keyCode);
%       end

%% querying arduino for thumbstick position        
    Start_loop = toc(start_loop);
    hold = tic;
%     DatapixxAOttl() %FOR TTL 

    linea = (['Trial' num2str(i)]);
    lineb = (['\n TIME:  ' num2str(toc(wholetrial)) ' seconds elapsed']); %
    linec = (['\n Percent complete:' num2str(percentcomplete)]); %
    Screen('TextSize', window, 35);
    DrawFormattedText(window, [linea lineb linec],...
    'center', screenYpixels * 0.25, black);
    Screen('Flip', window)
%     DatapixxAOttl() %FOR TTL 
    pahandle = PsychPortAudio('Open',[],[],0, (s(i).fs), 2);%0 is for no latency
    PsychPortAudio('FillBuffer', pahandle, cell2mat(s(i).tones));
    PsychPortAudio('Start', pahandle, repetitions, 0, 1);
    % really, here should be a running check to make sure that there hasn't been a left or right movement for the next 1.5(or so, 1+whatever delay period is) seconds
    stimbeepduration = tic;
%     DatapixxAOttl() %FOR TTL 
    WaitSecs(0.25);   
    PsychPortAudio('Stop', pahandle, 0); %0 tells fx to stop as soon as convenient (as quickly as possible w/out artifact)
    Stimbeepduration = toc(stimbeepduration);
%     DatapixxAOttl() %FOR TTL 

    rsp(i).Stimbeepduration = Stimbeepduration;
    PsychPortAudio('Close', pahandle);
    waitdur_fraction = 10;%how many times during the waitduration do you want to check key status?
        for iii = 1:waitdur_fraction
            
            write(nC1, 0, 'uint8');
            data = read(nC1, 6, 'uint8');
            joyYval = int16(data(2)) - int16(joyYoffset);
             if joyYval ~= 127 % (start position coordinate)
%                  DatapixxAOttl() %FOR TTL 
                     linee = 'Too soon! Wait till after tone.';
                     linee2 = '\n Press any key to continue.';
                     rsp(i).ERROR = 'ERROR';
                     % Draw all the text in one go
                     Screen('TextSize', window, 35);
                      DrawFormattedText(window, [linee linee2],...
                     'center', screenYpixels * 0.25, black);
                      Screen('Flip', window)
                    pahandle = PsychPortAudio('Open',[],[],0,sound_pleasecontinuetoholduntil_fs, 2);%0 is for no latency
                    PsychPortAudio('FillBuffer', pahandle, sound_pleasecontinuetoholduntil);
                    PsychPortAudio('Start', pahandle, repetitions, 0, 1); % Start audio playback for 'repetitions' repetitions of the sound data,start it immediately (0) and wait for the playback to start, return onset timestamp.
                    WaitSecs(length(sound_pleasecontinuetoholduntil)/sound_pleasecontinuetoholduntil_fs);
                    PsychPortAudio('Stop', pahandle, 3); %0 tells fx to stop as soon as convenient (as quickly as possible w/out artifact) but a '3' would mean run until completion and then stop audio playback
                    PsychPortAudio('Close', pahandle);
                    pahandle = PsychPortAudio('Open',[],[],0,gobeep_fs, 2);%0 is for no latency
                    PsychPortAudio('FillBuffer', pahandle, gobeep_sound);
                    PsychPortAudio('Start', pahandle, repetitions, 0, 1); % Start audio playback for 'repetitions' repetitions of the sound data,start it immediately (0) and wait for the playback to start, return onset timestamp.     
                    WaitSecs(0.1)
                    PsychPortAudio('Stop', pahandle, 3); %0 tells fx to stop as soon as convenient (as quickly as possible w/out artifact) but a '3' would mean run until completion and then stop audio playback
                    PsychPortAudio('Close', pahandle);
 
% AT commented out the below on 12/15 because it takes up too much time in
% the OR
%                     pahandle = PsychPortAudio('Open',[],[],0,sound_then_fs, 2);%0 is for no latency
%                     PsychPortAudio('FillBuffer', pahandle, sound_then);
%                     PsychPortAudio('Start', pahandle, repetitions, 0, 1); % Start audio playback for 'repetitions' repetitions of the sound data,start it immediately (0) and wait for the playback to start, return onset timestamp.
%                     WaitSecs(length(sound_then)/sound_then_fs); %this gives audio enough time to play without bumping into the 'Next' audio
%                     PsychPortAudio('Stop', pahandle, 3); %0 tells fx to stop as soon as convenient (as quickly as possible w/out artifact) but a '3' would mean run until completion and then stop audio playback
%                     PsychPortAudio('Close', pahandle);
                    
                    %because we're skipping a bunch of stuff, need to put in values so
                      %struct at ends computes properly (see below)
                      hold_time = toc(hold);
                      posthold = tic;
                      
                     posthold_yonly = tic; %AT added on 4/2/18 in order to keep track of when up position is released
                      pressedKey = 'f';
                      reactionTime = 0;
                      postholdt = toc(posthold);
                      howlong_UP_held = toc(posthold_yonly);

                      postholdt_tillfeedback = tic; %added this on 3/13/18 for case tomorrow so that we are able to figure out when feedback was given to pt. Adding in series with 'writeup' variable beacuse I do not want to mess up any of the internal checks I have going on after this with that as a timepoint
                      writeup = tic;
                      if i == 1
                          rsp(i).Opening = Opening;
                      elseif i ~= 1
                          rsp(i).Opening = 0;
                      end
                 rsp(i).Start_loop = Start_loop;
                 rsp(i).Hold_time = hold_time;
                 rsp(i).Response = pressedKey;
                 rsp(i).Postholdtime = postholdt;
                 rsp(i).actual = 'f'; %f for fail
                 rsp(i).rtime = reactionTime;
                 rsp(i).Postholdtime_UPheld = howlong_UP_held;
                 rsp(i).Writeread_UP1 = writeread_UP1; %AT added the 'Writereads' on 4/3/18
                 rsp(i).Writeread_UP2 = writeread_UP2;
                 writeread_response = 0;
                 rsp(i).Writeread_response = writeread_response;

                 
                 postholdt_tillfeedbackt = toc(postholdt_tillfeedback);
                 rsp(i).timeoffeedback = postholdt_tillfeedbackt;
                 Writeuptime = toc(writeup);
                 rsp(i).Writeuptime = Writeuptime;
%                  Wholetrial = toc(wholetrial);
%                  rsp(i).Wholetrial = Wholetrial;
                  break
             elseif joyYval == 127
%                   DatapixxAOttl() %FOR TTL 


%                   WaitSecs(responsedelay*((iii-iii+1)/waitdur_fraction)) %split up the response delay into parts so we can query in the middle of it as to the position of the participants joystick
                   %so remember that the response delay is going to for
                   %sure be right around 0.25 seconds. so if
                   %waitdur_fraction is 10; then we are sampling position
                   %every 0.025 seconds. I think what we want is sampling
                   %unimpeded, so lets just take it out (AT, 4/2/18)
                   
                  if iii == waitdur_fraction
%                         DatapixxAOttl() %FOR TTL 
                        rsp(i).ERROR = 'GOOD';                       
                        pahandle = PsychPortAudio('Open',[],[],0,gobeep_fs, 2);%0 is for no latency
                        PsychPortAudio('FillBuffer', pahandle, gobeep_sound);
                        PsychPortAudio('Start', pahandle, repetitions, 0, 1); % Start audio playback for 'repetitions' repetitions of the sound data,start it immediately (0) and wait for the playback to start, return onset timestamp.
%                         PsychPortAudio('Stop', pahandle, 3); %0 tells fx to stop as soon as convenient (as quickly as possible w/out artifact) but a '3' would mean run until completion and then stop audio playback
%                         PsychPortAudio('Close', pahandle);
                        startTime = GetSecs(); %GetSecs uses highest precision clock on each OS
                        hold_time = toc(hold);
%                         DatapixxAOttl() %FOR TTL 
                        posthold = tic;
                        posthold_yonly = tic; %AT added on 4/2/18 in order to keep track of when up position is released
%                         DatapixxAOttl() %FOR TTL 
                        check = 1;
                            while check == 1
                                
%                                WaitSecs(0.001) % on 4/2/18, AT is commenting this out
                                writeread_res = tic; %AT added 4/3/18
                                write(nC1, 0, 'uint8');
                                data = read(nC1, 6, 'uint8');
                                writeread_response = toc(writeread_res); 
%                                 ZBut = ~(bitget(data(6),1));
%                                 CBut = ~(bitget(data(6),2));
                                joyXval = int16(data(1)) - int16(joyXoffset);
                                joyYval = int16(data(2)) - int16(joyYoffset);
                                
                                
                                if joyYval == 127 %if the participant is still in the up position
                                    howlong_UP_held = toc(posthold_yonly);
                                    check = 1;
                                elseif joyYval ~= 127
                                   if joyXval == -127
%                                      DatapixxAOttl() %FOR TTL 
                                    pressedKey = 1; %1 is for low/left
                                    pressedSecs = GetSecs();
                                    reactionTime = pressedSecs-startTime;
                                    break
                                   elseif joyXval == 128
%                                      DatapixxAOttl() %FOR TTL 
                                    pressedKey = 2; %2 stands for right/high 
                                    pressedSecs = GetSecs();
                                    reactionTime = pressedSecs-startTime;
                                    break
                                   elseif joyXval ~= -127 || 128
                                    check = 1;
                                   end
                                end
                                end 
   
                        postholdt = toc(posthold);
                        postholdt_tillfeedback = tic; %added this on 3/13/18 for case tomorrow so that we are able to figure out when feedback was given to pt. Adding in series with 'writeup' variable beacuse I do not want to mess up any of the internal checks I have going on after this with that as a timepoint
                        writeup = tic;
                                if i == 1
                                     rsp(i).Opening = Opening;
                                elseif i ~= 1
                                     rsp(i).Opening = 0;
                                end
                            rsp(i).Start_loop = Start_loop;
                        rsp(i).Hold_time = hold_time;
                        rsp(i).Response = pressedKey;
                        rsp(i).Postholdtime = postholdt;
                        rsp(i).actual = s(i).correct;
                        rsp(i).rtime = reactionTime;
                        rsp(i).Postholdtime_UPheld = howlong_UP_held;
                        rsp(i).Writeread_UP1 = writeread_UP1; %AT added the 'Writereads' on 4/3/18
                        rsp(i).Writeread_UP2 = writeread_UP2;
                        rsp(i).Writeread_response = writeread_response;
                        
                            if (s(i).correct == 2 && rsp(i).Response == 2)
                                pahandle = PsychPortAudio('Open',[],[],0,sound_correctbeep_fs, 2);%0 is for no latency
                                PsychPortAudio('FillBuffer', pahandle, sound_correctbeep);
                                PsychPortAudio('Start', pahandle, repetitions, 0, 1); % Start audio playback for 'repetitions' repetitions of the sound data,start it immediately (0) and wait for the playback to start, return onset timestamp.
                                %                                 DatapixxAOttl() %FOR TTL
                                postholdt_tillfeedbackt = toc(postholdt_tillfeedback); %added pm 3/13/18 for next case and all cases going forward so it is easy to tell when feedback was given
                                
                                PsychPortAudio('Stop', pahandle, 3); %0 tells fx to stop as soon as convenient (as quickly as possible w/out artifact) but a '3' would mean run until completion and then stop audio playback
                                PsychPortAudio('Close', pahandle);
                                % keyCode(82) is UpArrow, keyCode(81) is DownArrow, keyCode(24) is u, keyCode(7) is d
                                DrawFormattedText(window, 'Correct', 'center', 'center', black);
                                Screen('Flip', window);
                        clear PsychPortAudio
                            elseif (s(i).correct == 1 && rsp(i).Response == 1)
                                pahandle = PsychPortAudio('Open',[],[],0,sound_correctbeep_fs, 2);%0 is for no latency
                                PsychPortAudio('FillBuffer', pahandle, sound_correctbeep);
                                PsychPortAudio('Start', pahandle, repetitions, 0, 1); % Start audio playback for 'repetitions' repetitions of the sound data,start it immediately (0) and wait for the playback to start, return onset timestamp.
                                %                                   DatapixxAOttl() %FOR TTL
                                postholdt_tillfeedbackt = toc(postholdt_tillfeedback); %added pm 3/13/18 for next case and all cases going forward so it is easy to tell when feedback was given
                                
                                PsychPortAudio('Stop', pahandle, 3); %0 tells fx to stop as soon as convenient (as quickly as possible w/out artifact) but a '3' would mean run until completion and then stop audio playback
                                PsychPortAudio('Close', pahandle);
                                DrawFormattedText(window, 'Correct', 'center', 'center', black);
                                Screen('Flip', window);
                        clear PsychPortAudio
                            else
                                pahandle = PsychPortAudio('Open',[],[],0,sound_incorrectbeep_fs, 2);%0 is for no latency
                                PsychPortAudio('FillBuffer', pahandle, sound_incorrectbeep);
                                PsychPortAudio('Start', pahandle, repetitions, 0, 1); % Start audio playback for 'repetitions' repetitions of the sound data,start it immediately (0) and wait for the playback to start, return onset timestamp.
                                postholdt_tillfeedbackt = toc(postholdt_tillfeedback); %added pm 3/13/18 for next case and all cases going forward so it is easy to tell when feedback was given
                                
                                PsychPortAudio('Stop', pahandle, 3); %0 tells fx to stop as soon as convenient (as quickly as possible w/out artifact) but a '3' would mean run until completion and then stop audio playback
                                PsychPortAudio('Close', pahandle);
                                DrawFormattedText(window, 'Incorrect', 'center', 'center', black);
                                  Screen('Flip', window);
                        clear PsychPortAudio
                            end
                            %                       FlushEvents('keyDown') % clears keyboard queue for Char fx's
                            rsp(i).timeoffeedback = postholdt_tillfeedbackt; %added pm 3/13/18 for next days case and all going forward so we can cue in on when feedback was given

                        Writeuptime = toc(writeup);
                        rsp(i).Writeuptime = Writeuptime;
%                         DatapixxAOttl() %FOR TTL 
                    end
             end
        end
       % Clear the screen
        % sca;
      Wholetrial = toc(wholetrial);
      rsp(i).Wholetrial = Wholetrial;
end
%% RESTART point (correct and incorrect converge here)
%     RestrictKeysForKbCheck([]);
    % final 'report': rsp(i).truetotal % everything
for i = 1:length(rsp)
    if i == 1
        rsp(i).Sumoftictocs = rsp(i).Opening+rsp(i).Start_loop+rsp(i).Hold_time+rsp(i).Postholdtime+rsp(i).Writeuptime;
    elseif i ~= 1
        rsp(i).Sumoftictocs = rsp(i).Start_loop+rsp(i).Hold_time+rsp(i).Postholdtime+rsp(i).Writeuptime;
    end 
end

for i = 1:length(rsp)

    
    a = rsp(length(rsp)).Wholetrial;
    sprintf('%.4f',a);
    b = rsp(i).Opening+rsp(i).Start_loop+rsp(i).Hold_time+rsp(i).Postholdtime+rsp(i).Writeuptime;
    sprintf('%.4f',a);

    if a <= b
        disp ('ERROR, see total calculator');
    else
        disp ('GOOD, total calculator time check');
    end
    
    a = rsp(i).Sumoftictocs;
    sprintf('%.4f',a);
    b = rsp(i).Opening+rsp(i).Start_loop+rsp(i).Hold_time+rsp(i).Postholdtime+rsp(i).Writeuptime;
    sprintf('%.4f',b);

    if a ~= b
        disp (['ERROR, see individual calculator for i = ' num2str(i)]);
    else
        disp (['GOOD, individual calculator for i = ' num2str(i)]);
    end
        
    %rsp(i).Date = datestr(datetime('now','Timezone','local','Format','d-MMM-y HH:mm:ss Z'));
    %above for recent matlab version only
    
    rsp(i).Date = now;
    rsp = renameStructField(rsp,'correct','actual'); % I HAVE NO IDEA WHY THIS IS NECESSARY (field name changes depending on whether high or low pitched cue, if calling low tone ends up as fieldname(correct) but for high tone its (fieldname(actual))
    %STR = renameStructField(STR, OLDFIELDNAME, NEWFIELDNAME)
    
    %changes order of struct fieldnames, imo makes reading output easier
    s = rsp;
    s2 = struct('Date',{'zero'}, 'ERROR', 0,  'Stimbeepduration', 0, 'responsedelay', 0,'Wholetrial', 0,'Sumoftictocs', 0, 'Response', {'zero'},'rtime',0,'actual', {'zero'}, 'Opening', 0,'Start_loop', 0,'Hold_time',0, 'Postholdtime',0, 'Writeuptime',0, 'timeoffeedback', 0, 'Postholdtime_UPheld',0, 'Writeread_UP1', 0, 'Writeread_UP2',0,'Writeread_response',0);
    snew = orderfields(s, s2);
    rsp = snew;
    
    
    
    
    
end
    if exist ('rsp_master_v3.mat', 'file') == 0
        rsp_master_v3 = rsp;
    else
        load('rsp_master_v3');
        rsp_master_v3 = renameStructField(rsp_master_v3,'correct','actual');
        rsp_newmaster_v3 = [rsp_master_v3, rsp];
        clear 'rsp_master_v3'
        rsp_master_v3 = rsp_newmaster_v3;
    end
    
    %following changes order of the structure output fields, will need to
    %adjust if adding more outputs to 'rsp'
    % (sample code:b = 20; c = 10; a = 500;
    %s = struct('b', 20, 'c', 30, 'a', 10);
    %s2 = struct('c', 3, 'a', 1, 'b', 2);
    %snew = orderfields(s, s2);
    
%     
%     s = rsp;
%     s2 = struct('Date',{'zero'}, 'ERROR', 0,  'Stimbeepduration', 0, 'responsedelay', 0,'Wholetrial', 0,'Sumoftictocs', 0, 'Response', {'zero'},'rtime',0,'actual', {'zero'}, 'Opening', 0,'Start_loop', 0,'Hold_time',0, 'Postholdtime',0,'Postholdtime_UPheld',0,'Writeuptime',0, 'timeoffeedback', 0);
%     snew = orderfields(s, s2);
%     rsp = snew;
    save('rsp_master_v3.mat', 'rsp_master_v3')
    
    
    
    
%     DatapixxAOttl() %FOR TTL 
    %ListenChar(0); %turns keyboard output to command window off 'ListenChar(0)' turns it on

    

sca;
end