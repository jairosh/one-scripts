set terminal svg enhanced size 800,800 fname 'Hack' background rgb 'white'

if (!exists("outputf")) outputf='delivery_prob.svg'
if (!exists("dbfile")) dbfile='resultados.db'
if (!exists("metric")) metric='delivery_prob'

set output outputf
set ylabel "Packet Delivery Ratio"
set yrange [0:1]
set grid y 
set xtics rotate
set datafile separator "|"

plot '< sqlite3 '.dbfile.' "SELECT * FROM stats WHERE nodos=400 AND escenario=\"cdmx\" AND nombre_metrica=\"'.metric.'\";"' using 0:5:xtic(2) notitle with boxes, \
     '' using 0:5:6 notitle with errorbars;

