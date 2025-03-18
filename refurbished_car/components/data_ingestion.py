from refurbished_car.exception.exception import RefurbishedCarException
from refurbished_car.logging.logger import logging


## configuration of the Data Ingestion Config

from refurbished_car.entity.config_entity import DataIngestionConfig
from refurbished_car.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL") # reading the mongo db url from the environment variable 


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):# inherit the DataIngestionConfig class from the config_entity.py file
        try:
            self.data_ingestion_config=data_ingestion_config# this will have all the configuration related to the data ingestion since we are inheriting the DataIngestionConfig class
        except Exception as e:
            raise RefurbishedCarException(e,sys)
        
    def export_collection_as_dataframe(self):
        """
        Read data from mongodb
        """
        try:
            database_name=self.data_ingestion_config.database_name # reading the database name from the data_ingestion_config WHICH IS INHERITED FROM THE DataIngestionConfig class of config_entity.py file
            collection_name=self.data_ingestion_config.collection_name # reading the collection name from the data_ingestion_config WHICH IS INHERITED FROM THE DataIngestionConfig class of config_entity.py file
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]# reading the collection from the database which is present in the mongodb

            df=pd.DataFrame(list(collection.find()))# reading the data from the collection and converting it into the dataframe
            if "_id" in df.columns.to_list():# checking if the _id column is present in the dataframe
                df=df.drop(columns=["_id"],axis=1)# if present then drop the column
            
            df.replace({"na":np.nan},inplace=True) # replace the na values with the np.nan values
            return df
        except Exception as e:
            raise RefurbishedCarException
        
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        """
        Export the data into the feature store file path as csv from mongodb
        """
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path 
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
            
        except Exception as e:
            raise RefurbishedCarException(e,sys)
        
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")

            
        except Exception as e:
            raise RefurbishedCarException(e,sys)
        
        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact

        except Exception as e:
            raise RefurbishedCarException
        