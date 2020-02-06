%V5 2/4/20
%V4 on 1/29/20 -
%V3 as of 1/29/20; works pretty ok, but need to make several formatting
%changes to have it be a prettier display, so creating V4
%V2 on 1/23/20; purpose is to integrate playing a computer or another human
%opponent. Note that for naming convention, Player A is always going to be
%the patient while Player B is the opponent


%AT 12/12/19 editting code for our PDilemma purposes

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [taskoutput] = PDil_AT_V5(opponent)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Experimental parameters
sca; clearvars; close all; clc;

wholesession = tic;

mode = 'testrun'; %either 'testrun' or 'experiment'
opponent = 'human'; %either 'human' or 'computer'
taskoutput = struct();
dbstop if error
PsychDefaultSetup(2);
DisableKeysForKbCheck(40)%this is used for keys that are stuck so that that specific keyboard output is ignored

txtsize = 20;
spacebar_wait = 1;

if strcmp(opponent, 'computer')
    choice_matrix_player1 = zeros(1,10);
    choice_matrix_player2 = {'c';'d';'c';'d';'d';'d';'d';'d';'c';'d'};
elseif strcmp(opponent, 'human')
    choice_matrix_player1 = zeros(1,10);
    choice_matrix_player2 = zeros(1,10);
end

% rand('state', sum(100*clock)); %AT this is no longer recommended
rng('shuffle');% At this is recommended in the ^'s place

ErrorDelay=1;
interTrialInterval = .1;
nTrialsPerBlock = 10;
rxnTime_player1 = zeros(1,nTrialsPerBlock);
rxnTime_player2 = zeros(1,nTrialsPerBlock);
playerA_pts_summary = zeros(1,nTrialsPerBlock);

KbName('UnifyKeyNames');
% Key1=KbName('LeftArrow'); Key_rtArrow=KbName('RightArrow');
Key_spacebar = KbName('space');
Key_esc = KbName('ESCAPE');
Key_c = KbName('c');
Key_d = KbName('d');
Key_1 = KbName('1!');
Key_2 = KbName('2@');
Key_3 = KbName('3#');
Key_4 = KbName('4$');
Key_5 = KbName('5%');
Key_6 = KbName('6^');
Key_7 = KbName('7&');
Key_8 = KbName('8*');
Key_9 = KbName('9(');

% corrkey = [80, 79]; % left and right arrow, %AT; note, this will need to be changed most likely if going between Mac and windows
%can use KbDemo to test out some key names and other timing things

gray = [.5 .5 .5];
white = [1 1 1];
black = [0 0 0];
%below is for red
str_color = '#FF401b';
red = sscanf(str_color(2:end),'%2x%2x%2x',[1 3])/255;
%below is for green
str_color = '#58de49';
green = sscanf(str_color(2:end),'%2x%2x%2x',[1 3])/255;
%below is for blue
str_color = '#009de6';
blue = sscanf(str_color(2:end),'%2x%2x%2x',[1 3])/255;

str_color = '#00BA00';
green2 = sscanf(str_color(2:end),'%2x%2x%2x',[1 3])/255;

str_color = '#FF00AB';
magenta = sscanf(str_color(2:end),'%2x%2x%2x',[1 3])/255;

str_color = '#00B1FF';
blue2 = sscanf(str_color(2:end),'%2x%2x%2x',[1 3])/255;


bgcolor = white;
textcolor_black = black;
textcolor_defect = magenta;
textcolor_cooperate = blue2;
textcolor_keypresses = green2;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% % Sound feedback
% BeepFreq = [800 1300 2000]; BeepDur = [.1 .1 .1];
% Beep1 = MakeBeep(BeepFreq(1), BeepDur(1));
% Beep2 = MakeBeep(BeepFreq(2), BeepDur(2));
% Beep3 = MakeBeep(BeepFreq(3), BeepDur(3));
% Beep4 = [Beep1 Beep2 Beep3];


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Login prompt and open file for writing data out
prompt = {'Outputfile', 'Subject''s number:', 'age', 'gender', 'group', 'Num of Blocks'};
defaults = {'ChoiceRT', '4', '4', '4', '4' , '4'};
answer = inputdlg(prompt, 'ChoiceRT', 2, defaults);
[output, subid, subage, gender, group, nBlocks] = deal(answer{:}); % all input variables are strings
outputname = [output gender subid group subage '.xls'];
nblocks = str2num(nBlocks); % convert string to number for subsequent reference

if exist(outputname)==2 % check to avoid overiding an existing file
    fileproblem = input('That file already exists! Append a .x (1), overwrite (2), or break (3/default)?');
    if isempty(fileproblem) || fileproblem==3
        return;
    elseif fileproblem==1
        outputname = [outputname '.x'];
    end
end
outfile = fopen(outputname,'w'); % open a file for writing data out
fprintf(outfile, 'subid\t subage\t gender\t group\t keyboardOrMouse\t blockNumber\t trialNumber\t redOrBlue\t accuracy\t ReactionTime\t \n');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Screen parameters

Screen('Preference', 'SkipSyncTests', 1);

screens=Screen('Screens');
% screenNumber=max(screens);
screenNumber = 0;

if strcmp(mode, 'testrun')
    rez = Screen('Resolution',screenNumber);
    width = (rez.width)/4;
    height = (rez.height)/4;
    newrect = [0,0,width,height];
    
    [mainwin, screenrect] = PsychImaging('OpenWindow', screenNumber, white, newrect);
    %     Screen('BlendFunction', mainwin, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');
    %     [mainwin, screenrect] = Screen('OpenWindow', window, newrect);
    
elseif strcmp(mode, 'experiment')
    
    % Open window with default settings:
    [mainwin, screenrect] = Screen('OpenWindow', screenNumber);
    
end
% [mainwin, screenrect] = Screen(0, 'OpenWindow');
% Screen('TextFont',mainwin, 'Helvetica');
% Screen('TextSize',mainwin, 14);
% Screen('TextStyle', mainwin, 1+2);
% Screen('FillRect', mainwin, bgcolor);
center = [screenrect(3)/2 screenrect(4)/2];
x_offset = -(center(1)/2);
y_offset = -(center(2)/2);
Screen(mainwin, 'Flip');

% %   load images
% im = imread('redStar.jpg'); redStar = Screen('MakeTexture', mainwin, im);
% im = imread('blueStar.jpg'); blueStar = Screen('MakeTexture', mainwin, im);

% %   potential locations to place the star.
% nrow = 6; ncolumn = 6; cellsize = 100;
% for ncells = 1:nrow.*ncolumn
%     xnum = (mod(ncells-1, ncolumn)+1)-3.5;
%     ynum = ceil(ncells/nrow)-3.5;
%     cellcenter(ncells,1) = center(1)+xnum.*cellsize;
%     cellcenter(ncells,2) = center(2)+ynum.*cellsize;
% end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Experimental instructions, wait for a spacebar response to start
Screen('FillRect', mainwin ,bgcolor);
Screen('TextSize', mainwin, txtsize);



linea = 'Starting task, please remember you can stop at any time.';
lineb = '';
Screen('TextSize', mainwin, txtsize);
DrawFormattedText(mainwin, [linea, lineb],...
    'center',center(2)+y_offset,textcolor_black);
Screen('Flip',mainwin );


WaitSecs(spacebar_wait)

linea = 'Starting task, please remember you can stop at any time.';
lineb = '';
Screen('TextSize', mainwin, txtsize);
DrawFormattedText(mainwin, [linea, lineb],...
    'center',center(2)+y_offset,textcolor_black);

DrawFormattedText(mainwin, '\n\n\n\n Press spacebar to begin the study.',...
    'center',center(2)+y_offset,textcolor_keypresses);

Screen('Flip',mainwin );
FlushEvents();

keyIsDown=0;

while 1
    [keyIsDown, secs, keyCode] = KbCheck;
    if keyIsDown
        if keyCode(Key_spacebar)
            break ;
        elseif keyCode(Key_esc)
            ShowCursor;
            fclose(outfile);
            Screen('CloseAll');
            return;
        end
    end
end

FlushEvents();
WaitSecs(0.5);


linea = 'Below are examples of different colors and their associations.';
Screen('TextSize', mainwin, txtsize);
DrawFormattedText(mainwin, linea,...
    'center',center(2)+y_offset,textcolor_black);
Screen('Flip',mainwin );

WaitSecs(spacebar_wait/2)

Screen('TextSize', mainwin, txtsize);
DrawFormattedText(mainwin, linea,...
    'center',center(2)+y_offset,textcolor_black);
DrawFormattedText(mainwin, '\n\n\n  ''Keypress requested''',...
    'center',center(2)+y_offset,textcolor_keypresses);
DrawFormattedText(mainwin, '\n\n\n\n\n   ''Cooperate''',...
    'center',center(2)+y_offset,textcolor_cooperate);
DrawFormattedText(mainwin, '\n\n\n\n\n\n\n    ''Defect''',...
    'center',center(2)+y_offset,textcolor_defect);

Screen('Flip',mainwin );

WaitSecs(spacebar_wait)

Screen('TextSize', mainwin, txtsize);
DrawFormattedText(mainwin, linea,...
    'center',center(2)+y_offset,textcolor_black);
DrawFormattedText(mainwin, '\n\n\n  ''Keypress requested''',...
    'center',center(2)+y_offset,textcolor_keypresses);
DrawFormattedText(mainwin, '\n\n\n\n\n   ''Cooperate''',...
    'center',center(2)+y_offset,textcolor_cooperate);
DrawFormattedText(mainwin, '\n\n\n\n\n\n\n    ''Defect''',...
    'center',center(2)+y_offset,textcolor_defect);
DrawFormattedText(mainwin, '\n\n\n\n\n\n\n\n\n\n    Press spacebar to continue.',...
    'center',center(2)+y_offset,textcolor_keypresses);

Screen('Flip',mainwin );
FlushEvents();

keyIsDown=0;

while 1
    [keyIsDown, secs, keyCode] = KbCheck;
    if keyIsDown
        if keyCode(Key_spacebar)
            break ;
        elseif keyCode(Key_esc)
            ShowCursor;
            fclose(outfile);
            Screen('CloseAll');
            return;
        end
    end
end

FlushEvents();
WaitSecs(0.5);

% %
% % % counterbalance the order of keyboard and mouse responses for even and odd numbered participants
% % if mod(str2num(subid),2)==0 %AT so this says if the subject ID is an even number, then
% %     firstblock=1;
% % else %AT, if subject ID is NOT an even number, then
% %     firstblock=0;
% % end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Block loop

for a = 1:str2num(nBlocks)
    Screen('FillRect', mainwin, bgcolor);
    %     Screen('TextSize', mainwin, txtsize);
    
    % %     if mod(a,2)==firstblock
    blocktype = 'keyboard';
    %         Screen('DrawText', mainwin, ['Keyboard response: left arrow for red, right arrow for blue'], center(1)-300, center(2)+130, textcolor);
    %     Screen('DrawText', mainwin, ('Keyboard response: \n c for cooperate, d for defect') ,center(1)-300, center(2)+130, textcolor);
    linea = 'Directions:';
    lineb = '\n\n     This is a two-player game (Player A, Player B), the goal of which is for you (Player A) to accumulate as many points as you can over ten trials. For each trial, you (Player A) will choose to either "cooperate" with or "defect" on the other player (Player B). ';
    linec = 'Points are awarded separatedly for each player at the end of each trial. The number of points you receive depends on your choice, as well as the other player''s choice. You will have access to a ''pay-off matrix'' throughout the game, which shows how different combinations of choices are rewarded.';
    lined = 'You will also be able to see the history of past choices you and the other player have made, as well as your point total.';
    %     linef = '\n\n Press spacebar to proceed.';
    
    Screen('TextSize', mainwin, txtsize);
    DrawFormattedText(mainwin, [linea  lineb linec lined],...
        'center',center(2)+y_offset,textcolor_black,...
        80);
    
    Screen('Flip', mainwin)
    
    WaitSecs(spacebar_wait)
    
    linea = 'Directions:';
    lineb = '\n\n     This is a two-player game (Player A, Player B), the goal of which is for you (Player A) to accumulate as many points as you can over ten trials. For each trial, you (Player A) will choose to either "cooperate" with or "defect" on the other player (Player B). ';
    linec = 'Points are awarded separatedly for each player at the end of each trial. The number of points you receive depends on your choice, as well as the other player''s choice. You will have access to a ''pay-off matrix'' throughout the game, which shows how different combinations of choices are rewarded.';
    lined = 'You will also be able to see the history of past choices you and the other player have made, as well as your point total.';
    %     linef = '\n\n Press spacebar to proceed.';
    
    Screen('TextSize', mainwin, txtsize);
    DrawFormattedText(mainwin, [linea  lineb linec lined],...
        'center',center(2)+y_offset,textcolor_black,...
        80);
    DrawFormattedText(mainwin, '\n\n\n\n\n\n\n\n\n\n\n\n Press spacebar to proceed.',...
        'center',center(2)+y_offset,textcolor_keypresses,...
        80);
    
    FlushEvents();
    Screen('Flip', mainwin)
    
    keyIsDown=0;
    while 1
        [keyIsDown, secs, keyCode] = KbCheck;
        if keyIsDown
            if keyCode(Key_spacebar)
                break ;
            elseif keyCode(Key_esc)
                ShowCursor;
                fclose(outfile);
                Screen('CloseAll');
                return;
            end
        end
    end
    
    WaitSecs(.5);
    
    if strcmp(opponent, 'computer')
        linea = 'For this block, "Player B" is a computer.'; %
    elseif strcmp(opponent, 'human')
        linea = 'For this block, "Player B" is another person.'; %
    end
    %     linef = '\n\n Press spacebar to advance.';
    Screen('TextSize', mainwin, txtsize);
    DrawFormattedText(mainwin, linea,...
        'center',center(2)+y_offset,textcolor_black,...
        80);
    
    Screen('Flip', mainwin)
    
    
    FlushEvents();
    WaitSecs(spacebar_wait);
    
    
    if strcmp(opponent, 'computer')
        linea = 'For this block, "Player B" is a computer.'; %
    elseif strcmp(opponent, 'human')
        linea = 'For this block, "Player B" is another person.'; %
    end
    Screen('TextSize', mainwin, txtsize);
    DrawFormattedText(mainwin, linea ,...
        'center',center(2)+y_offset,textcolor_black,...
        80);
    DrawFormattedText(mainwin, '\n\n\n\n Press spacebar to advance.',...
        'center',center(2)+y_offset,textcolor_keypresses,...
        80);
    
    Screen('Flip', mainwin)
    
    keyIsDown=0;
    while 1
        [keyIsDown, secs, keyCode] = KbCheck;
        if keyIsDown
            if keyCode(Key_spacebar)
                break ;
            elseif keyCode(Key_esc)
                ShowCursor;
                fclose(outfile);
                Screen('CloseAll');
                return;
            end
        end
    end
    
    
    FlushEvents();
    WaitSecs(.5);
    
%     trialorder = Shuffle(1:nTrialsPerBlock); % randomize trial order for each block
    
    % trial loop
    for i = 1:nTrialsPerBlock
        
        
        % % %             %Note, for when we want to get fancier and include the wireless
        % % %             %keyboards, see below:
        % % %             %              [keyIsDown, secs, keyCode, deltaSecs] = KbCheck([deviceNumber])
        % % %             % % %             which device are we listening to?
        % % %             % % % use PsychHID('Devices') to list all devices
        % % %             % % %
        % % %             % % % GetKeyboardIndices() will return the device numbers of all keyboard devices
        % % %
        
        linea = (['Your cumulative points: ' mat2str(sum(playerA_pts_summary))]);
        %         linec = (['\n TIME:  ' num2str(round(toc(wholesession))) ' seconds elapsed']); %
        linec = (''); %
        %         lined = ('\n\n Push spacebar to begin a trial.');
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, [linea linec],...
            'center',center(2)+y_offset,textcolor_black);
        
        Screen('Flip', mainwin)
        
        WaitSecs(spacebar_wait);
        
        linea = (['Your cumulative points: ' mat2str(sum(playerA_pts_summary))]);
        %         linec = (['\n TIME:  ' num2str(round(toc(wholesession))) ' seconds elapsed']); %
        linec = (''); %
        lined = (['\n\n\n\n Press spacebar to begin Trial #' mat2str(i) ' out of ' mat2str(nTrialsPerBlock)]);
        
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, [linea linec],...
            'center',center(2)+y_offset,textcolor_black);
        DrawFormattedText(mainwin, lined,...
            'center',center(2)+y_offset,textcolor_keypresses);
        
        
        Screen('Flip', mainwin)
        
        keyIsDown = 1;
        while 1
            [keyIsDown, secs, keyCode] = KbCheck; %keyIsDown returns a '1' if any key has been pressed, secs is time key was pressed
            
            if keyIsDown
                if keyCode(Key_spacebar)
                    break ;
                elseif keyCode(Key_esc)
                    ShowCursor;
                    fclose(outfile);
                    Screen('CloseAll');
                    return;
                end
            end
        end
        
        FlushEvents();
        WaitSecs(.5);
        
        
        linea = ('  Player A: Do you choose to cooperate or defect?');
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, linea,...
            'center', center(2)+y_offset,textcolor_black);
        
        Screen('Flip', mainwin)
        
        WaitSecs(spacebar_wait)
        FlushEvents();
        
        
        
        linea = ('  Player A: Do you choose to cooperate or defect?');
        lineb = ('\n\n'); %
        linec = ('\n   Press the       key for                  , or       key for        '); %
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, linea,...
            'center', center(2)+y_offset,textcolor_black);
        DrawFormattedText(mainwin, [lineb  linec],...
            'center', center(2)+y_offset,textcolor_keypresses);
        linea = ('');
        lineb = ('\n'); %
        linec = ('\n\n                                                  "D"             defect'); %
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, [linea  lineb  linec],...
            center(1)+x_offset, center(2)+y_offset,textcolor_defect);
        
        linea = ('');
        lineb = ('\n'); %
        linec = ('\n\n         "C"             cooperate'); %
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, [linea  lineb  linec],...
            center(1)+x_offset, center(2)+y_offset,textcolor_cooperate);
        
        FlushEvents();
        Screen('Flip', mainwin)
        
        keyIsDown=0;
        rxntime_player1 = tic;
        RestrictKeysForKbCheck([Key_c, Key_d, Key_esc])
        while 1
            [keyIsDown, secs, keyCode] = KbCheck;
            if keyIsDown
                rxnTime_player1(i) = toc(rxntime_player1);
                
                if keyCode(Key_c)
                    player1_response = 'c';
                    break ;
                elseif keyCode(Key_d)
                    player1_response = 'd';
                    break ;
                elseif keyCode(Key_esc)
                    ShowCursor;
                    fclose(outfile);
                    Screen('CloseAll');
                    return;
                end
                
            end
        end
        
        RestrictKeysForKbCheck([])
        FlushEvents();
        WaitSecs(.5);
        
        if strcmp(player1_response, 'd')
            linea = ('Your response: ______');
            
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, linea,...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '                                       Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
            
        elseif strcmp(player1_response, 'c')
            linea = ('Your response: _________');
            
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, linea,...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '                                    Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
        end
        %             lineb = ('\n'); %
        %             linec = ('\n  Press the       key for                 , or       key for       '); %
        
        Screen('Flip', mainwin)
        
        WaitSecs(spacebar_wait)
        
        if strcmp(player1_response, 'd')
            linea = ('Your response: ______');
            lineb = ('\n\n  Player B''s turn, awaiting Player B''s response...');
            
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, '                                       Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
            DrawFormattedText(mainwin, [linea, lineb],...
                'center',center(2)+y_offset,textcolor_black);
            
            
        elseif strcmp(player1_response, 'c')
            linea = ('Your response: _________');
            lineb = ('\n\n  Player B''s turn, awaiting Player B''s response...');
            
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, '                                    Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
            DrawFormattedText(mainwin, [linea, lineb],...
                'center',center(2)+y_offset,textcolor_black);
            
        end
        
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, [linea lineb],...
            'center',center(2)+y_offset,textcolor_black);
        
        Screen('Flip', mainwin)
        
        RestrictKeysForKbCheck([Key_c, Key_d, Key_esc])
        
        if strcmp(opponent, 'computer')
            WaitSecs(2)
            player2_response = choice_matrix_player2(i);
        elseif strcmp(opponent,'human')
            keyIsDown=0;
            rxntime_player2 = tic;
            
            while 1
                [keyIsDown, secs, keyCode] = KbCheck;
                if keyIsDown
                    toc_rxntime_player2 = toc(rxntime_player2);
                    
                    if keyCode(Key_spacebar)
                        break ;
                    elseif keyCode(Key_c)
                        player2_response = 'c';
                        break ;
                    elseif keyCode(Key_d)
                        player2_response = 'd';
                        break ;
                    elseif keyCode(Key_esc)
                        ShowCursor;
                        fclose(outfile);
                        Screen('CloseAll');
                        return;
                    end
                end
            end
            
            FlushEvents();
            RestrictKeysForKbCheck([])
            WaitSecs(.5);
            
        end
        
        if strcmp(opponent, 'human')
            rxnTime_player2(i) = toc_rxntime_player2;
        end
        
        
        linea = 'Player B has made a choice';
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, linea,...
            'center',center(2)+y_offset,textcolor_black);
        
        
        Screen('Flip', mainwin)
        
        WaitSecs(spacebar_wait)
        FlushEvents();
        
        linea = 'Player B has made a choice';
        lineb = '\n\n Press spacebar to see Player B''s choice';
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, linea,...
            'center',center(2)+y_offset,textcolor_black);
        DrawFormattedText(mainwin, lineb,...
            'center',center(2)+y_offset,textcolor_keypresses);
        
        Screen('Flip', mainwin)
        
        
        keyIsDown=0;
        while 1
            [keyIsDown, secs, keyCode] = KbCheck;
            if keyIsDown
                if keyCode(Key_spacebar)
                    break ;
                elseif keyCode(Key_esc)
                    ShowCursor;
                    fclose(outfile);
                    Screen('CloseAll');
                    return;
                end
            end
        end
        
        FlushEvents();
        WaitSecs(0.5);
        
        
        if strcmp(player2_response, 'c')
            
            linea = 'Player B chose to: _________';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, linea,...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '                                       Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
            
        elseif strcmp(player2_response, 'd')
            
            linea = 'Player B chose to: ______';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, linea,...
                'center',center(2)+y_offset,textcolor_black);
            
            DrawFormattedText(mainwin, '                                          Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
        end
        
        
        Screen('Flip', mainwin)
        
        WaitSecs(spacebar_wait)
        FlushEvents();
        
        if strcmp(player2_response, 'c')
            
            linea = 'Player B chose to: _________';
            lineb = '\n\n\n Press spacebar to see summary of trial outcome';
            
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, linea,...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '                                       Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
            DrawFormattedText(mainwin, lineb,...
                'center',center(2)+y_offset,textcolor_keypresses);
            
        elseif strcmp(player2_response, 'd')
            
            linea = 'Player B chose to: ______';
            lineb = '\n\n\n Press spacebar to see summary of trial outcome';
            
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, linea,...
                'center',center(2)+y_offset,textcolor_black);
            
            DrawFormattedText(mainwin, '                                          Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
            DrawFormattedText(mainwin, lineb,...
                'center',center(2)+y_offset,textcolor_keypresses);
        end
        
        
        Screen('Flip', mainwin)
        
        
        keyIsDown=0;
        while 1
            [keyIsDown, secs, keyCode] = KbCheck;
            if keyIsDown
                if keyCode(Key_spacebar)
                    break ;
                elseif keyCode(Key_esc)
                    ShowCursor;
                    fclose(outfile);
                    Screen('CloseAll');
                    return;
                end
            end
        end
        
        FlushEvents();
        WaitSecs(0.5);
        
        
        
        if strcmp(player2_response, 'c') && strcmp(player1_response,'c') %mod(trialorder(i),2)==0
            %             Screen('DrawTexture', mainwin, redStar, [], itemloc);
            linea = '\n\n Your choice: _________';
            lineb = '\n Player B''s choice: _________'; %
            linec = 'You receive 4 points'; %
            lined = '';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linec linea lineb lined],...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '\n\n                                   Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
            DrawFormattedText(mainwin, '\n\n\n                                       Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
            Screen('Flip', mainwin)
            PlayerA_pts = 4;
        elseif strcmp(player2_response, 'd') && strcmp(player1_response,'d') %mod(trialorder(i),2)==0
            linea = '\n\n Your choice: ______';
            lineb = '\n Player B''s choice: ______'; %
            linec = 'You receive 2 points'; %
            lined = '';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linec linea lineb lined],...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '\n\n                                      Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
            DrawFormattedText(mainwin, '\n\n\n                                          Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
            Screen('Flip', mainwin)
            PlayerA_pts = 2;
        elseif strcmp(player2_response, 'd') && strcmp(player1_response,'c') %mod(trialorder(i),2)==0
            linea = '\n\n Your choice: _________';
            lineb = '\n Player B''s choice: ______'; %
            linec = 'You receive 1 point'; %
            lined = '';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linec linea lineb lined],...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '\n\n                                   Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
            DrawFormattedText(mainwin, '\n\n\n                                          Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
            
            Screen('Flip', mainwin)
            PlayerA_pts = 1;
        elseif strcmp(player2_response, 'c') && strcmp(player1_response,'d') %mod(trialorder(i),2)==0
            linea = '\n\n Your choice: ______';
            lineb = '\n Player B''s choice: _________'; %
            linec = 'You receive 6 points'; %
            lined = '';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linec linea lineb lined],...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '\n\n                                      Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
            DrawFormattedText(mainwin, '\n\n\n                                       Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
            Screen('Flip', mainwin)
            PlayerA_pts = 6;
        end
        
        
        WaitSecs(spacebar_wait)
        
        
        if strcmp(player2_response, 'c') && strcmp(player1_response,'c') %mod(trialorder(i),2)==0
            %             Screen('DrawTexture', mainwin, redStar, [], itemloc);
            linea = '\n\n Your choice: _________';
            lineb = '\n Player B''s choice: _________'; %
            linec = 'You receive 4 points'; %
            lined = '\n\n\n\n\n\n\n   Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linec linea lineb ],...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '\n\n                                   Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
            DrawFormattedText(mainwin, '\n\n\n                                       Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
            DrawFormattedText(mainwin, lined,...
                'center',center(2)+y_offset,textcolor_keypresses);
            
            Screen('Flip', mainwin)
            PlayerA_pts = 4;
        elseif strcmp(player2_response, 'd') && strcmp(player1_response,'d') %mod(trialorder(i),2)==0
            linea = '\n\n Your choice: ______';
            lineb = '\n Player B''s choice: ______'; %
            linec = 'You receive 2 points'; %
            lined = '\n\n\n\n\n\n\n Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linec linea lineb],...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '\n\n                                      Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
            DrawFormattedText(mainwin, '\n\n\n                                          Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
            DrawFormattedText(mainwin, lined,...
                'center',center(2)+y_offset,textcolor_keypresses);
            
            Screen('Flip', mainwin)
            PlayerA_pts = 2;
        elseif strcmp(player2_response, 'd') && strcmp(player1_response,'c') %mod(trialorder(i),2)==0
            linea = '\n\n Your choice: _________';
            lineb = '\n Player B''s choice: ______'; %
            linec = 'You receive 1 point'; %
            lined = '\n\n\n\n\n\n\n  Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linec linea lineb ],...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '\n\n                                   Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
            DrawFormattedText(mainwin, '\n\n\n                                          Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
            DrawFormattedText(mainwin, lined,...
                'center',center(2)+y_offset,textcolor_keypresses);
            
            
            Screen('Flip', mainwin)
            PlayerA_pts = 1;
        elseif strcmp(player2_response, 'c') && strcmp(player1_response,'d') %mod(trialorder(i),2)==0
            linea = '\n\n Your choice: ______';
            lineb = '\n Player B''s choice: _________'; %
            linec = 'You receive 6 points'; %
            lined = '\n\n\n\n\n\n\n Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linec linea lineb],...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '\n\n                                      Defect',...
                center(1)+x_offset,center(2)+y_offset,textcolor_defect);
            DrawFormattedText(mainwin, '\n\n\n                                       Cooperate',...
                center(1)+x_offset,center(2)+y_offset,textcolor_cooperate);
            DrawFormattedText(mainwin, lined,...
                'center',center(2)+y_offset,textcolor_keypresses);
            
            Screen('Flip', mainwin)
            PlayerA_pts = 6;
        end
        
        
        choice_matrix_player1(i) = player1_response;
        choice_matrix_player2(i) = player2_response;
        
        
        keyIsDown=0;
        while 1
            [keyIsDown, secs, keyCode] = KbCheck;
            if keyIsDown
                if keyCode(Key_spacebar)
                    break ;
                elseif keyCode(Key_esc)
                    ShowCursor;
                    fclose(outfile);
                    Screen('CloseAll');
                    return;
                end
            end
        end
        
        
        FlushEvents();
        WaitSecs(0.5);
        
        %
        %         % now record  response
        %         timeStart = GetSecs;keyIsDown=0; correct=0; rt=0;
        %
        %         %% keyboard response
        %         while 1
        %             [keyIsDown, secs, keyCode] = KbCheck;
        %             FlushEvents('keyDown');
        %             if keyIsDown
        %                 nKeys = sum(keyCode);
        %                 if nKeys==1
        %                     if keyCode(Key1)||keyCode(Key2)
        %                         rt = 1000.*(GetSecs-timeStart);
        %                         keypressed=find(keyCode);
        %                         Screen('Flip', mainwin);
        %                         break;
        %                     elseif keyCode(escKey)
        %                         ShowCursor; fclose(outfile);  Screen('CloseAll'); return
        %                     end
        %                     keyIsDown=0; keyCode=0;
        %                 end
        %             end
        %         end
        %         if (keypressed==corrkey(1)&&answer==1)||(keypressed==corrkey(2)&&answer==2)
        %             correct=1;Snd('Play', Beep4);
        %         else
        %             correct=0; Snd('Play', Beep1); WaitSecs(ErrorDelay);
        %         end
        %
        %         Screen('FillRect', mainwin ,bgcolor); Screen('Flip', mainwin);
        %
        %         % write data out
        %         fprintf(outfile, '%s\t %s\t %s\t %s\t %s\t %d\t %d\t %d\t %d\t %6.2f\t \n', subid, ...,
        %             subage, gender, group, blocktype, a, i, answer, correct, rt);
        WaitSecs(interTrialInterval);
        
        
        
%Questions to ask at midpoint and at end

        if i == round(nTrialsPerBlock/2) || i == nTrialsPerBlock
            
            if i == round(nTrialsPerBlock/2)
             linea = ('How would you describe your level of cooperation?');
             linea2 = ('\n');

            elseif i == nTrialsPerBlock
             linea = (['You previously rated your level of cooperation as ' mat2str(scaledResponse_PlayerA) '/9, with 1/9 representing ''Very uncooperative'' and 9/9 representing ''Very cooperative'' ']);
             linea2 = ('\n Since then, how would you describe your level of cooperation?');

            end  
                
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea linea2],...
                'center',center(2)+y_offset,textcolor_black,...
                80);
%             DrawFormattedText(mainwin, '\n\n\n\n\n\n Press a key (1-9) now',...
%                 'center',center(2)+y_offset,textcolor_keypresses);
            Screen('Flip', mainwin)
            
            WaitSecs(spacebar_wait/2)
            
            
            lineb = ('\n\n\n 1 corresponds to ''Very uncooperative'''); %
            linec = ('\n\n 5 corresponds to  '' Average level '''); %
            lined = ('\n\n 9 corresponds to ''Very cooperative'''); %

            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea linea2 lineb linec lined],...
                'center',center(2)+y_offset,textcolor_black);
%             DrawFormattedText(mainwin, '\n\n\n\n\n\n Press a key (1-9) now',...
%                 'center',center(2)+y_offset,textcolor_keypresses);
            Screen('Flip', mainwin)
            
            WaitSecs(spacebar_wait)

            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea linea2 lineb linec lined],...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '\n\n\n\n\n\n\n\n\n Press a key (1-9) now',...
                'center',center(2)+y_offset,textcolor_keypresses);
            Screen('Flip', mainwin)
            
            
            keyIsDown=0;
            playerA_probeRrxntime = tic;
            
            while 1
                [keyIsDown, secs, keyCode] = KbCheck;
                if keyIsDown
                    playerA_probeRrxntime = toc(playerA_probeRrxntime);
                    
                    if keyCode(Key_spacebar)
                        break ;
                    elseif keyCode(Key_1)
                        playerA_probeResponse = '1';
                        break ;
                    elseif keyCode(Key_2)
                        playerA_probeResponse = '2';
                        break ;
                    elseif keyCode(Key_3)
                        playerA_probeResponse = '3';
                        break ;
                    elseif keyCode(Key_4)
                        playerA_probeResponse = '4';
                        break ;
                    elseif keyCode(Key_5)
                        playerA_probeResponse = '5';
                        break ;
                    elseif keyCode(Key_6)
                        playerA_probeResponse = '6';
                        break ;
                    elseif keyCode(Key_7)
                        playerA_probeResponse = '7';
                        break ;
                    elseif keyCode(Key_8)
                        playerA_probeResponse = '8';
                        break ;
                    elseif keyCode(Key_9)
                        playerA_probeResponse = '9';
                        break ;
                    elseif keyCode(Key_esc)
                        ShowCursor;
                        fclose(outfile);
                        Screen('CloseAll');
                        return;
                    end
                    
                end
            end
            
            
            FlushEvents();
            
            WaitSecs(.5);
            
            
            if i == round(nTrialsPerBlock/2)
                scaledResponse_PlayerA = playerA_probeResponse;
                probeResponse_playerAcooperativity(1) = scaledResponse_PlayerA;
                probeResponse_playerAcoop_rxntime(1) = playerA_probeRrxntime;
            elseif i == nTrialsPerBlock
                probeResponse_playerAcooperativity(2) = playerA_probeResponse;
                probeResponse_playerAcoop_rxntime(2) = playerA_probeRrxntime;
                
            end
            
        end
        
        
        
        if i == round(nTrialsPerBlock/2) || i == nTrialsPerBlock
            
            if i == round(nTrialsPerBlock/2)
             linea = ('How much do you trust Player B?');
             linea2 = ('\n');

            elseif i == nTrialsPerBlock
             linea = (['You previously rated Player B''s trustworthiness as ' mat2str(scaledResponse_PlayerB) '/9, with 1/9 representing ''Not trust'' and 9/9 representing ''Full trust'' ']);
             linea2 = ('\n Since then, how much do you trust Player B?');

            end  
                
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea linea2],...
                'center',center(2)+y_offset,textcolor_black,...
                80);
%             DrawFormattedText(mainwin, '\n\n\n\n\n\n Press a key (1-9) now',...
%                 'center',center(2)+y_offset,textcolor_keypresses);
            Screen('Flip', mainwin)
            
            WaitSecs(spacebar_wait/2)
            
            
            lineb = ('\n\n\n 1 corresponds to ''No trust'''); %
            linec = ('\n\n 5 corresponds to  ''Average trust '''); %
            lined = ('\n\n 9 corresponds to ''Full trust'''); %

            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea linea2 lineb linec lined],...
                'center',center(2)+y_offset,textcolor_black);
%             DrawFormattedText(mainwin, '\n\n\n\n\n\n Press a key (1-9) now',...
%                 'center',center(2)+y_offset,textcolor_keypresses);
            Screen('Flip', mainwin)
            
            WaitSecs(spacebar_wait)

            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea linea2 lineb linec lined],...
                'center',center(2)+y_offset,textcolor_black);
            DrawFormattedText(mainwin, '\n\n\n\n\n\n\n\n\n Press a key (1-9) now',...
                'center',center(2)+y_offset,textcolor_keypresses);
            Screen('Flip', mainwin)
            
            
            keyIsDown=0;
            playerA_probeRrxntime = tic;
            
            while 1
                [keyIsDown, secs, keyCode] = KbCheck;
                if keyIsDown
                    playerA_probeRrxntime = toc(playerA_probeRrxntime);
                    
                    if keyCode(Key_spacebar)
                        break ;
                    elseif keyCode(Key_1)
                        playerA_probeResponse = '1';
                        break ;
                    elseif keyCode(Key_2)
                        playerA_probeResponse = '2';
                        break ;
                    elseif keyCode(Key_3)
                        playerA_probeResponse = '3';
                        break ;
                    elseif keyCode(Key_4)
                        playerA_probeResponse = '4';
                        break ;
                    elseif keyCode(Key_5)
                        playerA_probeResponse = '5';
                        break ;
                    elseif keyCode(Key_6)
                        playerA_probeResponse = '6';
                        break ;
                    elseif keyCode(Key_7)
                        playerA_probeResponse = '7';
                        break ;
                    elseif keyCode(Key_8)
                        playerA_probeResponse = '8';
                        break ;
                    elseif keyCode(Key_9)
                        playerA_probeResponse = '9';
                        break ;
                    elseif keyCode(Key_esc)
                        ShowCursor;
                        fclose(outfile);
                        Screen('CloseAll');
                        return;
                    end
                    
                end
            end
            
            
            FlushEvents();
            
            WaitSecs(.5);
            
            
            if i == round(nTrialsPerBlock/2)
                scaledResponse_PlayerB = playerA_probeResponse;
                probeResponse_playerBcooperativity(1) = scaledResponse_PlayerB;
                probeResponse_playerBcoop_rxntime(1) = playerA_probeRrxntime;
            elseif i == nTrialsPerBlock
                probeResponse_playerBcooperativity(2) = playerA_probeResponse;
                probeResponse_playerBcoop_rxntime(2) = playerA_probeRrxntime;
                
            end
            
        end
        
        
        
        
        
        
        
        
        playerA_pts_summary(i) = PlayerA_pts;
    end  % end of trial loop
end % end of block loop


Screen('CloseAll');
fclose(outfile);
fprintf('\n\n\n\n\nThis block is now concluded! We appreciate your participation...\n\n');
wholesessionT = toc(wholesession);


%AT 1/23/20; point of taskoutput is to provide struct that stores relevant
%task information
taskoutput.choice_matrix_player1 = choice_matrix_player1;
taskoutput.choice_matrix_player2 = choice_matrix_player2;

taskoutput.rxnTime_player1 = rxnTime_player1;
taskoutput.rxnTime_player2 = rxnTime_player2;

taskoutput.durationWholeSession = wholesessionT;

taskoutput.probeResponse_playerAcoop = probeResponse_playerAcooperativity;
taskoutput.probeResponse_playerAcoop_rxntime = probeResponse_playerAcoop_rxntime;

taskoutput.probeResponse_playerBcoop = probeResponse_playerBcooperativity;
taskoutput.probeResponse_playerBcoop_rxntime = probeResponse_playerBcoop_rxntime;



taskoutput.playerA_pts_summary = playerA_pts_summary;



end


