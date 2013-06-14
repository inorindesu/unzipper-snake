#!/usr/bin/python
#
# unzipper.py
# Extract zip files containing files with non-ascii encoding
# 
# Copyright (C) 2013  Inori Sakura <inorindesu@gmail.com>
# 
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.
#
# unzipper.py:
# A python scrpt for extracting zip files containing files with
# CJK (or other) encoded filenames.
#
# To extract a zip file, use:
# ./unzipper.py -d extract/to/here -e big5 a.zip
#
# To list file names of a zip file, use:
# ./unzipper.py -d extract/to/here -e big5 -l a.zip

import sys
import getopt
import zipfile
import codecs

directory = "."
encoding = "ascii"
inFile = ''
doExtraction = True
doListing = False

def usage():
    fp = sys.stderr
    fp.write("Usage: {0} -[h|l|e ENCODING|d TARGET_DIR] INPUT_FILE(S)\n\n".format(sys.argv[0]))
    fp.write("\t-h\t\tPrint help message\n")
    fp.write("\t-e ENC\t\tSet encoding of filename\n")
    fp.write("\t-l\t\tList contents of the files\n")
    fp.write("\t-d TARGET_DIR\tExtract files to TARGET_DIR\n")
    fp.write("\nBeware that the filelist should be put after all command line options!\n")
    fp.write("\nFor all available encodings, please consult:\n")
    fp.write("http://docs.python.org/2/library/codecs.html#standard-encodings\n")

def extractFile(f):
    zf = None
    try:
        zf = zipfile.ZipFile(f)
    except IOError:
        sys.stderr.write("ERROR: file {0} not found\n".format(f))
        return

    # change info.filename for each ZipInfo
    # and extract the file
    for info in zf.infolist():
        try:
            info.filename = info.filename.decode(encoding)
            zf.extract(info, directory)
        except UnicodeError:
            sys.stderr.write("ERROR: when decoding filename with encoding {0}\n".format(encoding))
    zf.close()

def listFile(f):
    zf = None
    try:
        zf = zipfile.ZipFile(f)
    except IOError:
        sys.stderr.write("ERROR: file {0} not found\n".format(f))
        return

    for info in zf.infolist():
        try:
            sys.stdout.write("{0}\n".format(info.filename.decode(encoding)))
        except UnicodeError:
            sys.stderr.write("ERROR: when decoding filename with encoding {0}\n".format(encoding))
    zf.close()

#
# argument collection
#
opts = None
args = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "he:d:l")
except getopt.GetoptError:
    usage()
    exit()

for opt, arg in opts:
    if opt == '-h':
        usage()
        exit()
    elif opt == '-d':
        directory = arg
    elif opt == '-e':
        encoding = arg
        try:
            codecs.lookup(encoding)
        except LookupError:
            sys.stderr.write("ERROR: encoding {0} is unknown to python.\n".format(encoding))
            exit()
    elif opt == '-l':
        doExtraction = False
        doListing = True

if len(args) == 0:
    sys.stderr.write("No input zip file(s) specified!\n")
    usage()
    exit()

#
# Let's do the job!
#
if doListing == True and doExtraction == False:
    if len(args) > 1:
        for f in args:
            sys.stdout.write(">==  {0}  ==<\n".format(f))
            listFile(f)
    else:
        listFile(args[0])
elif doListing == False and doExtraction == True:
    if len(args) > 1:
        for f in args:
            sys.stdout.write("Extracting {0}..\n".format(f))
            extractFile(f)
    else:
        extractFile(args[0])
