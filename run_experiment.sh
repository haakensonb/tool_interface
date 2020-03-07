#!/bin/bash

LOGFILE="log2.txt"
PRIVS_PER_ROLE=10

START=10
INC=10
END=100
for ((input_value=$START ; input_value <= $END ; input_value += $INC));
do
    echo "Running experiment with $input_value roles, $PRIVS_PER_ROLE privs per role:" >> $LOGFILE
    for i in {1..3}
    do
       echo "Run number ${i}:" >> $LOGFILE
    #    echo "yes" | python3 manage.py flush
       rm -f db.sqlite3
       python3 manage.py migrate
       python3 experiment.py $input_value $PRIVS_PER_ROLE
    done
    echo "Ending experiment with $input_value roles" >> $LOGFILE
done