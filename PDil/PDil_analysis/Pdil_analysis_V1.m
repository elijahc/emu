% AT creating 6/21/20, goal is to generate some epoch timings





    for aa = 5
        timeTillStartQueries = taskoutput.timing.Time_scrn_flip_trials1(aa, 2)+taskoutput.timing.Time_scrn_flip_trials2(aa, 2)+taskoutput.timing.Time_scrn_flip_trials3(aa, 2)+taskoutput.timing.Time_scrn_flip_trials4(aa, 2)+taskoutput.timing.Time_scrn_flip_trials5(aa, 2)+taskoutput.timing.Time_postscrn_flip_trials1(aa,1)+taskoutput.timing.Time_postscrn_flip_trials2(aa,1)+taskoutput.timing.Time_postscrn_flip_trials3(aa,1)+taskoutput.timing.Time_postscrn_flip_trials4(aa,1)+taskoutput.timing.Time_postscrn_flip_trials5(aa,1);
    end
    
    
    
    timeTillEndQuery1 = taskoutput.timing.Time_query1(1) + taskoutput.timing.Time_query1_rxntime(1) + taskoutput.timing.Time_query1_Postrxntime(1);
    
    
    timeTillEndQuery2 = taskoutput.timing.Time_query2(1) + taskoutput.timing.Time_query2_rxntime(1) + taskoutput.timing.Time_query2_Postrxntime(1);
    
    
    sumforexample = timeTillStartQueries+timeTillEndQuery1+timeTillEndQuery2;
    
    
    %6/21/20 so the above is giving us the start and stop times for when
    %query1 and query2 are posed, following the 5th trial.
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
%         timing_sumTictocs_trial_n(queryTime1,1) = timing_sumTictocs_trial_n(queryTime1,1)+Time_query1(1)+Time_query1_rxntime(1)+Time_query1_Postrxntime(1)+Time_query2(1)+Time_query2_rxntime(1)+Time_query2_Postrxntime(1);
%     timing_sumTictocs_trial_n(queryTime2,1) = timing_sumTictocs_trial_n(queryTime2,1)+Time_query1(2)+Time_query1_rxntime(2)+Time_query1_Postrxntime(2)+Time_query2(2)+Time_query2_rxntime(2)+Time_query2_Postrxntime(2);
%     timing_sumTictocs_trial_n(queryTime3,1) = timing_sumTictocs_trial_n(queryTime3,1)+Time_query1(3)+Time_query1_rxntime(3)+Time_query1_Postrxntime(3)+Time_query2(3)+Time_query2_rxntime(3)+Time_query2_Postrxntime(3) + endScreen;
%     
%    