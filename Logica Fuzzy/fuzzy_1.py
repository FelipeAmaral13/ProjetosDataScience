import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.mlab as mlb
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
import datetime as dt

# Eixo das abscissas para as func. pertinencia
preco = ctl.Antecedent(np.arange(17, 30,1), 'preço')
vol = ctl.Antecedent(np.arange(0, 2e8,1e5), 'volume')
dec = ctl.Consequent(np.arange(0, 2e8,1e5), 'decisao')


# Func. de pertinencia para preços
preco['barato'] = fuzz.gaussmf(preco.universe, 19, 2)
preco['ideal'] = fuzz.gaussmf(preco.universe, 26, 2)
preco['caro'] = fuzz.gaussmf(preco.universe, 29, 2)
preco.view()
plt.text(x=18, y=0.8, s='barato', fontsize=8, weight='bold')
plt.text(x=22, y=0.8, s='ideal', fontsize=8, weight='bold')
plt.text(x=28, y=0.8, s='caro', fontsize=8, weight='bold')

# Func. de pertinencia para volumes
vol['baixo'] = fuzz.gaussmf(vol.universe, 0.4e8, 6e7)
vol['ideal'] = fuzz.gaussmf(vol.universe, 0.6e8, 2e7)
vol['alto'] = fuzz.gaussmf(vol.universe, 1e8, 3e7)
vol.view()
plt.text(x=0.25e8, y=0.8, s='baixo', fontsize=8, weight='bold')
plt.text(x=0.5e8, y=0.8, s='ideal', fontsize=8, weight='bold')
plt.text(x=1e8, y=0.8, s='alto', fontsize=8, weight='bold')

# Func. de pertinencia para decisao final
dec['comprar'] = fuzz.gaussmf(dec.universe, 0.4e8, 6e7)
dec['manter'] = fuzz.gaussmf(dec.universe, 0.6e8, 2e7)
dec['vender'] = fuzz.gaussmf(dec.universe, 1e8, 3e7)
dec.view()
plt.text(x=0.25e8, y=0.8, s='comprar', fontsize=8, weight='bold')
plt.text(x=0.5e8, y=0.8, s='manter', fontsize=8, weight='bold')
plt.text(x=1e8, y=0.8, s='vender', fontsize=8, weight='bold')

# Regras da Logica Fuzzy
regra1 = ctl.Rule(preco['barato'] & vol['baixo'], dec['comprar'])
regra2 = ctl.Rule(preco['barato'] & vol['alto'], dec['comprar'])
regra3 = ctl.Rule(preco['ideal'] & vol['baixo'], dec['comprar'])
regra4 = ctl.Rule(preco['ideal'] & vol['ideal'], dec['manter'])
regra5 = ctl.Rule(preco['ideal'] & vol['alto'], dec['vender'])
regra6 = ctl.Rule(preco['caro'] & vol['alto'], dec['vender'])

# Sistema de criacao de controle/simulacao
decisao_ctl = ctl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6])
decisao = ctl.ControlSystemSimulation(decisao_ctl)

# Funcao de calculo para defuzzificacao
def IndFzy(entrada):
    decisao.input['preço']=entrada[0]
    decisao.input['volume']=entrada[1]

    decisao.compute()
    return (decisao.output['decisao'])

# Decisao final

inicio = dt.datetime(2021,1,1)
fim = dt.datetime(2021,9,9)

df = web.DataReader('PETR4.SA', 'yahoo', inicio, fim)
mval = np.zeros((len(df), 3))

for i in range(len(df)):
    res1 = IndFzy([df['Close'].values[i], df['Volume'].values[i]])
    j=0
    for t in dec.terms:
        s = np.interp(res1, dec.universe, dec[t].mf)
        mval[i,j]=s
        j=j+1

mval = pd.DataFrame(mval, columns=['comprar', 'manter', 'vender'])
dec_fuzzy = mval.idxmax(axis=1)
print(dec_fuzzy)

dec.view(sim=decisao)
plt.text(x=0.25e8, y=0.8, s='comprar', fontsize=12, weight='bold')
plt.text(x=0.5e8, y=0.8, s='manter', fontsize=12, weight='bold')
plt.text(x=1e8, y=0.8, s='vender', fontsize=12, weight='bold')

figura = plt.figure()
ax1 = plt.subplot(111)
plt.title('IBOV ')

ax1.plot(df.index, df['Close'], '--k')
ax1.set_ylabel('BOV', fontsize=2, weight='bold')
for i in range(len(dec_fuzzy)):
    ax1.text(x=df.index[i], y=df['Close'].values[i], s=str(dec_fuzzy[i]),
    fontsize=12, color='black', weight='bold')

ax2 = ax1.twinx()
ax2.plot(df.index, df['Volume'], color='black')
ax2.set_ylabel('Volume', fontsize=2, weight='bold')
plt.show()