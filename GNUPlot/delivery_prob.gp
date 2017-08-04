set terminal svg enhanced size 800,800 fname 'Hack' background rgb 'white'

if (!exists("filename")) filename='delivery_prob.txt'
if (!exists("outputf")) outputf='delivery_prob.svg'

set output outputf
set ylabel "Packet Delivery Ratio"
set yrange [0:1]
set grid y 
set xtics rotate

plot filename using 0:3:xtic(1) notitle with boxes, \
     '' using 0:3:4 notitle with errorbars;

