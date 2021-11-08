import numpy as np 
import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


heart_data  = pd.read_csv("heart.csv")


### Pre-Processamento
y = heart_data['HeartDisease']
X = heart_data.drop(['HeartDisease'], axis=1)


X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2)


# Amostras Categoricas
s = (heart_data.dtypes == 'object')
object_cols = list(s[s].index)


label_X_train = X_train.copy()
label_X_test = X_test.copy()

# OridnalEnconder
ordinal_encoder = OrdinalEncoder()
label_X_train[object_cols] = ordinal_encoder.fit_transform(X_train[object_cols])
label_X_test[object_cols] = ordinal_encoder.transform(label_X_test[object_cols])


### Modelo - Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=0)
model.fit(label_X_train, y_train)

# Predicao
preds = model.predict(label_X_test)

# Avaliacao
mean_absolute_error(y_test, preds)


def optimise_forest_param(X_train, X_valid, y_train, y_valid,n_estimators=100, max_depth=None, max_features="auto" ):
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=0, max_depth=max_depth, max_features=max_features, bootstrap=False)
    model.fit(X_train, y_train)
    preds = model.predict(X_valid)
    return mean_absolute_error(y_valid, preds)

## Encontrar melhor n_estimator
n_estimator_value = []
n_estimator_mae = []

for i in range(1, 50, 1):
    n_estimator_mae.append(optimise_forest_param(label_X_train, label_X_test, y_train, y_test, i))
    n_estimator_value.append(i)
n_estimator_dict = dict(zip(n_estimator_value,n_estimator_mae ))
print("O valor MAE mínimo corresponde a n_estimator = ", min(n_estimator_dict, key=n_estimator_dict.get))
optimal_nestimator= min(n_estimator_dict, key=n_estimator_dict.get)



## Encontrar o melhor max_depth
max_depth_value = []
max_depth_mae = []

for i in range(1, 50, 1):
    max_depth_mae.append(optimise_forest_param(label_X_train, label_X_test, y_train, y_test, optimal_nestimator, i))
    max_depth_value.append(i)
max_depth_dict = dict(zip(max_depth_value,max_depth_mae ))
print("O valor MAE mínimo corresponde a max_depth = ", min(max_depth_dict, key=max_depth_dict.get))
optimal_max_depth= min(max_depth_dict, key=max_depth_dict.get)


def run_final_model(X_train, X_valid, y_train, y_valid):
    model = RandomForestRegressor(n_estimators=optimal_nestimator, random_state=0, max_depth = optimal_max_depth)
    modelo = model.fit(X_train, y_train)
    preds = model.predict(X_valid)
    return modelo, mean_absolute_error(y_valid, preds)

model, mae = run_final_model(label_X_train, label_X_test, y_train, y_test)
print("Acuracia Modelo = ", 1-mae)


### Salvar o Modelo
import pickle

with open('modelo.pkl', 'wb') as file:
    pickle.dump(model, file)


### testar o modelo salvo
with open('modelo.pkl', 'rb') as file:
    rf = pickle.load(file)

label_X_train.columns

rf.predict(np.array(label_X_train.iloc[9]).reshape(1, -1))