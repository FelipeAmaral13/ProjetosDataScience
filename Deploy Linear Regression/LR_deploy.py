import streamlit as st
import pickle
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error,\
    median_absolute_error

st.set_option('deprecation.showPyplotGlobalUse', False)


model = pickle.load(
    open(os.path.join(os.getcwd(), 'model', 'Pickle_RL_Model.pkl'), 'rb'))


def predict_RL(investimento: int) -> float:

    input = np.array([[investimento]]).astype(np.float64)
    input = input.reshape(-1, 1)
    prediction = model.predict(input)
    ponto = (prediction - model.intercept_)/model.coef_[0]

    return float(prediction), ponto


def main():
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">
    Regressao Linear ML App </h2>
    </div>
    """

    st.markdown(html_temp, unsafe_allow_html=True)
    TamCabeca = st.text_input("Qual o valor do investimento?")

    if st.button("Predict"):
        prediction, ponto = predict_RL(TamCabeca)
        st.success(f'O retorno é aproximado é de: {round(prediction, 2)}')
        st.text(f'Slope = {model.coef_[0]} e Intercept = {model.intercept_}')

        df = pd.read_csv(os.path.join('data', 'dataset.csv'))

        X = df.iloc[:, :-1].values
        y = df.iloc[:, 1].values

        predict = model.predict(X.reshape(-1, 1))

        plt.figure(figsize=(16, 8), dpi=100)
        plt.scatter(X, y, color='gray')
        plt.plot(X, predict, color='red', linewidth=2)
        plt.annotate(
            "Pt Predict", (ponto[0]+10, prediction-2), fontsize=17)
        plt.scatter(ponto[0], prediction, color='blue')
        plt.xlabel('Investimento')
        plt.ylabel('Retorno Previsto')
        plt.show()
        st.pyplot()


if __name__ == '__main__':
    main()
