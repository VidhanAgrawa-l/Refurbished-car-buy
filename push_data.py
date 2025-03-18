import os
import sys
import json

from dotenv import load_dotenv # Use to load the .env(environment variable) file 
load_dotenv() # initialize the .env file

MONGO_DB_URL=os.getenv("MONGO_DB_URL") # Get the environment variable from the .env file
print(MONGO_DB_URL)

import certifi # Use to get the path of the certificate file to connect with the mongodb with ssl or tls in a secure way
ca=certifi.where() #retreve the path of the bundel of certificates and store it in ca 

import pandas as pd
import numpy as np
import pymongo
from refurbished_car.exception.exception import RefurbishedCarException # Import the custom exception class
from refurbished_car.logging.logger import logging # Import the custom logger class

class CarDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise RefurbishedCarException(e,sys) 
        
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True) # Reset the index of the dataframe
            records=list(json.loads(data.T.to_json()).values()) #data.T.to_json() convert the dataframe to json where .T is used for transpose of data and .values() convert the json to list
            return records
        except Exception as e:
            raise RefurbishedCarException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection): 
        try:
            self.database=database 
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL) # Connect with the mongodb using the url via pymongo
            self.database = self.mongo_client[self.database] # assign to this which database you want to connect 
            self.collection=self.database[self.collection] # assign to this which collection you want to connect
            self.collection.insert_many(self.records) # insert the records into the collection
            return(len(self.records))  # return the number of records inserted into the collection
        except Exception as e:
            raise RefurbishedCarException (e,sys)
        
if __name__=='__main__': #it is used to run the code only when the file is run directly not when it is imported in another file
    FILE_PATH="dataset/cardekho_imputated.csv"
    DATABASE="CardekhoData"
    Collection="RefurbishedCarData"
    networkobj=CarDataExtract() 
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records) 
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)
        