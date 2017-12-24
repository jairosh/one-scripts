set terminal svg enhanced size 800,800 fname 'Hack' background rgb 'white'

if (!exists("filename")) filename='buffertime_avg.txt'
if (!exists("outputf")) outputf='buffertime[avg].svg'

set output outputf
set ylabel "Buffertime (Avg.)"
set yrange [:]
set grid y 
set xtics rotate

plot filename using 0:3:xtic(1) notitle with boxes, \
     '' using 0:3:4 notitle with errorbars;


