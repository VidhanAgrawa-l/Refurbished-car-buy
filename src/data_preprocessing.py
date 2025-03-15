import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pickle
import os

def preprocess_input(input_data):
    """
    Preprocess user input data to match the format expected by the model
    
    Parameters:
    input_data (dict): Dictionary containing user input values
    
    Returns:
    pd.DataFrame: Preprocessed data ready for prediction
    """
    # Convert input to DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Handle categorical variables (same as training)
    categorical_cols = ['brand', 'model', 'seller_type', 'fuel_type', 'transmission_type']
    
    # Try to load encoders if they exist, otherwise create simple encoding
    encoder_path = 'models/encoder.pkl'
    if os.path.exists(encoder_path):
        with open(encoder_path, 'rb') as f:
            encoder = pickle.load(f)
        # Transform using the loaded encoder
        cat_encoded = encoder.transform(input_df[categorical_cols])
        # Get the feature names
        encoded_feature_names = encoder.get_feature_names_out(categorical_cols)
        # Create a DataFrame with encoded features
        cat_df = pd.DataFrame(cat_encoded, columns=encoded_feature_names)
    else:
        # Simple one-hot encoding if no encoder is saved
        cat_df = pd.get_dummies(input_df[categorical_cols], drop_first=True)
    
    # Keep the numerical features
    num_cols = ['vehicle_age', 'km_driven', 'mileage', 'engine', 'max_power', 'seats']
    num_df = input_df[num_cols].copy()
    
    # Try to load scaler if it exists
    scaler_path = 'models/scaler.pkl'
    if os.path.exists(scaler_path):
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        # Scale the numerical features
        num_df = pd.DataFrame(scaler.transform(num_df), columns=num_cols)
    
    # Combine numerical and categorical features
    final_df = pd.concat([num_df, cat_df], axis=1)
    
    return final_df

def load_sample_data():
    """
    Load the sample data for reference
    
    Returns:
    pd.DataFrame: Sample car dataset
    """
    df = pd.read_csv('dataset/cardekho_imputated.csv')
    return df