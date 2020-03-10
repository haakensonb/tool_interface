#!/bin/bash
"""
IMPORTANT
When this filename is changed, the 'LOGFILE' variable in settings.py must
also be changed to the same thing. Due to issues with environment variables
the experiment logfile information must be changed in two places but 
this should be fixed in the future.
"""
EXP_LOGFILE="log4.txt"

PRIVS_PER_ROLE=10
EXP_NUM_FLAG=2

START=10
INC=10
END=100
for ((input_value=${START} ; input_value <= ${END} ; input_value += ${INC}));
do
    echo "Running experiment ${EXP_NUM_FLAG} with ${input_value} roles, ${PRIVS_PER_ROLE} privs per role:" >> "${EXP_LOGFILE}"
    for i in {1..3}
    do
       echo "Run number ${i}:" >> "${EXP_LOGFILE}"
    #    clear the database
       echo "yes" | python3 manage.py flush
       python3 experiment.py "${input_value}" "${PRIVS_PER_ROLE}" "${EXP_NUM_FLAG}"
    done
    echo "Ending experiment with $input_value roles" >> "${EXP_LOGFILE}"
done