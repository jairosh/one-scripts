set terminal svg enhanced size 800,800 fname 'Hack' background rgb 'white'

if (!exists("dbfile")) dbfile='/home/jairo/Software/the-one/RESULTADOS/resultados.db'
metric='delivery_prob'
outputf=metric.'.svg'

set output outputf
set ylabel "Proporción de paquetes entregados"
set xlabel "Nodos"
set yrange [0:1]
set xrange [150:550]
set grid y 
set datafile separator "|"
set key above

SQLiteDataSeries(e,m)='< sqlite3 '.dbfile.' "SELECT * FROM stats WHERE experimento=\"'.e.'\" AND nombre_metrica=\"'.m.'\" AND buffer=\"50M\";"'

set style line 1 lt 1 lc rgb "dark-violet" lw 1 dashtype 1
set style line 2 lt 2 lc rgb "green" lw 1 dashtype 1
set style line 3 lt 2 lc rgb "blue" lw 1 dashtype 1
set style line 4 lt 2 lc rgb "red" lw 1 dashtype 1
set style line 5 lt 2 lc rgb "magenta" lw 1 dashtype 1
set style line 6 lt 2 lc rgb "orange" lw 1 dashtype 4
set style line 7 lt 2 lc rgb "purple" lw 1 dashtype 4
set style line 8 lt 2 lc rgb "brown" lw 1 dashtype 4
set style line 9 lt 2 lc rgb "orangered4" lw 1 dashtype 4
set style line 10 lt 2 lc rgb "skyblue" lw 1 dashtype 4
set style line 11 lt 2 lc rgb "forest-green" lw 1 dashtype 4
set style line 12 lt 2 lc rgb "navy" lw 1 dashtype 4
set style line 13 lt 2 lc rgb "royalblue" lw 1 dashtype 4

plot SQLiteDataSeries('MaxPROP',metric) using 7:5 notitle with lines linestyle 3, '' using 7:5:6 title 'MaxPROP' with errorbars linecolor "blue",\
     SQLiteDataSeries('SeeR',metric) using 7:5 notitle with lines linestyle 7, '' using 7:5:6 title 'SeeR' with errorbars linecolor "purple",\
     SQLiteDataSeries('BFGMP-l0.4',metric) using 7:5 notitle with lines linestyle 11, '' using 7:5:6 title 'BFGMP(λ=0.4)' with errorbars linecolor "forest-green",\
     SQLiteDataSeries('BFGMP-lambda',metric) using 7:5 notitle with lines linestyle 1, '' using 7:5:6 title 'BFGMP(λ=0.6)' with errorbars linecolor "dark-violet",\
     SQLiteDataSeries('BFGMP-l0.8',metric) using 7:5 notitle with lines linestyle 11, '' using 7:5:6 title 'BFGMP(λ=0.8)' with errorbars linecolor "forest-green";

     #SQLiteDataSeries('SprayNWait',metric) using 7:5 notitle with lines linestyle 1, '' using 7:5:6 title 'SprayNWait' with errorbars linecolor "dark-violet",\
     #SQLiteDataSeries('Binary-SprayNWait',metric) using 7:5 notitle with lines linestyle 2, '' using 7:5:6 title 'Binary-SprayNWait' with errorbars linecolor "green",\
     #SQLiteDataSeries('Epidemic',metric) using 7:5 notitle with lines linestyle 4, '' using 7:5:6 title 'Epidemic' with errorbars linecolor "red",\
     #SQLiteDataSeries('PRoPHET',metric) using 7:5 notitle with lines linestyle 5, '' using 7:5:6 title 'PRoPHET'  with errorbars linecolor "magenta",\
     #SQLiteDataSeries('PRoPHETV2',metric) using 7:5 notitle with lines linestyle 6, '' using 7:5:6 title 'PRoPHET v2' with errorbars linecolor "orange",\
     #SQLiteDataSeries('BFGMP',metric) using 7:5 notitle with lines linestyle 13, '' using 7:5:6 title 'BFGMP' with errorbars linecolor "royalblue",\
     #SQLiteDataSeries('BFGMP-delta',metric) using 7:5 notitle with lines linestyle 8, '' using 7:5:6 title 'BFGMP-Δ' with errorbars linecolor "brown",\
