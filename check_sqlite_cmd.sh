#!/bin/bash

## bash check_sqlite_cmd.sh   

#CASA=`pwd`
#SRC="/mnt/fusion1/fengbr2/db4cpa/07.14.2016_mini_SQL_output__eg"
#SRC='/prj/id/bacteriology_hcs/output/07.14.2016_mini_SQL_output'
#SRC='/prj/id/bacteriology_hcs/output/07.29.2016-CPA_test'
#SRC='/prj/id/bacteriology_hcs/output/07.29.2016-CPA_test_recreated'
#SRC='./'
TAB_PREFIX="exp1"

DB=SQLite_recreated.db


#echo ".mode list"
#echo ".mode csv"
#echo ".separator ,"
#echo "pragma temp_store = 2;"


#CMD="cat - -"
CMD="wc -l"

echo "SELECT * FROM ${TAB_PREFIX}Per_Membranes;"        | sqlite3 $DB| $CMD
echo "SELECT * FROM ${TAB_PREFIX}Per_Nucleoids;"        | sqlite3 $DB| $CMD
echo "SELECT * FROM ${TAB_PREFIX}Per_Relationships;"    | sqlite3 $DB| $CMD
echo "SELECT * FROM ${TAB_PREFIX}Per_Whole_Cell_Mask;"  | sqlite3 $DB| $CMD
echo "SELECT * FROM ${TAB_PREFIX}Per_Image;"            | sqlite3 $DB| $CMD


exit 007

echo "SELECT COUNT(*) FROM ${TAB_PREFIX}Per_Membranes;"        | sqlite3 $DB
echo "SELECT COUNT(*) FROM ${TAB_PREFIX}Per_Nucleoids;"        | sqlite3 $DB
echo "SELECT COUNT(*) FROM ${TAB_PREFIX}Per_Relationships;"    | sqlite3 $DB
echo "SELECT COUNT(*) FROM ${TAB_PREFIX}Per_Whole_Cell_Mask;"  | sqlite3 $DB
echo "SELECT COUNT(*) FROM ${TAB_PREFIX}Per_Image;"            | sqlite3 $DB

