%V2 on 1/23/20; purpose is to integrate playing a computer or another human
%opponent



%AT 12/12/19 editting code for our PDilemma purposes

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   ChoiceRT.m   YVJ     Feb 18, 2009 Revised Feb 27, 2016
%   This program displays a red or a blue star for participants to make a
%   choice response. In some blocks they click the left or right side of
%   the mouse in response to the color of the star. In other blocks they
%   press the left or right arrow keys. There are 10 trials per block
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Experimental parameters
clearvars

wholesession = tic;


dbstop if error

close all
clc
DisableKeysForKbCheck(40)
mode = 'testrun';
task_output = struct();

txtsize = 20;
y_offset = -150;
% mode = 'experiment';
input_matrix = {'c';'d';'c';'d';'d';'d';'d';'d';'c';'d'};

% rand('state', sum(100*clock)); %AT this is no longer recommended
rng('shuffle');% At this is recommended in the ^'s place
 
ErrorDelay=1; interTrialInterval = .1; nTrialsPerBlock = 10;

KbName('UnifyKeyNames');
Key1=KbName('LeftArrow'); Key2=KbName('RightArrow');
spaceKey = KbName('space'); escKey = KbName('ESCAPE');
cKey = KbName('c');
dKey = KbName('d');
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

%   load images
im = imread('redStar.jpg'); redStar = Screen('MakeTexture', mainwin, im);
im = imread('blueStar.jpg'); blueStar = Screen('MakeTexture', mainwin, im);

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
    lineb = ('\n    A computer opponent'); %
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
        opponentResponse = input_matrix(i);
        
        %         cellindex = Shuffle(1:nrow.*ncolumn); % randomize the position of the star within the grid specified earlier
        %         itemloc = [cellcenter(cellindex(1),1)-cellsize/2, cellcenter(cellindex(1),2)-cellsize/2, cellcenter(cellindex(1),1)+cellsize/2, cellcenter(cellindex(1),2)+cellsize/2];
        %         Screen('FillRect', mainwin ,bgcolor);
        
        % present the stimulus
        percentcomplete = floor(100*((i-1)/length(input_matrix)));
        
        
        
        
        
        
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
        
        
        
        
        
        
        
        
        linea = ('Please provide a keyboard response:');
        lineb = ('\n'); %
        linec = ('Press key c for cooperate, or key d for defect'); %
        %         lined = ('\n Push spacebar to start trial.');
        Screen('TextSize', mainwin, txtsize);
        DrawFormattedText(mainwin, [linea lineb linec],...
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
        
        keyIsDown=0;
        while 1
            [keyIsDown, secs, keyCode] = KbCheck;
            if keyIsDown
                if keyCode(spaceKey)
                    break ;
                elseif keyCode(cKey)
                    participantResponse = 'c';
                    break ;
                elseif keyCode(dKey)
                    participantResponse = 'd';
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
        
        
        if strcmp(opponentResponse, 'c') && strcmp(participantResponse,'c') %mod(trialorder(i),2)==0
            %             Screen('DrawTexture', mainwin, redStar, [], itemloc);
            linea = ' Your choice: cooperate';
            lineb = '\n Other player: cooperate'; %
            linec = '\n Both players receive 4 point'; %
            lined = '\n Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea lineb linec lined],...
                center(1)+y_offset,center(2),textcolor);
            Screen('Flip', mainwin)
            answer=1;
        elseif strcmp(opponentResponse, 'd') && strcmp(participantResponse,'d') %mod(trialorder(i),2)==0
            linea = ' Your choice: defect';
            lineb = '\n Other player: defect'; %
            linec = '\n Both players receive 2 points'; %
            lined = '\n Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea lineb linec lined],...
                center(1)+y_offset,center(2),textcolor);
            Screen('Flip', mainwin)
            answer=2;
        elseif strcmp(opponentResponse, 'd') && strcmp(participantResponse,'c') %mod(trialorder(i),2)==0
            linea = ' Your choice: cooperate';
            lineb = '\n Other player: defect'; %
            linec = '\n You receive 1 point; Opponent receives 6 points'; %
            lined = '\n Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea lineb linec lined],...
                center(1)+y_offset,center(2),textcolor);
            Screen('Flip', mainwin)
            answer=3;
        elseif strcmp(opponentResponse, 'c') && strcmp(participantResponse,'d') %mod(trialorder(i),2)==0
            linea = ' Your choice: defect';
            lineb = '\n Other player: cooperate'; %
            linec = '\n You receive 6 points; Opponent receives 1 point'; %
            lined = '\n Press spacebar to proceed';
            Screen('TextSize', mainwin, txtsize);
            DrawFormattedText(mainwin, [linea lineb linec lined],...
                center(1)+y_offset,center(2),textcolor);
            Screen('Flip', mainwin)
            answer=4;
        end
        
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
    end  % end of trial loop
end % end of block loop

Screen('CloseAll');
fclose(outfile);
fprintf('\n\n\n\n\nFINISHED this part! PLEASE GET THE EXPERIMENTER...\n\n');



