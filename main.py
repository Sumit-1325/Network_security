from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.exception.exception import CustomException
from Network_Security.components.data_validation import DataValidation
from Network_Security.components.data_transformation import DataTransformation,DataTransformationConfig
from Network_Security.logging.logger import logging
from Network_Security.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
)
from Network_Security.entity.config_entity import TrainingPipelineConfig
import os
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Data Ingestion started")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")
        print(data_ingestion_artifact)


        data_validation_config = DataValidationConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_validation = DataValidation(
            data_validation_config=data_validation_config,
            data_ingestion_artifact=data_ingestion_artifact,
        )
        logging.info("Data Validation started")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")
        print(data_validation_artifact)

        logging.info("datatransformation started")
        data_transformation_config = DataTransformationConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_transformation_artifact = DataTransformation(data_transformation_config=data_transformation_config,data_validation_artifact=data_validation_artifact)
        data_transformation_artifact = data_transformation_artifact.initiate_data_transformation()
        logging.info("datatransformation completed")
        print(data_transformation_artifact)
        
        
    except Exception as e:
        raise CustomException(e, sys)
