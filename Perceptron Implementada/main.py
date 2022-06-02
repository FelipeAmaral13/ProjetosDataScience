import numpy as np
from sklearn.datasets import load_boston
from sklearn.utils import shuffle, resample
from RNA_scracth import Input, Linear, Sigmoid, MSE, topological_sort, forward_and_backward, sgd_update

# Carrega os dados
data = load_boston()


# Variáveis de entrada e saída para treinamento supervisionado
X_ = data['data'][0:int(np.floor(len(data.data)*0.7))]
y_ = data['target'][0:int(np.floor(len(data.target)*0.7))]

X_test = data['data'][int(np.floor(len(data.data)*0.7)):]

# Normaliza os dados
X_ = (X_ - np.mean(X_, axis = 0)) / np.std(X_, axis = 0)

# Número de features e número de neurônios
n_features = X_.shape[1]
n_hidden = 10

# Define valores randômicos para inicializar pesos e bias
W1_ = np.random.randn(n_features, n_hidden)
b1_ = np.zeros(n_hidden)
W2_ = np.random.randn(n_hidden, 1)
b2_ = np.zeros(1)

# Rede Neural
X, y = Input(), Input()
W1, b1 = Input(), Input()
W2, b2 = Input(), Input()

l1 = Linear(X, W1, b1)
s1 = Sigmoid(l1)
l2 = Linear(s1, W2, b2)
cost = MSE(y, l2)

# Define o feed_dict
feed_dict = {
    X: X_,
    y: y_,
    W1: W1_,
    b1: b1_,
    W2: W2_,
    b2: b2_
}

# Número de epochs (altere esse valor para ver as mudanças no resultado)
epochs = 10

# Número total de exemplos
m = X_.shape[0]

# Batch size
batch_size = 11
steps_per_epoch = m // batch_size

# Define o grafo computacional
graph = topological_sort(feed_dict)

# Valores que serão aprendidos pela rede
params = [W1, b1, W2, b2]

# Número total de exemplos
print("Número Total de Exemplos = {}".format(m))

# Treinamento do modelo
for i in range(epochs):
    loss = 0
    for j in range(steps_per_epoch):
        
        # Passo 1 - Testa aleatoriamente um lote de exemplos
        X_batch, y_batch = resample(X_, y_, n_samples = batch_size)

        # Reset dos valores de X e y 
        X.valor = X_batch
        y.valor = y_batch

        # Passo 2 - Forward e Backpropagation
        forward_and_backward(graph)

        # Passo 3 - Otimização por SGD
        sgd_update(params)

        loss += graph[-1].valor

    print("Epoch: {}, Custo: {:.3f}".format(i+1, loss/steps_per_epoch))