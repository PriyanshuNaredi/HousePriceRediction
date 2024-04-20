import streamlit as st
import pandas as pd
import pickle
from num_to_words import num_to_word
import requests

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

data = pd.read_csv('cleaned_data.csv')
pipe = pickle.load(open('RidgeModel.pkl','rb'))
locations = sorted(data['location'].unique())

def main():
    st.set_page_config(page_title="House Price Prediction", layout="wide", page_icon="🏠")

    # Header Section
    st.markdown(
        """
        <style>
            .header {
                position: relative;
                height: 600px;
                background-image: linear-gradient(to bottom, rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://plus.unsplash.com/premium_photo-1675324517011-24d2c741c22f?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
                background-size: cover;
                background-position: center;
                color: white;
                text-align: center;
                padding-top: 150px; /* Increase padding to add space */
                padding-bottom: 50px; /* Add some padding at the bottom */
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
                top: 40%;
                left: 0;
                width: 100%;
                height: 2px;
                background-color: #FFD700; /* Golden yellow */
                transform: translateY(-50%);
            }

            .main-section {
                background-color: #f9f9f9; /* Light gray */
                padding: 30px;
                border-radius: 20px;
                margin-bottom: 20px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Adding shadow for depth */
                color: black;
            }

            .footer {
                background-color: #333333; /* Dark gray */
                color: white;
                text-align: center;
                padding: 15px;
                width: 100%;
                font-size: 14px; /* Decrease font size */
                font-weight: normal; /* Decrease font weight */
            }

            .footer a {
                color: #FFD700; /* Golden yellow */
                text-decoration: none;
                font-weight: bold;
                margin: 0 10px;
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
            <p>Welcome to our app! </p>
            <p>Scroll down to predict house price</p>
        </div>
        """
    , unsafe_allow_html=True)

    # Main App Section
    st.markdown( """ <style> .main-section { padding: 20px;text-align:center } </style>"""
        "<h2 class='main-section'>House Features</h2>", unsafe_allow_html=True)

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

    # Footer Section
    st.markdown(
        """
        <div class="footer">
            <p>Developed by Priyanshu Naredi</p>
            <p>Find me on: <a href="https://github.com/PriyanshuNaredi" target="_blank">GitHub</a> | 
            <a href="https://linkedin.com/in/your_linkedin_username" target="_blank">LinkedIn</a></p>
        </div>
        """
    , unsafe_allow_html=True)

def predict(bhk,bath,sqft,location):
    input = pd.DataFrame([[location,sqft,bath,bhk]]
        ,columns=['location','total_sqft','bath','BHK'])
    prediction = pipe.predict(input)[0] * 1e5 # 1e5 -> 1 Lakh

    result = int(prediction)
    return result

main()
