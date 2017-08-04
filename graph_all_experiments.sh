#!/bin/bash

METRICS=( "dropped" "delivery_prob" "overhead_ratio" "latency_avg"  "latency_med" "hopcount_avg" "hopcount_med" "buffertime_avg" "buffertime_med" )


function usage {
    echo "graph_all_experiments.sh EXPERIMENTS_DIR [TARGET_DIR]"
    echo "    EXPERIMENTS_DIR : Directory containing all subdirectories of each experiment"
    echo "    TARGET_DIR : If specified, the output files will be written to this directory,"
    echo "                 else, it'll be written into EXPERIMENTS_DIR"
}

if [[ "$#" -eq 0 ]]; then
    usage
    exit 1
elif [[ "$#" -eq 1 ]]; then
    EXPERIMENTS_DIR=$1
    TARGET_DIR=$1
elif [[ "$#" -eq 2 ]]; then
    EXPERIMENTS_DIR=$1
    TARGET_DIR=$2
else
    usage
    exit 2
fi


if [[ ! -d "$EXPERIMENTS_DIR" ]] || [[ ! -d "$TARGET_DIR" ]]; then
    usage
    exit 3
fi


for m in "${METRICS[@]}"; do        
    for dir in `find $EXPERIMENTS_DIR -mindepth 1 -type d`; do
        # echo "./get_one_stats.sh $dir $m >> $TARGET_DIR/$m.txt"
        sh -c "./get_one_stats.sh $dir $m >> $TARGET_DIR/$m.txt"
    done

    sort "$TARGET_DIR/$m.txt" -o "$TARGET_DIR/$m.txt"
    sleep 1
    gnuplot -e "filename='$TARGET_DIR/$m.txt'; outputf='$TARGET_DIR/$m.svg'" "GNUPlot/$m.gp"
done



