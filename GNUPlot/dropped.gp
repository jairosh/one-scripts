set terminal svg enhanced size 800,800 fname 'Hack' background rgb 'white'

if (!exists("filename")) filename='dropped.txt'
if (!exists("outputf")) outputf='dropped.svg'

set output outputf
set ylabel "Dropped Packets"
set yrange [:]
set grid y 
set xtics rotate

plot filename using 0:3:xtic(1) notitle with boxes, \
     '' using 0:3:4 notitle with errorbars;


