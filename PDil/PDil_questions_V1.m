       %Questions to ask 
       
       queryTime1 = round(nTrialsPerBlock/3);
       queryTime2 = round((nTrialsPerBlock/3)*2);
       queryTime3 = nTrialsPerBlock;
              
        if a == queryTime1 || a == queryTime2 || a == queryTime3
            
            if a == queryTime1
                linea = ('How would you describe your level of cooperation?');
                linea2 = ('\n');
                
            elseif a == queryTime2
                linea = (['You previously rated your level of cooperation as ' mat2str(scaledResponse_PlayerA_query1) ' out of 9 ']);
                linea2 = ('\n Since then, how would you describe your level of cooperation?');
           
            elseif a == queryTime3
                linea = (['You previously rated your level of cooperation as ' mat2str(scaledResponse_PlayerA_query2) ' out of 9 ']);
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
            DrawFormattedText(mainwin, '\n\n\n\n\n\n\n\n\n\n\n Press a key (1-9) now',...
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
            
            
            if a == queryTime1
                scaledResponse_PlayerA_query1 = playerA_probeResponse;
                probeResponse_playerAcooperativity(1) = scaledResponse_PlayerA_query1;
                probeResponse_playerAcoop_rxntime(1) = playerA_probeRrxntime;
          
            elseif a == queryTime2
                scaledResponse_PlayerA_query2 = playerA_probeResponse;
                probeResponse_playerAcooperativity(2) = scaledResponse_PlayerA_query2;
                probeResponse_playerAcoop_rxntime(2) = playerA_probeRrxntime;
          
            elseif a == queryTime3
                probeResponse_playerAcooperativity(3) = playerA_probeResponse;
                probeResponse_playerAcoop_rxntime(3) = playerA_probeRrxntime;
               
            end
            
        end
        
        
        
        if a == round(nTrialsPerBlock/2) || a == nTrialsPerBlock
            
            if a == round(nTrialsPerBlock/2)
                linea = ('How much do you trust Player B?');
                linea2 = ('\n');
                
            elseif a == nTrialsPerBlock
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
            DrawFormattedText(mainwin, '\n\n\n\n\n\n\n\n\n\n\n Press a key (1-9) now',...
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
            
            
            if a == round(nTrialsPerBlock/2)
                scaledResponse_PlayerB = playerA_probeResponse;
                probeResponse_playerBcooperativity(1) = scaledResponse_PlayerB;
                probeResponse_playerBcoop_rxntime(1) = playerA_probeRrxntime;
            elseif a == nTrialsPerBlock
                probeResponse_playerBcooperativity(2) = playerA_probeResponse;
                probeResponse_playerBcoop_rxntime(2) = playerA_probeRrxntime;
                
            end
            
        end