#### Bibliotecas ####
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt
import os

#### Data Science ####
# Banco de dados 
df = pd.read_csv( filepath_or_buffer='https://raw.githubusercontent.com/insaid2018/Term-2/master/car%20data.csv')

#### Info Basicas ####
df.shape
df.head()
df.describe()
df.info()


#### Pre-Processsamento ####
final_dataset=df[['Year','Selling_Price','Present_Price','Kms_Driven','Fuel_Type','Seller_Type','Transmission','Owner']]

# Label encoding
le = LabelEncoder()
final = final_dataset[['Fuel_Type', 'Seller_Type','Transmission']].apply(le.fit_transform)
final_dataset.drop(['Fuel_Type', 'Seller_Type', 'Transmission'], inplace=True,axis=1)
final_dataset.head()


# Feature Engineering

# Ano Base
final_dataset['Current Year']=2021

# Coluna Diferenca do ano atual com o ano do carro
final_dataset['no_year'] = final_dataset['Current Year']- final_dataset['Year']
final_dataset.drop(['Year'],axis=1,inplace=True)

# Valores Gasolina, Venda e possui Transmissao
Fuel = final['Fuel_Type']
Seller = final['Seller_Type']
Transmission = final['Transmission']

# Agrupando o dataset
final_dataset=final_dataset.join(Fuel)
final_dataset=final_dataset.join(Seller)
final_dataset=final_dataset.join(Transmission)
final_dataset=final_dataset.drop(['Current Year'],axis=1)
final_dataset.head()

#### Modelo ####

# Features
X=final_dataset.iloc[:,1:]
# Label
y=final_dataset.iloc[:,0]

# Divisao em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Numero de arvores randomicas - SearchCV
n_estimators = [int(x) for x in np.linspace(start = 100, 
               stop = 1200, num = 12)]

# Numero de features a ser considerado cada split split
max_features = ['auto', 'sqrt']

# Maximo numero de lvls na arvore
max_depth = [int(x) for x in np.linspace(5, 30, num = 6)]

# Minimo numero de amostras requisitada para o split dos nos
min_samples_split = [2, 5, 10, 15, 100]

#  Minimo numero de amostras requisitad em cada no das folhas
min_samples_leaf = [1, 2, 5, 10]

# Grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}
print(random_grid)

rf = RandomForestRegressor()
rf_random = RandomizedSearchCV(estimator = rf, 
                               param_distributions = random_grid,
                               scoring='neg_mean_squared_error', 
                               n_iter = 10, 
                               cv = 5,
                               verbose=2, 
                               random_state=42,
                               n_jobs = -1)
rf_random.fit(X_train,y_train)

# Melhores parametros
rf_random.best_params_

### Validação do modelo ###
predictions=rf_random.predict(X_test)

print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:',np.sqrt(metrics.mean_squared_error(y_test, predictions)))

plt.scatter(y_test,predictions)
plt.show()

# Salvar o modelo
file = open(os.path.join(os.getcwd(), 'random_forest_regression_model.pkl'), 'wb')
pickle.dump(rf_random, file)
file.close()

