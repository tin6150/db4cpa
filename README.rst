
db4cpa
------

Generate a SQLite database for use by Cell Profiler Analyst

Cell Profiler can produce sqlite DB for use by Cell Profiler Analyst.
However, sqlite cannot be written in parallel, thus Cell Profiler run in HPC
is directed to generate MySQL snipplets and CSV instead.

The series of scripts contained here will convert the above into 
a single SQLite DB suitable for use by CPA.



Run instructions:

1. create a folder to contain the SQLite DB 
   This dir will also store new CSV that have been stripped of " 
   (because sqlite import don't have a way to strip them as MySQL does).
2. copy the script in this folder to the dir created in (1)
3. updte setup_cmd.sh with source location of the CSV file
   (don't think any changes is needed in generate_sqlite_load_cmd.sh)
4. Run ./setup_cmd.sh
   (this will call generate_sqlite_load_cmd.sh) 
5. Optional: rm *CSV that is created and placed in this dir.
6. Bring in a .properties for CPA



Overview of scripts and their purposes

check_sqlite_cmd.sh             # run some sanity check against the created SQLite DB
count_csv.sh                    # get count of lines in CSV, compare to output from above
generate_sqlite_load_cmd.sh     # actual import of CSV into DB, called by setup_cmd.sh
load_csv.example.sql            # example load_csv.sql that should be created by generate_sqlite_load_cmd.sh
setup_cmd.sh                    # main script to run to create the DB
sqlite_scheme.ref.sql           # SQL commands to create "reference" DB.  
sqlite_scheme.ref.sql           # This was generated from a previous run of CP that store output into SQLite (non HPC run)
                                # If undertaking the task of running CP in non HPC mode to generate a sqlite DB, 
                                # then using this schema is recommended as it is known to work.  
                                # (Currently, actually using this in setup_cmd.sh

sqlite_scheme.sql               # Generated schema created by setup_cmd.sh.  Untested.
                                # use only when don't have a schema from a previous SQLite output.



Tin
2016.08.05




----

git init
git add README.rst
git commit -a -m "initial commit, creating git repo via cli"
git remote add origin https://tin6150@github.com/tin6150/db4cpa.git
git push -u origin master

# but still need to pre-create the db4cpa repo in github

git push -u origin master

