
# Bibliotecas
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn import metrics

import pickle

# Banco de dados
diabetesDF = pd.read_csv('diabetes.csv')

# Pre-Processamento do modelo
dfTrain = diabetesDF[:650]
dfTest = diabetesDF[650:]

trainLabel = np.asarray(dfTrain['Outcome'])
trainData = np.asarray(dfTrain.drop('Outcome',1))
testLabel = np.asarray(dfTest['Outcome'])
testData = np.asarray(dfTest.drop('Outcome',1))

# Modelo - Regressao Logistica
diabetesCheck = LogisticRegression()
diabetesCheck.fit(trainData, trainLabel)

# Predicao
predictions=diabetesCheck.predict(testData)


# Avaliacao
accuracy = diabetesCheck.score(testData, testLabel)
print("accuracy = ", accuracy * 100, "%")


file = open('diabeteseModel.pkl', 'wb')
pickle.dump(diabetesCheck, file)
file.close()

