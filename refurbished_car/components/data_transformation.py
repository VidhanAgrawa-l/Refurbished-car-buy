# import sys
# import os
# import numpy as np
# import pandas as pd
# from sklearn.impute import KNNImputer
# from sklearn.pipeline import Pipeline

# from refurbished_car.constant.training_pipeline import TARGET_COLUMN
# from refurbished_car.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

# from refurbished_car.entity.artifact_entity import (
#     DataTransformationArtifact,
#     DataValidationArtifact
# )

# from refurbished_car.entity.config_entity import DataTransformationConfig
# from refurbished_car.exception.exception import RefurbishedCarException
# from refurbished_car.logging.logger import logging
# from refurbished_car.utils.main_utils.utils import save_numpy_array_data,save_object

# class DataTransformation:
#     def __init__(self,data_validation_artifact:DataValidationArtifact,
#                  data_transformation_config:DataTransformationConfig):
#         try:
#             self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
#             self.data_transformation_config:DataTransformationConfig=data_transformation_config
#         except Exception as e:
#             raise RefurbishedCarException(e,sys)
        
#     @staticmethod
#     def read_data(file_path) -> pd.DataFrame:
#         try:
#             return pd.read_csv(file_path)
#         except Exception as e:
#             raise RefurbishedCarException(e, sys)
        
#     def get_data_transformer_object(cls)->Pipeline:
#         """
#         It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
#         and returns a Pipeline object with the KNNImputer object as the first step.

#         Args:
#           cls: DataTransformation

#         Returns:
#           A Pipeline object
#         """
#         logging.info(
#             "Entered get_data_trnasformer_object method of Trnasformation class"
#         )
#         try:
#            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
#            logging.info(
#                 f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
#             )
#            processor:Pipeline=Pipeline([("imputer",imputer)])
#            return processor
#         except Exception as e:
#             raise RefurbishedCarException(e,sys)

        
#     def initiate_data_transformation(self)->DataTransformationArtifact:
#         logging.info("Entered initiate_data_transformation method of DataTransformation class")
#         try:
#             logging.info("Starting data transformation")
#             train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
#             test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

#             ## training dataframe
#             input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
#             target_feature_train_df = train_df[TARGET_COLUMN]
#             target_feature_train_df = target_feature_train_df.replace(-1, 0)

#             #testing dataframe
#             input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
#             target_feature_test_df = test_df[TARGET_COLUMN]
#             target_feature_test_df = target_feature_test_df.replace(-1, 0)

#             preprocessor=self.get_data_transformer_object()

#             preprocessor_object=preprocessor.fit(input_feature_train_df)
#             transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
#             transformed_input_test_feature =preprocessor_object.transform(input_feature_test_df)
             

#             train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
#             test_arr = np.c_[ transformed_input_test_feature, np.array(target_feature_test_df) ]

#             #save numpy array data
#             save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
#             save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
#             save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_object,)

#             save_object( "final_model/preprocessor.pkl", preprocessor_object,)


#             #preparing artifacts

#             data_transformation_artifact=DataTransformationArtifact(
#                 transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
#                 transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
#                 transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
#             )
#             return data_transformation_artifact


            
#         except Exception as e:
#             raise RefurbishedCarException(e,sys)





import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from refurbished_car.constant.training_pipeline import TARGET_COLUMN
from refurbished_car.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from refurbished_car.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from refurbished_car.entity.config_entity import DataTransformationConfig
from refurbished_car.exception.exception import RefurbishedCarException
from refurbished_car.logging.logger import logging
from refurbished_car.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise RefurbishedCarException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise RefurbishedCarException(e, sys)
        
    def get_data_transformer_object(self) -> Pipeline:
        """
        Creates a preprocessing pipeline for car data that handles both numerical and categorical features.
        
        Returns:
          A ColumnTransformer object that processes different feature types appropriately
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )
        try:
            # Define categorical and numerical columns based on the dataset
            categorical_columns = ['car_name', 'brand', 'model', 'seller_type', 'fuel_type', 'transmission_type']
            numerical_columns = ['vehicle_age', 'km_driven', 'mileage', 'engine', 'max_power', 'seats']
            
            # Create preprocessing steps for numerical features
            # Use SimpleImputer for missing numerical values followed by scaling
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )
            
            # Create preprocessing steps for categorical features
            # Use SimpleImputer with 'most_frequent' strategy for categorical data before encoding
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder(sparse_output=False, handle_unknown='ignore'))
                ]
            )
            
            # Combine both pipelines in a column transformer
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ],
                remainder='drop'  # Drop any columns not specified
            )
            
            logging.info(
                f"Created preprocessing pipeline for numerical and categorical features"
            )
            
            return preprocessor
        except Exception as e:
            raise RefurbishedCarException(e, sys)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            logging.info(f"Train dataframe shape: {train_df.shape}")
            logging.info(f"Test dataframe shape: {test_df.shape}")
            
            # Print column data types for debugging
            logging.info(f"Train dataframe data types: {train_df.dtypes}")

            # Training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            
            # Testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            
            # Get preprocessing object
            preprocessor = self.get_data_transformer_object()
            
            # Fit on training data
            logging.info("Fitting preprocessor on training data")
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            
            # Transform training and testing data
            logging.info("Transforming training and testing data")
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            
            # Log transformed data shapes
            logging.info(f"Transformed train data shape: {transformed_input_train_feature.shape}")
            logging.info(f"Transformed test data shape: {transformed_input_test_feature.shape}")
            
            # Combine features and target
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]
            
            # Save transformed data and preprocessor object
            logging.info("Saving transformed data and preprocessor object")
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)
            
            # Also save preprocessor to final_model directory for convenience
            os.makedirs("final_model", exist_ok=True)  # Ensure directory exists
            save_object("final_model/preprocessor.pkl", preprocessor_object)
            
            # Prepare artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            
            logging.info("Data transformation completed successfully")
            return data_transformation_artifact
            
        except Exception as e:
            logging.error(f"Error in data transformation: {e}")
            raise RefurbishedCarException(e, sys)