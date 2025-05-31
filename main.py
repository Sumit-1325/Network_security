from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.exception.exception import CustomException
from Network_Security.logging.logger import logging
from Network_Security.entity.config_entity import DataIngestionConfig
from Network_Security.entity.config_entity import TrainingPipelineConfig
import os
import sys 

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config) 
        logging.info("Data Ingestion started")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")
        print(data_ingestion_artifact)
    except Exception as e:
        raise CustomException(e, sys)