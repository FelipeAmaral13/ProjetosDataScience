import streamlit as st
import pickle
import numpy as np
import os


model = pickle.load(open(os.path.join(os.getcwd(), 'random_forest_regression_model.pkl'),'rb'))

def predict_price(Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, no_year):
    input=np.array([[Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, no_year]]).astype(np.float64)
    prediction=model.predict(input)
    return float(prediction)

def main():
    st.title("Car Price Prediction")
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">
    Used Car Price Prediction ML App </h2>
    </div>
    """

    st.markdown(html_temp, unsafe_allow_html=True)
    Present_Price = st.text_input("What is the current market value of the car?","In Lakhs")
    Kms_Driven = st.text_input("How much kilometers the car has driven?","Type Here")
    Fuel_Type = st.text_input("What is the type of fuel used?","Please Type 0 for CNG/ 1 for Diesel/ 2 for Petrol")
    Seller_Type = st.text_input("What is the type of seller?","Please Type 0 for Dealer/ 1 for Individual")
    Transmission = st.text_input("What is the type of Transmission?","Please type 0 for Automatic/ 1 for manual")
    Owner = st.text_input("What is the no. of owners?", "Please type 0/1/3")
    no_year = st.text_input("How many years old?","Type here")

    if st.button("Predict"):
            output=predict_price(Present_Price, Kms_Driven,Fuel_Type, Seller_Type,  Transmission, Owner, no_year)
            st.success('The selling price of this vehicle will be approximately {} lakhs'.format(round(output, 2)))

if __name__ == '__main__':
    main()