%V4 on 1/29/20 - 
%V3 as of 1/29/20; works pretty ok, but need to make several formatting
%changes to have it be a prettier display, so creating V4
%V2 on 1/23/20; purpose is to integrate playing a computer or another human
%opponent. Note that for naming convention, player 1 is always going to be
%the patient while player 2 is the opponent


%AT 12/12/19 editting code for our PDilemma purposes

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [taskoutput] = PDil_AT_V3(opponent)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Experimental parameters
clearvars; close all; clc;


mode = 'testrun'; %either testrun or experiment
opponent = 'human'; %either human or computer
taskoutput = struct();


wholesession = tic;
dbstop if error

DisableKeysForKbCheck(40)%this is used for keys that are stuck so that that specific keyboard output is ignored
taskoutput = struct();

txtsize = 20;
y_offset = -150;
% mode = 'experiment';

if strcmp(opponent, 'computer')
    choice_matrix_player1 = zeros(1,10);
    choice_matrix_player2 = {'c';'d';'c';'d';'d';'d';'d';'d';'c';'d'};
elseif strcmp(opponent, 'human')
    choice_matrix_player1 = zeros(1,10);
    choice_matrix_player2 = zeros(1,10);
end

% rand('state', sum(100*clock)); %AT this is no longer recommended
rng('shuffle');% At this is recommended in the ^'s place

ErrorDelay=1; interTrialInterval = .1; nTrialsPerBlock = 10;

KbName('UnifyKeyNames');
Key1=KbName('LeftArrow'); Key2=KbName('RightArrow');
spaceKey = KbName('space'); escKey = KbName('ESCAPE');
cKey = KbName('c');
dKey = KbName('d');

Key_1 = KbName('1!');
Key_2 = KbName('2@');
Key_3 = KbName('3#');
Key_4 = KbName('4$');
Key_5 = KbName('5%');
Key_6 = KbName('6^');
Key_7 = KbName('7&');
Key_8 = KbName('8*');
Key_9 = KbName('9(');

corrkey = [80, 79]; % left and right arrow, %AT; note, this will need to be changed most likely if going between Mac and windows
%can use KbDemo to test out some key names and other timing things

gray = [127 127 127 ]; white = [ 255 255 255]; black = [ 0 0 0];
bgcolor = white; textcolor = black;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Sound feedback
BeepFreq = [800 1300 2000]; BeepDur = [.1 .1 .1];
Beep1 = MakeBeep(BeepFreq(1), BeepDur(1));
Beep2 = MakeBeep(BeepFreq(2), BeepDur(2));
Beep3 = MakeBeep(BeepFreq(3), BeepDur(3));
Beep4 = [Beep1 Beep2 Beep3];


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
ListenChar(1)

Screen('Preference', 'SkipSyncTests', 1);

screens=Screen('Screens');
%     screenNumber=max(screens);
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
% Screen('DrawText',mainwin,['Report the color of the star. Press spacebar to start the experiment.'] ,center(1)-350,center(2)-20,textcolor);


Screen('DrawText',mainwin,('Press spacebar to begin the study.') ,center(1)-350,center(2)-20,textcolor);
Screen('Flip',mainwin );

keyIsDown=0;
while 1
    [keyIsDown, secs, keyCode] = KbCheck;
    if keyIsDown
        if keyCode(spaceKey)
            break ;
        elseif keyCode(escKey)
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
    linea = '  You will be playing against:  ';
    
    if strcmp(opponent, 'computer')
        lineb = ('\n    A computer opponent'); %
    elseif strcmp(opponent, 'human')
        lineb = ('\n    A human opponent'); %
    end
    
    linec = '\n';
    lined = '\n Press spacebar to begin the study.';
    Screen('TextSize', mainwin, txtsize);
    DrawFormattedText(mainwin, [linea  lineb linec lined],...
        center(1)+y_offset,center(2),textcolor);
    
    Screen('Flip', mainwin)
    
    
    
    % %     else
    %         %         blocktype = 'mouse';
    %         %         Screen('DrawText', mainwin, ['Mouse response: left click for red, right click for blue'], center(1)-300, center(2)+130, textcolor);
    %         blocktype = 'keyboard';
    %         Screen('DrawText', mainwin, ['Keyboard response: left arrow for red, right arrow for blue'], center(1)-300, center(2)+130, textcolor);
    %
    % %     end
    
    %     Screen('DrawText', mainwin, ['Click to start'], center(1)-300, center(2)+30, textcolor);
    %     Screen('DrawText', mainwin, ('Spacebar to start'), center(1)-300, center(2)+30, textcolor);
    
    %     Screen('Flip', mainwin);
    %     GetClicks;
    keyIsDown=0;
    while 1
        [keyIsDown, secs, keyCode] = KbCheck;
        if keyIsDown
            if keyCode(spaceKey)
                break ;
            elseif keyCode(escKey)
                ShowCursor;
                fclose(outfile);
                Screen('CloseAll');
                return;
            end
        end
    end
    
    FlushEvents();
    
    WaitSecs(.5);
    
    trialorder = Shuffle(1:nTrialsPerBlock); % randomize trial order for each block
    
    % trial loop
    for i = 1:nTrialsPerBlock
        
        
        %         cellindex = Shuffle(1:nrow.*ncolumn); % randomize the position of the star within the grid specified earlier
        %         itemloc = [cellcenter(cellindex(1),1)-cellsize/2, cellcenter(cellindex(1),2)-cellsize/2, cellcenter(cellindex(1),1)+cellsize/2, cellcenter(cellindex(1),2)+cellsize/2];
        %         Screen('FillRect', mainwin ,bgcolor);
        
        % present the stimulus
        percentcomplete = floor(100*((i-1)/length(choice_matrix_player1)));
        
        
        
        
        
        
        linea = (['Block #: ' mat2str(a) '          Trial #: ' mat2str(i)]);
        lineb = (['\n TIME:  ' num2str(toc(wholesession)) ' seconds elapsed']); %
        linec = (['\n Percent complete:   ' num2str(percentcomplete)]); %
        lined = ('\n Push spacebar to start trial.');
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, [linea lineb linec],...
            center(1)+y_offset,center(2),textcolor);
        Screen('Flip', mainwin)
        keyIsDown = 0;
        while 1
            [keyIsDown, secs, keyCode] = KbCheck;
            if keyIsDown
                if keyCode(spaceKey)
                    break ;
                elseif keyCode(escKey)
                    ShowCursor;
                    fclose(outfile);
                    Screen('CloseAll');
                    return;
                end
            end
        end
        
        FlushEvents();
        
        WaitSecs(.5);
        
        
        
        
        
        
        
        
        linea = ('Player 1: Please provide a keyboard response');
        lineb = ('\n'); %
        linec = ('Press key c for cooperate, or key d for defect'); %
        %         lined = ('\n Push spacebar to start trial.');
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, [linea lineb linec],...
            center(1)+y_offset,center(2),textcolor);
        Screen('Flip', mainwin)
        
        keyIsDown=0;
        rxntime_player1 = tic;
        
        while 1
            [keyIsDown, secs, keyCode] = KbCheck;
            if keyIsDown
                toc_rxntime_player1 = toc(rxntime_player1);
                
                if keyCode(spaceKey)
                    break ;
                elseif keyCode(cKey)
                    player1_response = 'c';
                    break ;
                elseif keyCode(dKey)
                    player1_response = 'd';
                    break ;
                elseif keyCode(escKey)
                    ShowCursor;
                    fclose(outfile);
                    Screen('CloseAll');
                    return;
                end
                
            end
        end
        
        FlushEvents();
        
        WaitSecs(.5);
        
        
        
        
        if strcmp(opponent, 'computer')
            player2_response = choice_matrix_player2(i);
        elseif strcmp(opponent,'human')
            linea = ('Player 2: Please provide a keyboard response');
            lineb = ('\n'); %
            linec = ('Press key c for cooperate, or key d for defect'); %
            %         lined = ('\n Push spacebar to start trial.');
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea lineb linec],...
                center(1)+y_offset,center(2),textcolor);
            Screen('Flip', mainwin)
            
            keyIsDown=0;
            rxntime_player2 = tic;
            while 1
                [keyIsDown, secs, keyCode] = KbCheck;
                if keyIsDown
                    toc_rxntime_player2 = toc(rxntime_player2);
                    
                    if keyCode(spaceKey)
                        break ;
                    elseif keyCode(cKey)
                        player2_response = 'c';
                        break ;
                    elseif keyCode(dKey)
                        player2_response = 'd';
                        break ;
                    elseif keyCode(escKey)
                        ShowCursor;
                        fclose(outfile);
                        Screen('CloseAll');
                        return;
                    end
                end
            end
            
            FlushEvents();
            
            WaitSecs(.5);
        end
        
        
        rxnTime_player1(i) = toc_rxntime_player1;
        if strcmp(opponent, 'human')
            rxnTime_player2(i) = toc_rxntime_player2;
        end
        
        
        
        if strcmp(player2_response, 'c') && strcmp(player1_response,'c') %mod(trialorder(i),2)==0
            %             Screen('DrawTexture', mainwin, redStar, [], itemloc);
            linea = ' Player 1 choice: cooperate';
            lineb = '\n Player 2 choice: cooperate'; %
            linec = '\n Both players receive 4 point'; %
            lined = '\n Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea lineb linec lined],...
                center(1)+y_offset,center(2),textcolor);
            Screen('Flip', mainwin)
            answer=1;
        elseif strcmp(player2_response, 'd') && strcmp(player1_response,'d') %mod(trialorder(i),2)==0
            linea = ' Player 1 choice: defect';
            lineb = '\n Player 2 choice: defect'; %
            linec = '\n Both players receive 2 points'; %
            lined = '\n Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea lineb linec lined],...
                center(1)+y_offset,center(2),textcolor);
            Screen('Flip', mainwin)
            answer=2;
        elseif strcmp(player2_response, 'd') && strcmp(player1_response,'c') %mod(trialorder(i),2)==0
            linea = ' Player 1 choice: cooperate';
            lineb = '\n Player 2 choice: defect'; %
            linec = '\n You receive 1 point; Opponent receives 6 points'; %
            lined = '\n Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea lineb linec lined],...
                center(1)+y_offset,center(2),textcolor);
            Screen('Flip', mainwin)
            answer=3;
        elseif strcmp(player2_response, 'c') && strcmp(player1_response,'d') %mod(trialorder(i),2)==0
            linea = ' Player 1 choice: defect';
            lineb = '\n Player 2 choice: cooperate'; %
            linec = '\n You receive 6 points; Opponent receives 1 point'; %
            lined = '\n Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea lineb linec lined],...
                center(1)+y_offset,center(2),textcolor);
            Screen('Flip', mainwin)
            answer=4;
        end
        
        choice_matrix_player1(i) = player1_response;
        choice_matrix_player2(i) = player2_response;
        
        
        keyIsDown=0;
        while 1
            [keyIsDown, secs, keyCode] = KbCheck;
            if keyIsDown
                if keyCode(spaceKey)
                    break ;
                elseif keyCode(escKey)
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
        
        
        
        %AT 1/25/20 below are probe trials for how trusthworthy player 1
        %thinks player 2 is.
        if i == round(nTrialsPerBlock/2) || i == nTrialsPerBlock
            
            linea = ('Player 1: How fair do you think your opponent is being?');
            lineb = ('\n 1 corresponds to least trustworthy'); %
            linec = ('\n 9 corresponds to most trustworthy'); %
            lined = ('');
            linee = ('\n\n Press a key (1-9) now'); %
            %         lined = ('\n Push spacebar to start trial.');
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea lineb linec lined linee],...
                center(1)+y_offset,center(2),textcolor);
            Screen('Flip', mainwin)
            
            keyIsDown=0;
            proberxntime_player1 = tic;
            
            while 1
                [keyIsDown, secs, keyCode] = KbCheck;
                if keyIsDown
                    toc_rxntime_player1 = toc(proberxntime_player1);
                    
                    
                    
                    
                    
                    
                    if keyCode(spaceKey)
                        break ;
                    elseif keyCode(Key_1)
                        player1_probeResponse = '1';
                        break ;
                    elseif keyCode(Key_2)
                        player1_probeResponse = '2';
                        break ;
                    elseif keyCode(Key_3)
                        player1_probeResponse = '3';
                        break ;
                    elseif keyCode(Key_4)
                        player1_probeResponse = '4';
                        break ;
                    elseif keyCode(Key_5)
                        player1_probeResponse = '5';
                        break ;
                    elseif keyCode(Key_6)
                        player1_probeResponse = '6';
                        break ;
                    elseif keyCode(Key_7)
                        player1_probeResponse = '7';
                        break ;
                    elseif keyCode(Key_8)
                        player1_probeResponse = '8';
                        break ;
                    elseif keyCode(Key_9)
                        player1_probeResponse = '9';
                        break ;
                    elseif keyCode(escKey)
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
                probeResponse(1) = player1_probeResponse;
            elseif i == nTrialsPerBlock
                probeResponse(2) = player1_probeResponse;
            end
            
        end
        
        
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

taskoutput.probeResponse = probeResponse;
ListenChar(0)


end


