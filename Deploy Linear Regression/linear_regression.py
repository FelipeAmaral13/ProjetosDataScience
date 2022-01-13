import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pickle
import numpy as np

df = pd.read_csv(os.path.join('data', 'headbrain.csv'), sep=',')

X = df['HeadSize'].values
y = df['BrainWeight'].values

clf = LinearRegression()
X_Reshaped = X.reshape((-1, 1))
regressao = clf.fit(X_Reshaped, y)

predict = clf.predict(X_Reshaped)

print(f'Slope = {clf.coef_[0]} e Intercept = {clf.intercept_}')
print(f'Coef. de Determinacao (R2): {r2_score(y, predict)}')

y_teste = clf.predict(np.array(3741).reshape(-1, 1))
# y = b0 + b1x -> y-b0 = b1x -> y-b0/b1 = x
ponto = (y_teste - clf.intercept_)/clf.coef_[0]

plt.figure(figsize=(16, 8), dpi=100)
plt.scatter(X, y, color='gray')
plt.plot(X, predict, color='red', linewidth=2)
plt.scatter(ponto[0], y_teste, color='blue')
plt.xlabel('Head Size(cm^3')
plt.ylabel('Brain Weight(grams)')
plt.show()


Pkl_Filename = os.path.join('model', 'Pickle_RL_Model.pkl')

with open(Pkl_Filename, 'wb') as file:
    pickle.dump(clf, file)
