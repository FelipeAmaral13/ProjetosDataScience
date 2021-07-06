import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('framingham.csv')

# Analise basica
df.info()

# Proporcao de dados faltantes
dados_faltantes = df.isnull().sum() / df.shape[0] * 100.00

## ---- Pre-processamento -> Dados Faltantes
# Col: Education, cigsPerDay, BPMeds, totChol, BMI, heartRate, glucose
df['education'].fillna(df['education'].mode()[0], inplace=True)
df['cigsPerDay'].fillna(df['cigsPerDay'].mode()[0], inplace=True)
df['BPMeds'].fillna(df['BPMeds'].mode()[0], inplace=True)

df['totChol'].fillna(df['totChol'].mean(), inplace=True)
df['BMI'].fillna(df['BMI'].mean(), inplace=True)
df['heartRate'].fillna(df['BMI'].mode()[0], inplace=True)
df['glucose'].fillna(df['glucose'].mode()[0], inplace=True)


## ---- Pre-processamento -> Outliers
df.describe()


fig = make_subplots(
    rows=4, cols=4, subplot_titles=('male', 'age', 'education', 'currentSmoker', 'cigsPerDay', 'BPMeds',
       'prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol', 'sysBP',
       'diaBP', 'BMI', 'heartRate', 'glucose', 'TenYearCHD')
)

# Add traces - 1
fig.add_trace(go.Box(y=df['male']), row=1, col=1)
fig.add_trace(go.Box(y=df['age']), row=1, col=2)
fig.add_trace(go.Box(y=df['education']), row=1, col=3)
fig.add_trace(go.Box(y=df['currentSmoker']), row=1, col=4)

# Add traces - 2
fig.add_trace(go.Box(y=df['cigsPerDay']), row=2, col=1)
fig.add_trace(go.Box(y=df['BPMeds']), row=2, col=2)
fig.add_trace(go.Box(y=df['prevalentStroke']), row=2, col=3)
fig.add_trace(go.Box(y=df['prevalentHyp']), row=2, col=4)

# Add traces - 3
fig.add_trace(go.Box(y=df['diabetes']), row=3, col=1)
fig.add_trace(go.Box(y=df['totChol']), row=3, col=2)
fig.add_trace(go.Box(y=df['sysBP']), row=3, col=3)
fig.add_trace(go.Box(y=df['diaBP']), row=3, col=4)

# Add traces - 4
fig.add_trace(go.Box(y=df['BMI']), row=4, col=1)
fig.add_trace(go.Box(y=df['heartRate']), row=4, col=2)
fig.add_trace(go.Box(y=df['glucose']), row=4, col=3)
fig.add_trace(go.Box(y=df['TenYearCHD']), row=4, col=4)

fig.update_layout(title_text="Boxplot - Detecção de Outliers", height=700)

fig.show()


# Analise e Exploracao de Dados - EAD

# Distribuicao da Idade
fig = px.histogram(df, x='age', title='Rating distribution', )
fig.show()



# Trocar nome das amostras
df['male'] = np.where(df['male']==1, 'Masc', 'Fem')
df['prevalentHyp'] = np.where(df['prevalentHyp']==1, 'Hipertenso', 'NAO - Hipertenso')
df['diabetes'] = np.where(df['diabetes']==1, 'Diabetico', 'NAO - Diabetico')
df['prevalentStroke'] = np.where(df['prevalentStroke']==1, 'AVC', 'NAO - AVC')



# Qual a contagem de Sexo, Hipertensos, Diabeticos, Tiveram AVC
fig = go.Figure(data=[go.Bar(x=df['male'], y=df['male'].value_counts(), text=df['male'].value_counts(), textposition='auto')])
fig.show()





## Correlacao entre os dados
sns.heatmap(df.corr(), annot = True, cmap = 'viridis')
plt.show()

### Enconders

from sklearn.preprocessing import LabelEncoder

labelencoder = LabelEncoder()

df['male'] = labelencoder.fit_transform(df['male'])
df['prevalentHyp'] = labelencoder.fit_transform(df['prevalentHyp'])
df['diabetes'] = labelencoder.fit_transform(df['diabetes'])
df['prevalentStroke'] = labelencoder.fit_transform(df['prevalentStroke'])




### ------------ Modelo Logistic Regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix


x = df.drop('TenYearCHD',axis='columns')
y = df['TenYearCHD']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=10)


model = LogisticRegression(max_iter=5000)
model.fit(x_train,y_train)

predictions = model.predict(x_test)

### ------------ Metrificacao

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from sklearn.model_selection import cross_val_score

print(classification_report(y_test,predictions))
cm = confusion_matrix(y_test,predictions)

sns.heatmap(cm, annot=True)
plt.show()

print('Score da acc do Modelo: {0:0.4f}'. format(accuracy_score(y_test, predictions)))


score=cross_val_score(LogisticRegression(max_iter=5000),df.drop('TenYearCHD',axis=1),df['TenYearCHD'],cv=10)
print(f"Score depois do k-fold cross validation: {score.mean()}")

## -------------------- Melhoria do Modelo
from sklearn.model_selection import GridSearchCV
parameters = [{'C':[1, 10, 100, 1000]},
              {'solver':['newton-cg', 'lbfgs', 'sag', 'saga']},
              {'max_iter': [500, 5000]}]

grid_search = GridSearchCV(estimator = model,  
                           param_grid = parameters,
                           scoring = 'accuracy',
                           cv = 5,
                           verbose=0, n_jobs=-1)

grid_search.fit(x_train, y_train)

print('GridSearch CV best score: {:.4f}\n'.format(grid_search.best_score_))
print(f'Melhores Paremetros: {grid_search.best_params_}')