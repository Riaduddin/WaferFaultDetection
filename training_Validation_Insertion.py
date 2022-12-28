from Training_Raw_data_validation.rawValidation import Raw_Data_validation
from DataTransform_Training.DataTransformation import dataTransform
from DataTypeValidation_Insertion_Training.DataTypeValidation import dBOperation
from application_logging import logger

class train_validation:
    def __init__(self,path):
        self.raw_data = Raw_Data_validation(path)
        self.dataTransform = dataTransform()
        self.dBOperation = dBOperation()
        self.file_object=open('Training_Logs/Training_Main_Log.txt','a+')
        self.log_writer=logger.App_Logger()

    def train_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Start of Validation on files!!')

            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valuesFromSchema()

            regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"    #self.raw_data.manualRegexCreation()

            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)