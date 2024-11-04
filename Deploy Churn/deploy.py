# Projeto 2 - Prevendo o Churn de Alunos com RandomForest
# Deploy do Modelo


# Imports
import joblib
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Carregar o modelo e o scaler
modelo = joblib.load('calibrated_cat_isotonic.pkl')
scaler = joblib.load('padronizador.pkl')

# Função para pré-processar os dados de entrada
# As colunas devem ser exatamente as mesmas usadas durante o treinamento
# Função para pré-processar os dados de entrada
def preprocess_input(idade, 
                     HorasEstudoSemanal, 
                     satisfacao_curso, 
                     Mensalidade, 
                     TipoCurso_Online, 
                     TipoCurso_Presencial, 
                     TipoCurso_Semi_Presencial, 
                     DuracaoCurso_Anual, 
                     DuracaoCurso_Medio,
                     DuracaoCurso_Semestral):
    
    # Dataframe com as colunas organizadas na ordem correta
    data = pd.DataFrame({
        'Idade': [idade],
        'HorasEstudoSemanal': [HorasEstudoSemanal],
        'SatisfacaoCurso': [satisfacao_curso],
        'Mensalidade': [Mensalidade],
        'TipoCurso_Online': [TipoCurso_Online],
        'TipoCurso_Presencial': [TipoCurso_Presencial],
        'TipoCurso_Semi-Presencial': [TipoCurso_Semi_Presencial],
        'DuracaoCurso_Anual': [DuracaoCurso_Anual],
        'DuracaoCurso_Medio': [DuracaoCurso_Medio],
        'DuracaoCurso_Semestral': [DuracaoCurso_Semestral]
    })[[
        'Idade', 
        'HorasEstudoSemanal', 
        'SatisfacaoCurso', 
        'Mensalidade', 
        'TipoCurso_Online', 
        'TipoCurso_Presencial', 
        'TipoCurso_Semi-Presencial', 
        'DuracaoCurso_Anual', 
        'DuracaoCurso_Medio', 
        'DuracaoCurso_Semestral'
    ]]

    # Aplicando padronização
    data = scaler.transform(data)

    return data




# Função para fazer previsões
def predict(data):
    prediction = modelo.predict(data)
    return prediction

# Interface do Streamlit
st.title("Preditor de Churn com RandomForest")

# Criação de campos para entrada de dados
idade = st.number_input('Idade', min_value=18, max_value=100, value=30)
HorasEstudoSemanal = st.number_input('Horas de Estudo Semanal', min_value=0, max_value=200, value=50)
satisfacao_curso = st.number_input('Satisfação com o Curso', min_value=1, max_value=5, value=3)
Mensalidade = st.number_input('Mensalidade', min_value=0.0, max_value=500.0, value=100.0)
plano = st.selectbox('Tipo de Curso', ['Online', 'Presencial', 'Semi-Presencial'])
duracao_curso = st.selectbox('Duração do Curso', ['Anual', 'Medio', 'Semestral'])

# Botão para realizar previsões
if st.button('Prever Churn'):
    # Ajusta as variáveis pré-processadas com One-Hot Encoding
    TipoCurso_Online = 1 if plano == 'Online' else 0
    TipoCurso_Presencial = 1 if plano == 'Presencial' else 0
    TipoCurso_Semi_Presencial = 1 if plano == 'Semi-Presencial' else 0
    DuracaoCurso_Anual = 1 if duracao_curso == 'Anual' else 0
    DuracaoCurso_Medio = 1 if duracao_curso == 'Medio' else 0
    DuracaoCurso_Semestral = 1 if duracao_curso == 'Semestral' else 0

    # Executa a função de pré-processamento de dados
    input_data = preprocess_input(idade, 
                                  HorasEstudoSemanal, 
                                  satisfacao_curso, 
                                  Mensalidade, 
                                  TipoCurso_Online, 
                                  TipoCurso_Presencial, 
                                  TipoCurso_Semi_Presencial, 
                                  DuracaoCurso_Anual, 
                                  DuracaoCurso_Medio, 
                                  DuracaoCurso_Semestral)

    # Faz a previsão com o modelo
    prediction = predict(input_data)

    st.write('Churn Previsto:', 'Sim' if prediction[0] == 1 else 'Não')
