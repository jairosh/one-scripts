BEGIN{
    split("",times); 
    timesum=0; 
    n=0;
} 
!/^($|#)/{
    timesum+=$4; 
    ops+=$2; 
    times[n]=$4; 
    n+=1;
} 
END{ 
    tss=0; 
    media=timesum/n; 
    for(i in times) 
        tss+=(times[i]-media)**2; 
    stdev=sqrt(tss/(n-1)); 
    print FILENAME,media,stdev; 
}