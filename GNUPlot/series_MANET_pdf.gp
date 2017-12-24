#11in,8.5in
set terminal pdf color enhanced font 'IBM Plex Sans' size 5in,5in

if (!exists("dbfile")) dbfile='/home/jairo/Software/the-one/RESULTADOS/MANET/manet.db'
outputf='MANET.pdf'

set output outputf
set xlabel "Nodos"
set grid y linestyle 1 lw 0.5 dashtype 1 lc "gray"
set datafile separator "|"
set key above

SQLiteDataSeries(e,m)='< sqlite3 '.dbfile.' "SELECT * FROM stats WHERE experimento=\"'.e.'\" AND nombre_metrica=\"'.m.'\" AND buffer=\"50M\" ORDER BY nodos;"'

set ylabel "Proporción de paquetes entregados"
set xrange [150:550]
set yrange [0:1]
plot SQLiteDataSeries('MaxPROP','delivery_prob') using 7:5:6 title 'MaxPROP' with errorlines linestyle 1,\
     SQLiteDataSeries('SeeR','delivery_prob') using 7:5:6 title 'SeeR' with errorlines linestyle 2,\
     SQLiteDataSeries('BFGMP-l0.4','delivery_prob') using 7:5:6 title 'BFGMP(λ=0.4)' with errorlines linestyle 3,\
     SQLiteDataSeries('BFGMP-lambda','delivery_prob') using 7:5:6 title 'BFGMP(λ=0.6)' with errorlines linestyle 4,\
     SQLiteDataSeries('BFGMP-l0.8','delivery_prob') using 7:5:6 title 'BFGMP(λ=0.8)' with errorlines linestyle 5;


set ylabel "Latencia promedio (s)"
set xrange [150:550]
set yrange [*:*]

plot SQLiteDataSeries('MaxPROP','latency_avg') using 7:5:6 title 'MaxPROP' with errorlines linestyle 1,\
     SQLiteDataSeries('SeeR','latency_avg') using 7:5:6 title 'SeeR' with errorlines linestyle 2,\
     SQLiteDataSeries('BFGMP-l0.4','latency_avg') using 7:5:6 title 'BFGMP(λ=0.4)' with errorlines linestyle 3,\
     SQLiteDataSeries('BFGMP-lambda','latency_avg') using 7:5:6 title 'BFGMP(λ=0.6)' with errorlines linestyle 4,\
     SQLiteDataSeries('BFGMP-l0.8','latency_avg') using 7:5:6 title 'BFGMP(λ=0.8)' with errorlines linestyle 5;

     
set ylabel "Sobrecarga (copias creadas/paquetes creados)"
set xrange [150:550]
set yrange [*:*]

plot SQLiteDataSeries('MaxPROP','overhead_ratio') using 7:5:6 title 'MaxPROP' with errorlines linestyle 1,\
     SQLiteDataSeries('SeeR','overhead_ratio') using 7:5:6 title 'SeeR' with errorlines linestyle 2,\
     SQLiteDataSeries('BFGMP-l0.4','overhead_ratio') using 7:5:6 title 'BFGMP(λ=0.4)' with errorlines linestyle 3,\
     SQLiteDataSeries('BFGMP-lambda','overhead_ratio') using 7:5:6 title 'BFGMP(λ=0.6)' with errorlines linestyle 4,\
     SQLiteDataSeries('BFGMP-l0.8','overhead_ratio') using 7:5:6 title 'BFGMP(λ=0.8)' with errorlines linestyle 5;

set ylabel "Saltos promedio (saltos)"
set xrange [150:550]
set yrange [*:*]
plot SQLiteDataSeries('MaxPROP','hopcount_avg') using 7:5:6 title 'MaxPROP' with errorlines linestyle 1,\
     SQLiteDataSeries('SeeR','hopcount_avg') using 7:5:6 title 'SeeR' with errorlines linestyle 2,\
     SQLiteDataSeries('BFGMP-l0.4','hopcount_avg') using 7:5:6 title 'BFGMP(λ=0.4)' with errorlines linestyle 3,\
     SQLiteDataSeries('BFGMP-lambda','hopcount_avg') using 7:5:6 title 'BFGMP(λ=0.6)' with errorlines linestyle 4,\
     SQLiteDataSeries('BFGMP-l0.8','hopcount_avg') using 7:5:6 title 'BFGMP(λ=0.8)' with errorlines linestyle 5;


     #SQLiteDataSeries('SprayNWait',metric) using 7:5 notitle with lines linestyle 1, '' using 7:5:6 title 'SprayNWait' with errorbars linecolor "dark-violet",\
     #SQLiteDataSeries('Binary-SprayNWait',metric) using 7:5 notitle with lines linestyle 2, '' using 7:5:6 title 'Binary-SprayNWait' with errorbars linecolor "green",\
     #SQLiteDataSeries('Epidemic',metric) using 7:5 notitle with lines linestyle 4, '' using 7:5:6 title 'Epidemic' with errorbars linecolor "red",\
     #SQLiteDataSeries('PRoPHET',metric) using 7:5 notitle with lines linestyle 5, '' using 7:5:6 title 'PRoPHET'  with errorbars linecolor "magenta",\
     #SQLiteDataSeries('PRoPHETv2',metric) using 7:5 notitle with lines linestyle 6, '' using 7:5:6 title 'PRoPHET v2' with errorbars linecolor "orange",\
     #SQLiteDataSeries('BFGMP',metric) using 7:5 notitle with lines linestyle 13, '' using 7:5:6 title 'BFGMP' with errorbars linecolor "royalblue",\
     #SQLiteDataSeries('BFGMP-delta',metric) using 7:5 notitle with lines linestyle 8, '' using 7:5:6 title 'BFGMP-Δ' with errorbars linecolor "brown",\
     

     #SQLiteDataSeries('zT[0.25]-dT[600]',metric) using 7:5 notitle with lines linestyle 10, '' using 7:5:6 title 'zT[0.25]-dT[600]' with errorbars linecolor "skyblue",\
     #SQLiteDataSeries('zT[0.5]-dT[600]',metric) using 7:5 notitle with lines linestyle 11, '' using 7:5:6 title 'zT[0.5]-dT[600]' with errorbars linecolor "forest-green",\
     #SQLiteDataSeries('zT[0.75]-dT[600]',metric) using 7:5 notitle with lines linestyle 12, '' using 7:5:6 title 'zT[0.75]-dT[600]' with errorbars linecolor "navy",\
