#!/bin/env python
##  #!/db/idinfo/prog/local_python_2.7.9/bin/python
## /usr/prog/python/2.7.9-goolf-1.5.14-NX/bin/python    # started using in v .6 (2016.0304)
## #!/usr/prog/python/3.4.2-goolf-1.5.14-NX/bin/python  # used till v .5.1

# this script will update the image id in the csv file so that they can be 
# imported into existing Cell Profiler sqlite db w/o causing primary key violation
# specifically, a YYMMDD date prefix will be added to the image number. 
# eg image 65 will become 65140916 (former prefix would make it 1609140065, but that doesn't hash/partition well)
# 
# example run: 
# ./renum_csv.py
#    it will look for all csv file, figure what kind of file it is and change the columns accordingly.
# need python 2.7 or so

# adopted from taxorpt.py 
# Tin 2016.0914



from __future__ import print_function
#http://stackoverflow.com/questions/12592544/typeerror-expected-a-character-buffer-object
import argparse 
import os
import sys
import time             # for --prefix setting by  time.strftime
import datetime         # printing start and end time, nothing with image number prefix with YYMMDD date stamp
import errno            # mkdir dir already exist exception catching
import glob             # for listing files in dir matching certain pattern
import re               # regular expression matching in processLine



dbgLevel = 0            # global var, set via cli -dddd flag
def dbg( level, strg ):
        if( dbgLevel >= level ) :
                print( "<!--dbg%s: %s-->" % (level, strg) )


def process_cli() :
        # https://docs.python.org/2/howto/argparse.html#id1
        parser = argparse.ArgumentParser( description='This script update image number in CSV with YYMMDD prefix')
        parser.add_argument('-s', '--separator', '--ifs', dest='IFS',  help="the column separator character (defualt COMMA)",      default=',' ) 
        parser.add_argument('-p', '--prefix',  help="DDMMYY SUFFIX to append to image number (default today's date)", default="", required=False ) 
        parser.add_argument('-i', '--indir',  help="name of input dir where SOURCE csv files can be found (default . [other dir UNTESTED])",  default=".", required=False ) 
        parser.add_argument('-o', '--outdir',  help="name of output dir to store result (default csv_renum)",  default="csv_renum", required=False ) 
        parser.add_argument('-d', '--debuglevel', help="Debug mode. Up to -ddd useful for troubleshooting input file parsing. -ddddd intended for coder. ", action="count", default=0)
        parser.add_argument('--version', action='version', version='%(prog)s 0.1  For help, email tin.ho@novartis.com')
        args = parser.parse_args()
        global dbgLevel 
        dbgLevel = args.debuglevel
        if args.prefix == '' or args.prefix == ' ' :
                #args.prefix = time.strftime("%y%m%d")
                args.prefix = time.strftime("%d%m%y")
        return args
# end process_cli() 




def prerun_setup( args ) :
        start_time = datetime.datetime.now()
        dbg( 1, "csv image renumbering starting at %s" % start_time )
        dbg( 1, "renum suffix is %s" % args.prefix )
        try:
                os.makedirs( args.outdir )
        except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(args.outdir):
                        pass
                else:
                        raise
# end prerun_setup procedure




# this function takes one input line
# massage it and return it back
# image number is expected at col index 1 and possibly col index 2 
# (use -1 if not don't want to change image number in colidx 2)
# (use -1, -1 ie twice if only wants to strip quotes)
# renum_prefix expected to be a string of form YYMMDD, eg 160904
# totCol  is for  total number of column, for sanity check of processed line, 
#         for lazyness, could just specify a large number and skip the sanity check :-P 
# ifs is expected to be COMMA (,)
# adapted from getAccVerFromBlastLine( line, colidx, ifs ) "pyphy_ext.py"
def processLine( line, colidx1, colidx2, renum_prefix, totCol, ifs ) : 
        dbg( 5, "processLine in: '%s'" % line )
        newLin = ""
        line = line.rstrip("\n\r")
        lineList = line.split( ifs )
        if( len(lineList) > totCol  ) :
                #dbg( 1, "Not enough columns for input line '%s'" % line )
                dbg( 1, "ERROR! Unexpected number of columns! input line has %s col, expected max of %s " % (len(lineList), totCol) )
                dbg( 4, "Line split into %s words" % len (lineList) )
                return ""       # return empty string if line did not have required number of columns
        #dbg( 5, "col idx: %s has val: %s"  % (colidx, lineList[colidx]) )
        # wants to iterate each col idx till the end
        # process each column as it is scanned and modify as needed
        idx = 0
        newLin = ""
        for item in lineList :
                dbg( 4, "item[%s] contains: '%s'" % (idx, item) )
                if( idx == colidx1 or idx == colidx2 ) :
                        dbg(4, "need to renum this image column '%s'" % item )
                        imageNum = lineList[idx].strip()       # strip() removes white space on left and right ends only, not middle
                        if( re.search( '^[0-9]+$', imageNum ) ) :
                             # re is the regular expression match.  
                             #dbg( 2, "Extract ok for imageNum [%14s] from input line '%s'" % (imageNum, line) )
                             #newImageNum = ( int(renum_prefix) * 10000 )+ int(imageNum)        # 1609140035
                             newImageNum =  ( int(imageNum) * 1000000 )  + int(renum_prefix)    #   35140916 is better for big data hash partitioning (also changed process_cli)
                             dbg( 5, "imageNum [%4s] changed to [%10s] from input line '%s'" % (imageNum, newImageNum, line) )
                             newLin = newLin + str(newImageNum) 
                        else :
                             dbg( 1, "Fail - imageNum pattern not found at col index '%s' for input line '%s'" % (colidx, line) )
                             return "***ERROR unexpected pattern***"  # error case
                else :
                        #newLin.push( item )     # tmp
                        newLin = newLin + item.strip('\"')            
                #return ""
                idx = idx + 1
                #if idx <= len(lineList) :
                if idx < len(lineList) :                
                        newLin = newLin + ifs            # careful, avoid tailing comma 
                        #newLin = newLin + ","           # careful, avoid tailing comma 
        #print( "====== new line ======" )
        dbg( 3, "processLine out: '%s'" % newLin )
        return newLin #line
# end processLine()

def processFile( filename, outDir, colidx1, colidx2, prefix, totCol, ifs ) :
        f = open( filename, "r" )
        outFilename = outDir + "/" + os.path.basename(filename)
        outf = open( outFilename, "w" )
        for line in f :
                        newLin = processLine( line, colidx1, colidx2, prefix, totCol, ifs )
                        dbg( 4, "result line is '%s'" % newLin )
                        print( newLin, file = outf )

        f.close()
        outf.close()
 

def renum_relationship_csv( args ) :
        # example input line for SQL_385_396_Relationships.CSV
        # 1,385,3,385,6
        # col 1 and 3 are the image number that need transforming  (python is 0-based indexing)
        colidx1 = 1
        colidx2 = 3
        totCol  = 5             # total number of column, for sanity check of processed line
        #colidx2 = -1 # use negative number for col idx that would not match
        filelist = glob.glob( args.indir + "/[Ss][Qq][Ll]_*_[Rr]elationships.[Cc][Ss][Vv]" ) 
        for fil in filelist:
                #print( "getting basename ... %s" % os.path.basename(fil) )
                dbg( 2, "Working on file %s" % fil )
                processFile( fil, args.outdir, colidx1, colidx2, args.prefix, totCol, args.IFS )
# end renum_relationship_csv procedure


def renum_membranes_csv( args ) :
        # schema says:
        # ImageNumber INTEGER$
        # Membranes_Number_Object_Number integer                # hopefully this don't matter
        colidx1 = 0
        colidx2 = -1    # use negative number for col idx that would not match
        maxCol  = 228   # total number of column, for sanity check of processed line, don't have to be exact, a rough high limit is enough
        #maxCol  = 227   # total number of column, for sanity check of processed line, don't have to be exact, a rough high limit is enough
        filelist = glob.glob( args.indir + "/[Ss][Qq][Ll]_*_[Mm]embranes.[Cc][Ss][Vv]" ) 
        for fil in filelist:
                #print( "getting basename ... %s" % os.path.basename(fil) )
                dbg( 2, "Working on file %s" % fil )
                processFile( fil, args.outdir, colidx1, colidx2, args.prefix, maxCol, args.IFS )
# end renum_..._csv procedure
        
def renum_image_csv( args ) :
        # schema starts as:
        # ImageNumber INTEGER$
        # Image_Align_Xshift_Aligned_GFP integer
        colidx1 = 0
        colidx2 = -1    # use negative number for col idx that would not match
        maxCol  = 253   # total number of column, for sanity check of processed line, don't have to be exact, a rough high limit is enough
        #maxCol  = 252   # total number of column, for sanity check of processed line, don't have to be exact, a rough high limit is enough
        filelist = glob.glob( args.indir + "/[Ss][Qq][Ll]_*_[Ii]mage.[Cc][Ss][Vv]" ) 
        for fil in filelist:
                #print( "getting basename ... %s" % os.path.basename(fil) )
                dbg( 2, "Working on file %s" % fil )
                processFile( fil, args.outdir, colidx1, colidx2, args.prefix, maxCol, args.IFS )
# end renum_..._csv procedure

def renum_nucleoids_csv( args ) :
        # schema says:
        # ImageNumber INTEGER$
        # Nucleoids_Number_Object_Number integer                # hopefully this don't matter
        colidx1 = 0
        colidx2 = -1    # use negative number for col idx that would not match
        maxCol  = 191     # total number of column, for sanity check of processed line, just put a large number for now
        filelist = glob.glob( args.indir + "/[Ss][Qq][Ll]_*_[Nn]ucleoids.[Cc][Ss][Vv]" ) 
        for fil in filelist:
                #print( "getting basename ... %s" % os.path.basename(fil) )
                dbg( 2, "Working on file %s" % fil )
                processFile( fil, args.outdir, colidx1, colidx2, args.prefix, maxCol, args.IFS )
# end renum_..._csv procedure

def renum_whole_cell_mask_csv( args ) :
        # schema says:
        # ImageNumber INTEGER
        # Whole_Cell_Mask_Number_Object_Number integer,$
        # Whole_Cell_Mask_AreaShape_Area float,$
        colidx1 = 0
        colidx2 = -1    # use negative number for col idx that would not match
        maxCol  = 67    # total number of column, for sanity check of processed line, just put a large number for now
        filelist = glob.glob( args.indir + "/[Ss][Qq][Ll]_*_[Ww]hole_[Cc]ell_[Mm]ask.[Cc][Ss][Vv]" ) 
        for fil in filelist:
                #print( "getting basename ... %s" % os.path.basename(fil) )
                dbg( 2, "Working on file %s" % fil )
                processFile( fil, args.outdir, colidx1, colidx2, args.prefix, maxCol, args.IFS )
# end renum_..._csv procedure



def postrun_wrapup( args ) :
        end_time = datetime.datetime.now()
        dbg(1, "csv image renumbering done at %s" % end_time )
        print( "The End.  Renumbered csv stored in outdir of %s" % args.outdir )
# end prerun_setup procedure




        
def main():
        args = process_cli()
        prerun_setup(args)
        renum_relationship_csv(args)
        renum_membranes_csv( args )
        renum_image_csv( args )
        renum_whole_cell_mask_csv( args )
        renum_nucleoids_csv( args )
        postrun_wrapup(args)
# main()-end


### end of all fn definition, begin of main program flow.
main()

