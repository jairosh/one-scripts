#!/bin/bash
BUFFER_SIZE="50M"
NODOS=500
MOBILITY="cdmx"

function usage {
	echo "add_experiment_to_db.sh TARGET_DIR DB_FILE PROTOCOL"
	echo "    Gets the metrics in all MessageStatsReport contained in"
	echo "    TARGET_DIR amd stores the results in DB_FILE."
	echo "    DB_FILE An SQLite 3 database"	
    echo "    PROTOCOL Name of the protocol to process"
}

function createDB() {
	sqlite3 $1 "CREATE TABLE stats (\
    			id             INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,\
			experimento    TEXT     NOT NULL,\
			finalizacion   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\
			nombre_metrica TEXT     NOT NULL,\
			valor_metrica  DOUBLE   NOT NULL,\
			error          DOUBLE,\
			nodos          INTEGER  NOT NULL DEFAULT (0),
			escenario      TEXT     NOT NULL DEFAULT \"cdmx\",
			protocolo      TEXT,
			buffer         STRING);"
        sqlite3 $1 "CREATE INDEX expParam on stats(experimento,nodos,escenario);"
}

if [[ "$#" -eq 0 ]] || [[ "$#" -gt 4 ]]; then
    echo "Incorrect number of arguments ($#)"
    usage    
    exit 1
fi

if [ ! -d $1 ]; then
	echo "Directory doesn't exists."
    usage
    exit 2
fi

if [ ! -f $2 ]; then
	echo "Database file does not exists. Creating an empty one"
    createDB $2
fi

TARGET_DIR=$1
DB_FILE=$2
SCENARIO=`basename $TARGET_DIR`
PROTOCOL=$3

for metric in "created" "dropped" "delivered" "delivery_prob" "overhead_ratio" "latency_avg"  "latency_med" "hopcount_avg" "hopcount_med" "buffertime_avg" "buffertime_med"; do
	VALUES=`./get_one_stats.sh  $TARGET_DIR $metric`	
	M_VAL=`echo $VALUES | cut -d' ' -f 3`
	M_ERR=`echo $VALUES | cut -d' ' -f 4`
        RET=`sqlite3 $DB_FILE "INSERT INTO stats(experimento, nombre_metrica, valor_metrica, error, nodos, escenario, protocolo, buffer) VALUES (\"$SCENARIO\",\"$metric\",$M_VAL,$M_ERR, $NODOS, \"$MOBILITY\", \"$PROTOCOL\", \"$BUFFER_SIZE\");"`
done
