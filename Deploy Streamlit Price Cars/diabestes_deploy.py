from logging import PercentStyle
import streamlit as st
import pickle
import numpy as np
import os


model = pickle.load(open(os.path.join(os.getcwd(), 'diabeteseModel.pkl'),'rb'))

def predict_price( Pregnancies,  Glucose,  BloodPressure,  SkinThickness,  Insulin,   BMI,  DiabetesPedigreeFunction,  Age):
    input=np.array([[ Pregnancies,  Glucose,  BloodPressure,  SkinThickness,  Insulin,   BMI,  DiabetesPedigreeFunction,  Age]]).astype(np.float64)
    prediction=model.predict(input)
    return float(prediction)

def main():
    st.title("Diabetes Prediction ")
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">
    Diabetes Prediction ML App </h2>
    </div>
    """

    st.markdown(html_temp, unsafe_allow_html=True)
    gravides = st.text_input("Numero de vezes que engravidou?")
    glicose = st.text_input("Concentracao de glicose?")
    pressao = st.text_input("Pressao Arterial?")
    esp_pele = st.text_input("Espessura da Pele?")
    insulina = st.text_input("Insulina?")
    imb = st.text_input("IMB?")
    ped_dia = st.text_input("Função de pedigree de diabetes?")
    idade = st.text_input("Idade?")

    if st.button("Predict"):
            output=predict_price(gravides, glicose,pressao, esp_pele,  insulina, imb, ped_dia, idade)
            st.success('{}'.format(round(output, 2)))

if __name__ == '__main__':
    main()