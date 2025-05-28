import sys
import os 
import json
from dotenv import load_dotenv 

load_dotenv()

mongoDbUrl = os.getenv("MongoDbUrl")

import certifi

ca = certifi.where()

import pymongo
import pandas as pd
import numpy as np
from Network_Security.exception.exception import CustomException
from Network_Security.logging.logger import logging

class ExtractData():
    def __init__(self) :
        try:
           pass
        except Exception as e:
            raise CustomException(e,sys)
        
    def dv_to_json(self,file_path: str):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomException(e,sys)
    
    def insert_data_MongoDB(self,records,collection,Database):
        try:
            self.records = records
            self.collection = collection
            self.Database = Database

            self.client = pymongo.MongoClient(mongoDbUrl,tlsCAFile=ca)
            self.db = self.client[self.Database]
            self.collection = self.db[self.collection]
            self.collection.insert_many(self.records)

            return (len(self.records))
            
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    FILE_PATH = r"Network_Data\phisingData.csv"
    DATABASE = "ML_Data"
    collection = "Network_Security"

    network_obj = ExtractData()
    records = network_obj.dv_to_json(file_path=FILE_PATH)
    print(records)
    no_of_records = network_obj.insert_data_MongoDB(records=records,collection=collection,Database=DATABASE)
    print(no_of_records)