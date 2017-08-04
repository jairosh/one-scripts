#!/bin/bash

VALID_METRICS=( "sim_time" "created" "started" "relayed" "aborted" "dropped" "removed" "delivered" "delivery_prob" "response_prob" "overhead_ratio" "latency_avg"  "latency_med" "hopcount_avg" "hopcount_med" "buffertime_avg" "buffertime_med" "rtt_avg" "rtt_med" )

function usage {
	echo "get_one_stats.sh [TARGET_DIR] [METRIC]"
	echo "    Gets the specific METRIC in all MessageStatsReport contained in"
    echo "    TARGET_DIR. At the end the Media and the standard deviation is printed"
	echo "    Possible metrics: "

	for metric in "${VALID_METRICS[@]}" ; do
		echo "        $metric"
	done
}

if [[ "$#" -eq 0 ]] || [[ "$#" -eq 1 ]]; then
    usage
    exit 1
elif [[ "$#" -eq 2 ]]; then
    match=0
    for m in "${VALID_METRICS[@]}"; do
        if [[ $m = "$2" ]]; then
            match=1
            break
        fi
    done
    if [[ $match = 0 ]]; then
        usage
        exit 1
    fi
elif [[ "$#" -eq 3 ]]; then
    match=0
    for m in "${VALID_METRICS[@]}"; do
        if [[ $m = "$2" ]]; then
            match=1
            break
        fi
    done
    if [[ $match = 0 ]]; then
        usage
        exit 1
    fi
else
    usage
    exit 2
fi
  
# echo "Protocol, Nodes, Seed, $2"

VALUES=()
i=0
sum=0
SERIESNAME=''
for f in `find $1 -name "*MessageStatsReport*"` 
do    
    PROTO=`echo $(dirname -- $f) | egrep -o "[^\/]+$"`
    NODESSEED=`echo $f | awk '{if (match($0, /[0-9]+n/)) nodes=substr($0, RSTART, RLENGTH -1); if (match($0, /\[[0-9]+\]/)) seed=substr($0, RSTART+1, RLENGTH-2); print nodes", "seed;}'`
    METRIC_VALUE=`grep "$2" < $f | cut -d' ' -f2`
    if [[ $f == *"BFG"* ]]; then
        SERIE=$(basename $f | sed 's/cdmx-seed\[[0-9]*\]-//g' | cut -d_ -f1)
	if ! [[ "$SERIE" == "$SERIESNAME" ]]; then 
	    SERIESNAME=$SERIE
	fi
    fi

    # echo "$PROTO, $NODESSEED, $METRIC_VALUE"
    if [[ $METRIC_VALUE = "" ]]; then
	   echo "ERROR: No value was found for the metric '$2' in file $f"
	   exit 2
    fi
    VALUES[i]=$METRIC_VALUE
    ((i++))
    sum=`echo "scale=5; $sum + $METRIC_VALUE" | bc`
    # grep "delivery_prob:" < $f | cut -d' ' -f2 | echo ", "$(cat -)'
done

media=`echo "scale=3; $sum/$i" | bc`

sqsum=0
for value in "${VALUES[@]}"; do 
    sqsum=`echo "scale=5; $sqsum + ($value-$media)^2"| bc`    
done

stdev=`echo "scale=5; sqrt($sqsum/($i-1))" | bc`
#echo "scale=5; sqrt($sqsum/($i-1))"
if [[ "$1" == *"BFG"* ]]; then
	echo "$SERIESNAME $2 $media $stdev"
else
	echo "$PROTO $2 $media $stdev"
fi


