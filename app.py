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
        
    


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score

data = pd.read_csv('cleaned_data.csv')
pipe = pickle.load(open('RidgeModel.pkl','rb'))
locations = sorted(data['location'].unique())

def main():
    style = """<div style='background-color:pink; padding:12px'>
              <h1 style='color:black'>House Price Prediction App</h1>
       </div>"""
    st.markdown(style, unsafe_allow_html=True)
    left, right = st.columns((2,2))
    total_bedrooms = left.number_input('BHK',
                                       step=1.0, format='%.1f', value=2.0)
    total_bathrooms = right.number_input('Bathrooms',
                                    step=1.0, format='%.1f', value=2.0)
    sqft = left.number_input('Sq Ft',  step=1.0,
                                   format='%.1f',value=1500.0)
    location = right.selectbox('location',options=locations)
    button = st.button('Predict')
    
    # if button is pressed
    if button:
        
        # make prediction
        result = predict(total_bedrooms,total_bathrooms,sqft,location)
        total = str(num_to_word(result, lang='en')).replace(',',' ').title()
        st.success(f'The value of the house is ₹{result}  {total}')
        lat_long = get_lat_long(location)
        st.map(lat_long,zoom=16)
        

def predict(bhk,bath,sqft,location):

    input = pd.DataFrame([[location,sqft,bath,bhk]]
        ,columns=['location','total_sqft','bath','BHK'])
    prediction = pipe.predict(input)[0] * 1e5 # 1e5 -> 1 Lakh
    
    result = int(prediction)
    return result

main()