
% Clear the workspace and the screen
sca;
close all;
clearvars;


str_color = '#58de49';
green = sscanf(str_color(2:end),'%2x%2x%2x',[1 3])/255;




% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');

% Draw to the external screen if avaliable
screenNumber = max(screens);

% Define black and white
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);


rez = Screen('Resolution',screenNumber);
width = (rez.width)/4;
height = (rez.height)/4;
newrect = [0,0,width,height];

[mainwin, screenrect] = PsychImaging('OpenWindow', screenNumber, white, newrect);

[screenXpixels, screenYpixels] = Screen('WindowSize', mainwin);













str_color = '#58de49';
green = sscanf(str_color(2:end),'%2x%2x%2x',[1 3])/255;

% Set blend function for alpha blending
Screen('BlendFunction', mainwin, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(screenrect);

% Make a base Rect of 400 by 400 pixels
baseRect = [0 0 width/15 width/15];

% Screen X positions of our nine rectangles
for ii = 1:9
    squareXpos(ii) = ((width/15)+(width/30))+((width/15)*(ii-1))*1.5;
    squareYpos(ii) = (height*(2/3));
end
    numSqaures = length(squareXpos);
    

% % Screen X positions of our three rectangles
% squareXpos = [xCenter - 200 xCenter + 200 xCenter];
% squareYpos = [yCenter yCenter yCenter + 200];
% numSqaures = length(squareXpos);

% Set the colors to Red, Green and Blue, with the fourth value being the
% "alpha" value. This also takes a value between 0 and 1 just like a
% normal colour, however now 0 = totally transparent and 1 = totally
% opaque. Our RGB triplets are now RGBA values.
% allColors = [1 0 0 1; 0 1 0 1; 0 0 1 0.5]';

green = [green, .25];

% Make our rectangle coordinates
allRects = nan(4, numSqaures);
for i = 1:numSqaures
    allRects(:, i) = CenterRectOnPointd(baseRect,...
        squareXpos(i), squareYpos(i));
end

% Draw the rect to the screen
Screen('FillRect', mainwin, green, allRects);
numbs = [1,2,3,4,5,6,7,8,9];
linea = (mat2str(numbs));
lineb = '';
Screen('TextSize', mainwin, 20);
for kk = 1:numSqaures
    linea = (mat2str(numbs(kk)));
    
    DrawFormattedText(mainwin, linea,...
        squareXpos(kk), squareYpos(kk), [0 0 0]);
end

for kk = 1
    linea = 'Very Uncooperative';
    
    DrawFormattedText(mainwin, linea,...
        'left', squareYpos(kk)+(squareYpos(kk)/4), [0 0 0]);
end
for kk = 9
    linea = 'Cooperative';
    
    DrawFormattedText(mainwin, linea,...
        'right', squareYpos(kk)+(squareYpos(kk)/4), [0 0 0]);
end

% Flip to the screen
Screen('Flip', mainwin);

% Wait for a key press
KbStrokeWait;

% Clear the screen
sca;