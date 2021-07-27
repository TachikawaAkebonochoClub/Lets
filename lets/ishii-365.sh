#!/bin/bash

CMD=$(cd $(dirname $0); pwd)/storage_battery.py
#CMD="echo $CMD"
NUM=365
START=$(date "+%Y-%m-%d" )
CSV="./data.csv"

usage (){
    cat <<EOF
Usage: $(basename $CMD)  [OPTION]
execute $(basename $CMD) at 1 year.


  -d date     day of start.(default: today)
  -l list     list file(default: $CSV)
  -n          number of days(default: $NUM)
  -h          display this help and exit

Examples:
   $(basename $CMD) -d 2020-04-01 -l ./data.csv -n 10
    
EOF
}

while getopts "d:n:l:h" OPT
do
  case $OPT in
    h) usage; exit 0;;
    d) START=$OPTARG;;
    l) CSV=$OPTARG;;
    n) NUM=$OPTARG;;
    \?) echo "[ERROR] Undefined options.";;
  esac
done

start=$( date "+%s" -d $START )
for a  in $( seq  0 $(( $NUM -1)) )
do
    sec=$(( $a * 60 * 60 * 24 + $start))
    $CMD $( date -d "@$sec" "+%Y-%m-%d" ) $CSV
done
