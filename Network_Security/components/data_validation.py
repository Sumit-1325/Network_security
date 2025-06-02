from Network_Security.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from Network_Security.entity.config_entity import DataValidationConfig
from Network_Security.entity.config_entity import TrainingPipelineConfig
from Network_Security.exception.exception import CustomException
from Network_Security.logging.logger import logging
from Network_Security.constant.training_pipeline import SCHEMA_FILE_PATH
from Network_Security.utils.main_utils.utils import read_yaml_file,write_yaml_file
import sys,os
from scipy.stats import ks_2samp
import numpy as np
import pandas as pd


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                    data_validation_config:DataValidationConfig):
            
            try:
                self.data_ingestion_artifact=data_ingestion_artifact
                self.data_validation_config=data_validation_config
                self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            except Exception as e:
                raise CustomException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:  
            raise CustomException(e,sys)  


    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise CustomException(e,sys)          


    def detect_dataset_drift (self,base_df,current_df,threshold=0.05):
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                if d1.dtype != object:
                    d1 = d1.astype('float32')
                    d2 = d2.astype('float32')
                    p = ks_2samp(d1, d2)
                if p.pvalue > threshold:
                    status = False
                report.update({column:{
                    "pvalues":float(p.pvalue),
                    "same_distribution":status

                }})
            drift_report = self.data_validation_config.drift_report_file_path
            

            #create Directory
            dir_path = os.path.dirname(drift_report)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report,content=report)

        except Exception as e:
            raise CustomException(e,sys)




    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_File_Path = self.data_ingestion_artifact.train_file_path
            test_File_Path = self.data_ingestion_artifact.test_file_path

            # reading train and test file Via Above Staticmethod
            train_df = DataValidation.read_data(train_File_Path)
            test_df = DataValidation.read_data(test_File_Path)

            #Validate the No of columnns 
            status=self.validate_number_of_columns(dataframe=train_df)
            if not status:
                error_message=f"Train dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(dataframe=test_df)
            if not status:
                error_message=f"Test dataframe does not contain all columns.\n"   

            #detect datadrift 
            status = self.detect_dataset_drift(base_df=train_df, current_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True

            )

            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)



