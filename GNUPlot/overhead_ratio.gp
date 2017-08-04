set terminal svg enhanced size 800,800 fname 'Hack' background rgb 'white'

if (!exists("filename")) filename='overhead_ratio.txt'
if (!exists("outputf")) outputf='overhead_ratio.svg'

set output outputf
set ylabel "Overhead Ratio"
set yrange [:]
set grid y 
set xtics rotate

plot filename using 0:3:xtic(1) notitle with boxes, \
     '' using 0:3:4 notitle with errorbars;


