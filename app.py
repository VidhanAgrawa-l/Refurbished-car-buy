import streamlit as st
import pandas as pd
import pickle
# With this more robust import approach:
import os
import sys

# Add the current directory to the path so Python can find the src package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now import the modules
from src.data_preprocessing import preprocess_input
from src.model_utils import load_model, make_prediction

# Set page configuration
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# Load the model
model = load_model('models/cardekho_model.pkl')

# Load sample data for statistics
@st.cache_data
def load_data():
    return pd.read_csv('dataset/cardekho_imputated.csv')

df = load_data()

# App title and description
st.title('🚗 Used Car Price Predictor')
st.markdown("""
This app predicts the price of used cars based on various features like brand, model, age, mileage, etc.
Simply fill in the details of the car you're interested in, and get an estimated selling price!
""")

# Create sidebar for inputs
st.sidebar.header('Car Details')

# Brand selection with statistics
brands = sorted(df['brand'].unique())
selected_brand = st.sidebar.selectbox('Brand', brands)

# Filter models based on selected brand
brand_models = sorted(df[df['brand'] == selected_brand]['model'].unique())
selected_model = st.sidebar.selectbox('Model', brand_models)

# Vehicle age
vehicle_age = st.sidebar.slider('Vehicle Age (years)', 0, 20, 5)

# Kilometers driven
km_driven = st.sidebar.number_input('Kilometers Driven', min_value=0, max_value=500000, value=50000, step=5000)

# Seller type
seller_type = st.sidebar.selectbox('Seller Type', ['Individual', 'Dealer'])

# Fuel type
fuel_type = st.sidebar.selectbox('Fuel Type', ['Petrol', 'Diesel', 'CNG', 'LPG', 'Electric'])

# Transmission type
transmission_type = st.sidebar.selectbox('Transmission Type', ['Manual', 'Automatic'])

# Mileage (km/l)
mileage = st.sidebar.slider('Mileage (km/l)', 5.0, 35.0, 18.0, 0.1)

# Engine (cc)
engine = st.sidebar.slider('Engine (cc)', 500, 5000, 1200, 50)

# Max Power (bhp)
max_power = st.sidebar.slider('Max Power (bhp)', 20.0, 400.0, 80.0, 0.1)

# Number of seats
seats = st.sidebar.slider('Number of Seats', 2, 10, 5)

# Create a dictionary of inputs
input_data = {
    'car_name': f"{selected_brand} {selected_model}",
    'brand': selected_brand,
    'model': selected_model,
    'vehicle_age': vehicle_age,
    'km_driven': km_driven,
    'seller_type': seller_type,
    'fuel_type': fuel_type,
    'transmission_type': transmission_type,
    'mileage': mileage,
    'engine': engine,
    'max_power': max_power,
    'seats': seats
}

# Main content area
st.header('Car Analysis')

# Display 3 columns for visualization
col1, col2, col3 = st.columns(3)

# Column 1: Brand statistics
with col1:
    st.subheader(f"{selected_brand} Statistics")
    brand_df = df[df['brand'] == selected_brand]
    st.metric("Average Price", f"₹{int(brand_df['selling_price'].mean()):,}")
    st.metric("Cars Available", f"{len(brand_df)}")
    
    # Brand price range
    min_price = int(brand_df['selling_price'].min())
    max_price = int(brand_df['selling_price'].max())
    st.write(f"Price Range: ₹{min_price:,} - ₹{max_price:,}")

# Column 2: Model statistics
with col2:
    st.subheader(f"{selected_model} Statistics")
    model_df = df[(df['brand'] == selected_brand) & (df['model'] == selected_model)]
    if not model_df.empty:
        st.metric("Average Price", f"₹{int(model_df['selling_price'].mean()):,}")
        st.metric("Cars Available", f"{len(model_df)}")
        
        # Model price range
        min_price = int(model_df['selling_price'].min())
        max_price = int(model_df['selling_price'].max())
        st.write(f"Price Range: ₹{min_price:,} - ₹{max_price:,}")
    else:
        st.write("No data available for this model.")

# Column 3: Age impact
with col3:
    st.subheader("Age Impact on Price")
    age_price = df.groupby('vehicle_age')['selling_price'].mean().reset_index()
    st.line_chart(age_price.set_index('vehicle_age'))

# Predict button
if st.sidebar.button('Predict Price'):
    # Preprocess the input data
    processed_data = preprocess_input(input_data)
    
    # Make prediction
    prediction = make_prediction(model, processed_data)
    
    # Display prediction
    st.success(f"### Predicted Price: ₹{int(prediction):,}")
    
    # Additional insights
    st.header("Insights")
    
    # Compare with average
    avg_price = df[(df['brand'] == selected_brand) & (df['model'] == selected_model)]['selling_price'].mean()
    if not pd.isna(avg_price):
        diff = prediction - avg_price
        if diff > 0:
            st.info(f"This price is ₹{int(abs(diff)):,} higher than the average {selected_brand} {selected_model} in our database.")
        else:
            st.info(f"This price is ₹{int(abs(diff)):,} lower than the average {selected_brand} {selected_model} in our database.")
    
    # Factors affecting price
    st.subheader("Factors Affecting Price")
    factors = [
        f"**Vehicle Age**: Older vehicles generally have lower prices.",
        f"**Kilometers Driven**: Cars with higher mileage often sell for less.",
        f"**Transmission**: Automatic transmissions can command a premium.",
        f"**Fuel Type**: Fuel efficiency and type affect resale value.",
        f"**Seller Type**: Dealer prices may include markup compared to individual sellers."
    ]
    for factor in factors:
        st.write(factor)

# Add data exploration section
st.header("Data Exploration")
show_data = st.checkbox("Show Raw Data Sample")
if show_data:
    st.write(df.head())

# Price distribution
st.subheader("Price Distribution by Brand")
brand_prices = df.groupby('brand')['selling_price'].mean().sort_values(ascending=False).head(10)
st.bar_chart(brand_prices)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and XGBoost")