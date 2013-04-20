#!/usr/bin/python
import csv, time, sys
import hashlib

SEPERATOR = ','
QUOTECHAR = '"'

#Definition of the input CSV file format
#csvformat = {'Separator':SEPARATOR,'QuoteChar':QUOTECHAR,'TransType':0,'Entity':1,'Description':2,'Unknown':3,'Unknown2':4,'Amount':5,'Date':6}

#We need to define the format of the list row we need to build for input into the sqlite DB.
statementRowFormatForDB = {'Date':0,'TransType':1,'Entity':2,'Description':3,'Amount':4,'HashValue':5,'Category':6,'PropertyID':7}

class csvStatement(object):
    def __init__(self,filename,csvformat):
        self.csvformat = csvformat
        self.fileName = filename
        self.rawStatement = []
        self.modifiedStatement = []
        self._rowForDB = ['','','','','','','','']
        self._importCsvStatement()
        
    def _importCsvStatement(self):
        with open(filename, 'rb') as csvfile:
            self.rawStatement = csv.reader(csvfile, delimiter=SEPERATOR, quotechar=QUOTECHAR)
            self.rawStatement = list(self.rawStatement)
            
            for row in self.rawStatement:
                if len(row)==0:
                    break
                
                               
                self._rowForDB[statementRowFormatForDB['Date']] = self._dateTransform(row[csvformat['Date']])
                self._rowForDB[statementRowFormatForDB['TransType']] = row[csvformat['TransType']]
                self._rowForDB[statementRowFormatForDB['Entity']] = row[csvformat['Entity']]
                self._rowForDB[statementRowFormatForDB['Description']] = row[csvformat['Description']]
                self._rowForDB[statementRowFormatForDB['Amount']] = float(row[csvformat['Amount']])
                self._rowForDB[statementRowFormatForDB['HashValue']] = self._generateUniqueHash(row)
                self._rowForDB[statementRowFormatForDB['Category']] = ''
                self._rowForDB[statementRowFormatForDB['PropertyID']] = ''
                
                self.modifiedStatement.append(self._rowForDB)
                    

    def _dateTransform(self,csvDate):
        components = csvDate.split('/')
        newDate = components[2] + '-' + components[1] + '-' + components[0]
        return newDate


    def _generateUniqueHash(self,rowInStatement):
        #At this point all fields are still in string format from the CSV file
        h = hashlib.new('ripemd160')
        h.update(rowInStatement[csvformat['Date']]+rowInStatement[csvformat['Entity']]+str(rowInStatement[csvformat['Amount']]))
        hashString = h.hexdigest()
        return hashString



if __name__ == "__main__":
    
    SEPARATOR = ','
    QUOTECHAR = '"'
    
    csvformat = {'Separator':SEPARATOR,'QuoteChar':QUOTECHAR,'TransType':0,'Entity':1,'Description':2,'Unknown':3,'Unknown2':4,'Amount':5,'Date':6}


    t = time.time()
    
    if len(sys.argv) == 1:
        sys.argv.insert(1, "./data/082012_PP_RCA_v2.csv")
    filename = sys.argv[1]
    print("loading file {}".format(filename))
        
    csvStatementObj = csvStatement(filename,csvformat)
    
    print csvStatementObj.rawStatement    
    print csvStatementObj.modifiedStatement
