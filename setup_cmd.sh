# going forward, need full absolute path of .db, as script change dir in the process of recreating new csv. 
##xx DB_FILE=SQLite_recreated.db
#DB_FILE=/prj/id/bacteriology_hcs/output/09.07.2016-azt-addendum-SQLCSV-expt2/SQLite_recreated.db
DB_FILE=/prj/id/bacteriology_hcs/output/09.07.2016-azt-addendum-SQLCSV-expt2.../SQLite_renum.db


umask 0002

#SCHEMA=sqlite_schema.sql
#SCHEMA_DEF=sqlite_scheme.sql
#SCHEMA_DEF=sqlite_scheme_ext2.sql
SCHEMA_DEF=sqlite_scheme_exp2.sql
# in future, this schema may need special hand crafting...


# if need to create a new db schema from existing db, tweak these lines:
#DBSRC=/prj/id/bacteriology_hcs/output/08.03.2016-CPA_PBP_training_set
#echo ".schema" | sqlite3 $DBSRC/SQLite.db > $SCHEMA_DEF 

# following steap create a new database 
# comment out if appending to existing database
sqlite3 $DB_FILE  < $SCHEMA_DEF 



SRC=./
DST="./csv_recreated"
##DST=/prj/id/bacteriology_hcs/output/08.03.2016-CPA_PBP_training_set_recreated

mkdir $DST

for FF in $( ls $SRC/*CSV ) ; do
        BF=$(basename $FF )
        cat $FF | tr -d '"'  > ${DST}/${BF}
done

##cd $DST

./generate_sqlite_load_cmd.sh > load_csv.sql
mv load_csv.sql $DST
cd $DST
## potentially could move $DB_FILE $DST, but what if reusing other existing DB, don't want to move it
sqlite3 $DB_FILE  < load_csv.sql 


chmod g+rw $DB_FILE

