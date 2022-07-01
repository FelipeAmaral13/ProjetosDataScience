import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error,\
    median_absolute_error
import pickle
import numpy as np

# df = pd.read_csv(os.path.join('data', 'headbrain.csv'), sep=',')
df = pd.read_csv(os.path.join('data', 'dataset.csv'))


# Preparando os dados
X = df.iloc[:, :-1].values
y = df.iloc[:, 1].values

X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=0)
X_treino = X_treino.reshape(-1, 1).astype(np.float32)


clf = LinearRegression()
regressao = clf.fit(X_treino, y_treino)

print("\n")
print('B1 (coef_) :', clf.coef_)
print('B0 (intercept_) :', clf.intercept_)


regression_line = clf.coef_ * X + clf.intercept_
plt.scatter(X, y)
plt.title('Invetimento x Retorno')
plt.xlabel('Investimento')
plt.ylabel('Retorno Previsto')
plt.plot(X, regression_line, color='red')
plt.show()


y_pred = clf.predict(X_teste)
# predict = clf.predict(X_Reshaped)

print(f'Slope = {clf.coef_[0]} e Intercept = {clf.intercept_}')
print(f'MAE - {mean_absolute_error(y_teste, y_pred)}')
print(f'MSE - {mean_squared_error(y_teste, y_pred)}')
print(f'MedAE - {median_absolute_error(y_teste, y_pred)}')
print(f'Coef. de Determinacao (R2): {r2_score(y_teste, y_pred)}')

Pkl_Filename = os.path.join('model', 'Pickle_RL_Model.pkl')

with open(Pkl_Filename, 'wb') as file:
    pickle.dump(clf, file)
