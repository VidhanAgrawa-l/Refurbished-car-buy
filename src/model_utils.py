import pickle
import numpy as np
import pandas as pd
import os

def load_model(model_path):
    """
    Load the trained model from the given path
    
    Parameters:
    model_path (str): Path to the saved model file
    
    Returns:
    object: Loaded model
    """
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def make_prediction(model, input_data):
    """
    Make a prediction using the loaded model
    
    Parameters:
    model (object): Loaded model
    input_data (pd.DataFrame): Preprocessed input data
    
    Returns:
    float: Predicted car price
    """
    if model is None:
        return 0
    
    try:
        # Make prediction
        prediction = model.predict(input_data)
        
        # Return the first prediction (should only be one)
        return float(prediction[0])
    except Exception as e:
        print(f"Error making prediction: {e}")
        return 0

def evaluate_model_performance(model, X_test, y_test):
    """
    Evaluate the model performance on test data
    
    Parameters:
    model (object): Loaded model
    X_test (pd.DataFrame): Test features
    y_test (pd.Series): Test target
    
    Returns:
    dict: Dictionary containing performance metrics
    """
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
        'MAE': mean_absolute_error(y_test, y_pred),
        'R2': r2_score(y_test, y_pred)
    }
    
    return metrics