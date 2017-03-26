#!/bin/bash

## generate_sqlite_load_cmd.sh > load_csv.sql
## sqlite3 SQLite_tin.db < load_csv.sql

CASA=`pwd`
#SRC='/prj/id/bacteriology_hcs/output/07.14.2016_mini_SQL_output'
#SRC='/prj/id/bacteriology_hcs/output/07.29.2016-CPA_test'
#SRC='/prj/id/bacteriology_hcs/output/07.29.2016-CPA_test_recreated'
SRC='./'
TAB_PREFIX="exp1"


#echo ".mode list"
echo ".mode csv"
echo ".separator ,"
echo "pragma temp_store = 2;"



for F in $(ls  $SRC/SQL_*_Membranes.CSV ); do
        echo ".import $F ${TAB_PREFIX}Per_Membranes"
done

for F in $(ls  $SRC/SQL_*_Nucleoids.CSV ); do
        echo ".import $F ${TAB_PREFIX}Per_Nucleoids"
done

for F in $(ls  $SRC/SQL_*_Relationships.CSV ); do
        echo ".import $F ${TAB_PREFIX}Per_Relationships"
done

for F in $(ls  $SRC/SQL_*_Whole_Cell_Mask.CSV ); do
        echo ".import $F ${TAB_PREFIX}Per_Whole_Cell_Mask"
done


# this one has complain that there isn't enough number of fields...
for F in $(ls  $SRC/SQL_*_Image.CSV ); do
        echo ".import $F ${TAB_PREFIX}Per_Image"
done


        # orig mysql load has more complex handling directives:
        #echo "LOAD DATA LOCAL INFILE '$F' REPLACE INTO TABLE ${TAB_PREFIX}Per_Image       FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\\\\';"
