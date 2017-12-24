set terminal svg enhanced size 800,800 fname 'Hack' background rgb 'white'

if (!exists("filename")) filename='latency_med.txt'
if (!exists("outputf")) outputf='latency[med].svg'

set output outputf
set ylabel "Latency (Med.)"
set yrange [:]
set grid y 
set xtics rotate

plot filename using 0:3:xtic(1) notitle with boxes, \
     '' using 0:3:4 notitle with errorbars;

