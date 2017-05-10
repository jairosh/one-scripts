BEGIN{
    sum=0; 
    media=0; 
    n=0; 
    split("", sample);
    print "#seed, ops(media), ops(std_dev), total_time"
} 

{
    if(match($0, /\[([0-9]+)\]/, arr)){
        seed=arr[1];
    }  
    if(match($0,/([0-9\.]*) 1\/s/, arr)){
        sum+=arr[1]; 
        sample[n]=arr[1]; 
        n+=1;
    }   
    if(match($0,/Simulation done/)){ 
        media=sum/n; 
        temp=0;
        for(i in sample){ 
            temp+=(sample[i]-media)**2;
        } 
        ttime=substr($4, 1, length($4)-1)
        stdev=sqrt(temp/(n-1)); 
        print seed,media,stdev,ttime; 
        sum=0; 
        n=0; 
        media=0; 
        delete sample; 
        stdev=0; 
    }
}