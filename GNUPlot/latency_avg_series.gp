set terminal svg enhanced size 800,800 fname 'Hack' background rgb 'white'

if (!exists("dbfile")) dbfile='/home/jairo/Software/the-one/RESULTADOS/resultados.db'
metric='latency_avg'
outputf=metric.'.svg'

set output outputf
set ylabel "Latencia promedio (s)"
set xlabel "Nodos"
set xrange [150:550]
set grid y 
set datafile separator "|"
set key above

SQLiteDataSeries(e,m)='< sqlite3 '.dbfile.' "SELECT * FROM stats WHERE experimento=\"'.e.'\" AND nombre_metrica=\"'.m.'\";"'


plot SQLiteDataSeries('SprayNWait',metric) using 7:5 notitle with lines linecolor 1, '' using 7:5:6 title 'SprayNWait' with errorbars linecolor 1,\
     SQLiteDataSeries('Binary-SprayNWait',metric) using 7:5 notitle with lines linecolor 2, '' using 7:5:6 title 'Binary-SprayNWait' with errorbars linecolor 2,\
     SQLiteDataSeries('MaxPROP',metric) using 7:5 notitle with lines linecolor 3, '' using 7:5:6 title 'MaxPROP' with errorbars linecolor 3,\
     SQLiteDataSeries('Epidemic',metric) using 7:5 notitle with lines linecolor 4, '' using 7:5:6 title 'Epidemic' with errorbars linecolor 4,\
     SQLiteDataSeries('PRoPHET',metric) using 7:5 notitle with lines linecolor 5, '' using 7:5:6 title 'PRoPHET'  with errorbars linecolor 5,\
     SQLiteDataSeries('PRoPHETV2',metric) using 7:5 notitle with lines linecolor 6, '' using 7:5:6 title 'PRoPHET v2' with errorbars linecolor 6,\
     SQLiteDataSeries('s[6]-zT[0.5]-ic[8]-FIFO',metric) using 7:5 notitle with lines linecolor 7, '' using 7:5:6 title 's[6]-zT[0.5]-ic[8]-FIFO' with errorbars linecolor 7;

