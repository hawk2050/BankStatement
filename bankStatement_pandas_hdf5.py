#!/usr/bin/python
from pandas import read_csv
import time, sys
import hashlib
import statementImport

#You can store dates in SQLite with the following data types:

#TEXT as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS").

#http://greeennotebook.com/2010/06/how-to-use-sqlite3-from-python-introductory-tutorial/

SEPARATOR = ','
QUOTECHAR = '"'

csvformat = {'Separator':SEPARATOR,'QuoteChar':QUOTECHAR,'TransType':0,'Entity':1,'Description':2,'Unknown':3,'Unknown2':4,'Amount':5,'Date':6}

        

def checkAlreadyExist(curs,hashString):
    
    sql = "SELECT * FROM pp_transactions WHERE hashvalue=?"
    curs.execute(sql, [(hashString)])
    duplicateEntries = curs.fetchall()  # or use fetchone()
    
    return duplicateEntries 
        



if __name__ == "__main__":

    t = time.time()
    
  
    if len(sys.argv) == 1:
        sys.argv.insert(1, "./data/082012_PP_RCA_v2.csv")
    filename = sys.argv[1]
    print("loading file {}".format(filename))
    
    df = read_csv(filename)
    print df