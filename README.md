# Car Price Predictor Application

This application predicts the selling price of used cars based on various features like brand, model, age, mileage, etc. using an XGBoost Regression model.

## Project Structure

```
CAR DEKHO/
├── dataset/
│   └── cardekho_imputated.csv
├── models/
│   └── cardekho_model.pkl
├── notebooks/
│   └── Xgboost Regression Implementation.ipynb
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   └── model_utils.py
├── app.py
└── README.md
```

## Installation

1. Make sure you have Python 3.8+ installed
2. Install the required packages:

```bash
pip install streamlit pandas scikit-learn xgboost numpy
```

## Running the Application

To run the Streamlit app:

```bash
streamlit run app.py
```

This will start the application and open it in your default web browser.

## Features

- Interactive UI to input car details
- Real-time price prediction
- Data visualizations for market insights
- Comparison with average prices
- Factors affecting car prices

## Model Information

The application uses an XGBoost Regression model trained on car sales data. The model takes into account multiple features such as:

- Car brand and model
- Vehicle age
- Kilometers driven
- Seller type (Individual or Dealer)
- Fuel type
- Transmission type
- Mileage
- Engine capacity
- Maximum power
- Number of seats

## Additional Notes

- The data preprocessing step handles categorical variables through one-hot encoding
- Numerical variables are scaled for better model performance
- The model file (`cardekho_model.pkl`) contains the trained XGBoost model