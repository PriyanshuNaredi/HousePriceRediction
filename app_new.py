import streamlit as st
import pandas as pd
import pickle
from num_to_words import num_to_word
import requests
import os

API_KEY = "0f9e8cd64be44b248d159b270003ccdc"

def get_lat_long(add):
    address = add
    if address == 'other':
        address = 'Bengaluru'

    url = f"https://api.geoapify.com/v1/geocode/search?text={address}&limit=1&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = data["features"][0]
        latitude = result["geometry"]["coordinates"][1]
        longitude = result["geometry"]["coordinates"][0]
        location = pd.DataFrame({
            'latitude': [latitude],
            'longitude': [longitude]
        }) 
    return location

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
import streamlit.components.v1 as components

data = pd.read_csv('cleaned_data.csv')
pipe = pickle.load(open('RidgeModel.pkl','rb'))
locations = sorted(data['location'].unique())

# Function to check if terms have been accepted
def check_terms_accepted():
    return False

# Function to mark terms as accepted
def mark_terms_accepted():
    with open("terms_accepted.txt", "w") as file:
        file.write("True")

def main():
    st.set_page_config(page_title="House Price Prediction", layout="wide", page_icon="🏠")

    # Header Section
    st.markdown(
        """
        <style>
            .header {
                position: relative;
                height: 500px;
                background-image: url('https://plus.unsplash.com/premium_photo-1675324517011-24d2c741c22f?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
                background-size: cover;
                background-position: center;
                color: white;
                text-align: center;
                padding-top: 100px;
            }

            .header h1 {
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 20px;
                color: #FFD700; /* Golden yellow */
                text-shadow: 2px 2px 4px #000000; /* Adding shadow for better visibility */
            }

            .header p {
                font-size: 24px;
                margin-bottom: 10px;
                color: #FFD700; /* Golden yellow */
            }

            .header a {
                color: #FFD700; /* Golden yellow */
                text-decoration: none;
                font-weight: bold;
            }
            
            .line-container {
                position: absolute;
                top: 50%;
                left: 0;
                width: 100%;
                height: 2px;
                background-color: #FFD700; /* Golden yellow */
                transform: translateY(-50%);
            }
        </style>
        """
    , unsafe_allow_html=True)

    st.markdown(
        """
        <div class="header">
            <div class="line-container"></div>
            <h1>House Price Prediction App</h1>
            <p>Predict the price of houses based on their features</p>
            <p>This app helps buyers and sellers to estimate the value of properties</p>
            <p>Welcome to our app! Visit our <a href="https://example.com" target="_blank">website</a>.</p>
            <p>Scroll down to predict house price</p>
        </div>
        """
    , unsafe_allow_html=True)

    # Terms of Service agreement
    if not check_terms_accepted():
        agree = st.checkbox("I agree to the Terms of Service")
        if agree:
            mark_terms_accepted()
        else:
            st.warning("You must agree to the Terms of Service to proceed.")
            st.stop()

    # Main App Section
    st.markdown(
        """
        <style>
            .main-section {
                background-color: #f5f5f5; /* Light gray */
                padding: 20px;
                border-radius: 20px;
                margin-bottom: 20px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Adding shadow for depth */
            }
        </style>
        """
    , unsafe_allow_html=True)

    st.markdown("<h2 class='main-section'>House Features</h2>", unsafe_allow_html=True)

    left, right = st.columns((2,2))
    total_bedrooms = left.number_input('BHK',
                                       step=1.0, format='%.1f', value=2.0)
    total_bathrooms = right.number_input('Bathrooms',
                                    step=1.0, format='%.1f', value=2.0)
    sqft = left.number_input('Sq Ft',  step=1.0,
                                   format='%.1f',value=1500.0)
    location = right.selectbox('Location', options=locations)

    button = st.button('Predict')

    # if button is pressed
    if button:
        # make prediction
        with st.spinner("Predicting..."):
            lat_long = get_lat_long(location)
            result = predict(total_bedrooms,total_bathrooms,sqft,location)
            total = str(num_to_word(result, lang='en')).replace(',',' ').title()
            st.success(f'The value of the house is ₹{result}  {total}')
            st.map(lat_long,zoom=16)

def predict(bhk,bath,sqft,location):
    input = pd.DataFrame([[location,sqft,bath,bhk]]
        ,columns=['location','total_sqft','bath','BHK'])
    prediction = pipe.predict(input)[0] * 1e5 # 1e5 -> 1 Lakh

    result = int(prediction)
    return result

main()


