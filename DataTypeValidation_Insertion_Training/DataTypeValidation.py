import csv
import shutil
from application_logging.logger import App_Logger
from os import listdir
import os
import sqlite3
class dBOperation:

    def __init__(self):
        self.path = 'Training_Database/'
        self.badFilePath = "Training_Raw_files_validated/Bad_Raw"
        self.goodFilePath = "Training_Raw_files_validated/Good_Raw"
        self.logger = App_Logger()

    def dataBaseConnection(self,DatabaseName):

        try:
            conn = sqlite3.connect(self.path + DatabaseName + '.db')
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" % DatabaseName)
            file.close()

        except ConnectionError:
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError
        return conn

    def createTableDb(self, DatabaseName, column_names):


        try:
            conn = self.dataBaseConnection(DatabaseName)
            c = conn.cursor()
            c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Good_Raw_Data'")
            if c.fectone()[0]==1:
                conn.close()
                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()
            else:
                for key in column_names.keys():
                    type=column_names[key]

                    try:
                        conn.execute("ALTER TABLE Good_Raw_Data ADD COLUMN '{column_name}' {datatype}"),format(column_name=key,dataType=type)
                    except:
                        conn.execute('CREATE TABLE Good_Raw_Data ({column_name} {datatype}'.format(column_name=key,dataType=type))

                conn.close()

                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

        except Exception as e:
            file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e

    def insertIntoTableGoodData(self,Database):

        conn = self.dataBaseConnection(Database)
        goodFilePath = self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        log_file = open("Training_Logs/DbInsertLog.txt", 'a+')

        for file in onlyfiles:
            try:
                with open(goodFilePath+'/'+file,'r') as f:
                    next(f)
                    reader=csv.reader(f,delimiter='\n')
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_1)))
                                self.logger.log(log_file, " %s: File loaded successfully!!" % file)
                                conn.commit()

                            except Exception as e:
                                raise e

            except Exception as e:

                conn.rollback()
                self.logger.log(log_file,"Error while creating table: %s " % e)
                shutil.move(goodFilePath+'/' + file, badFilePath)
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                conn.close()

        conn.close()
        log_file.close()