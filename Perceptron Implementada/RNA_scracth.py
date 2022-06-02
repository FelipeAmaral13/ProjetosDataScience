import numpy as np

class Neuronio:
    """
    Classe base para os nós da rede.

    Argumentos:

        "nodes_entrada": Uma lista de nós com arestas para este nó.
    """
    def __init__(self, nodes_entrada = []):
        """
        O construtor do nó (é executado quando o objeto é instanciado). 
        Define propriedades que podem ser usadas por todos os nós.
        """
        # Lista de nós com arestas para este nó.
        self.nodes_entrada = nodes_entrada
        
        # Lista de nós para os quais este nó gera saída.
        self.nodes_saida = []
        
        # O valor calculado por este nó. É definido executando o método forward().
        self.valor = None
        
        # Este objeto é um dicionário com pares chaves/valor entre {} 
        # As chaves (keys) são os inputs para este nó e o valores (values) são as paciais deste nó em relação ao input.
        self.gradientes = {}
        
        # Configuramos este nó como um nó de saída para todos os nós de entrada.
        for n in nodes_entrada:
            n.nodes_saida.append(self)

    def forward(self):
        """
        Todo o nó que usar essa classe como uma classe base, precisa definir seu próprio método "forward".
        """
        raise NotImplementedError

    def backward(self):
        """
        Todo o nó que usar essa classe como uma classe base, precisa definir seu próprio método "backward".
        """
        raise NotImplementedError



class Input(Neuronio):
    """
    Input genérico para a rede.
    """
    def __init__(self):
        # O construtor da classe base deve ser executado para configurar todas as propriedades aqui.
        #
        # A propriedade mais importante de Input é valor.
        # self.valor é definido na função topological_sort().
        Neuronio.__init__(self)

    def forward(self):
        # Nada a ser feito aqui.
        pass

    def backward(self):
        # Um nó de Input não possui entradas (pois ele já é a entrada) e assim o gradiente (derivada) é zero.
        # A palavra reservada "self", é referência para este objeto.
        self.gradientes = {self: 0}
        
        # Pesos e bias podem ser inputs, assim precisamos somar o gradiente de outros gradientes de saída
        for n in self.nodes_saida:
            self.gradientes[self] += n.gradientes[self]
            

class Linear(Neuronio):
    """
    Representa um nó que realiza transformação linear.
    """
    def __init__(self, X, W, b):
        # O construtor da classe base (nó). 
        # Pesos e bias são tratados como nós de entrada (nodes_entrada).
        Neuronio.__init__(self, [X, W, b])

    def forward(self):
        """
        Executa a matemática por trás da transformação linear.
        """
        X = self.nodes_entrada[0].valor
        W = self.nodes_entrada[1].valor
        b = self.nodes_entrada[2].valor
        self.valor = np.dot(X, W) + b

    def backward(self):
        """
        Calcula o gradiente com base nos valores de saída.
        """
        # Inicializa um parcial para cada um dos nodes_entrada.
        self.gradientes = {n: np.zeros_like(n.valor) for n in self.nodes_entrada}
        
        # Ciclo através dos outputs. 
        # O gradiente mudará dependendo de cada output, assim os gradientes são somados sobre todos os outputs.
        for n in self.nodes_saida:
            
            # Obtendo parcial da perda em relação a este nó.
            grad_cost = n.gradientes[self]
            
            # Definindo o parcial da perda em relação às entradas deste nó.
            self.gradientes[self.nodes_entrada[0]] += np.dot(grad_cost, self.nodes_entrada[1].valor.T)
            
            # Definindo o parcial da perda em relação aos pesos deste nó.
            self.gradientes[self.nodes_entrada[1]] += np.dot(self.nodes_entrada[0].valor.T, grad_cost)
            
            # Definindo o parcial da perda em relação ao bias deste nó.
            self.gradientes[self.nodes_entrada[2]] += np.sum(grad_cost, axis = 0, keepdims = False)


class Sigmoid(Neuronio):
    """
    Representa o nó da função de ativação Sigmoid.
    """
    def __init__(self, node):
        # O construtor da classe base.
        Neuronio.__init__(self, [node])

    def _sigmoid(self, x):
        """
        Este método é separado do `forward` porque ele também será usado com "backward".

        `x`: Um array Numpy.
        """
        return 1. / (1. + np.exp(-x))

    def forward(self):
        """
        Executa a função _sigmoid e define a variável self.valor
        """
        input_value = self.nodes_entrada[0].valor
        self.valor = self._sigmoid(input_value)

    def backward(self):
        """
        Calcula o gradiente usando a derivada da função sigmoid 
        
        O método backward da classe Sigmoid, soma as derivadas (é uma derivada normal quando há apenas uma variável) 
        em relação à única entrada sobre todos os nós de saída.
        """
        
        # Inicializa os gradientes com zero.
        self.gradientes = {n: np.zeros_like(n.valor) for n in self.nodes_entrada}
        
        # Soma a parcial em relação ao input sobre todos os outputs.
        for n in self.nodes_saida:
            grad_cost = n.gradientes[self]
            sigmoid = self.valor
            self.gradientes[self.nodes_entrada[0]] += sigmoid * (1 - sigmoid) * grad_cost


class MSE(Neuronio):
    def __init__(self, y, a):
        """
        Função de custo para calcular o erro médio quadrático.
        Deve ser usado como último nó da rede.
        """
        # Chamada ao construtor da classe base.
        Neuronio.__init__(self, [y, a])

    def forward(self):
        """
        Calcula o erro médio ao quadrado.
        """
        # Fazemos o reshape para evitar possíveis problemas nas operações de matrizes/vetores 
        #
        # Convertendo os 2 arrays (3,1) garantimos que o resultado será (3,1) e, assim, 
        # teremos uma subtração elementwise.
        y = self.nodes_entrada[0].valor.reshape(-1, 1)
        a = self.nodes_entrada[1].valor.reshape(-1, 1)

        self.m = self.nodes_entrada[0].valor.shape[0]
        
        # Salva o output computado para o backward pass.
        self.diff = y - a
        self.valor = np.mean(self.diff**2)

    def backward(self):
        """
        Calcula o gradiente do custo.
        """
        self.gradientes[self.nodes_entrada[0]] = (2 / self.m) * self.diff
        self.gradientes[self.nodes_entrada[1]] = (-2 / self.m) * self.diff


def topological_sort(feed_dict):
    """
    Classifica os nós em ordem topológica usando o Algoritmo de Kahn.

    `Feed_dict`: um dicionário em que a chave é um nó `Input` e o valor é o respectivo feed de valor para esse nó.

    Retorna uma lista de nós ordenados.
    """

    input_nodes = [n for n in feed_dict.keys()]

    G = {}
    nodes = [n for n in input_nodes]
    while len(nodes) > 0:
        n = nodes.pop(0)
        if n not in G:
            G[n] = {'in': set(), 'out': set()}
        for m in n.nodes_saida:
            if m not in G:
                G[m] = {'in': set(), 'out': set()}
            G[n]['out'].add(m)
            G[m]['in'].add(n)
            nodes.append(m)

    L = []
    S = set(input_nodes)
    while len(S) > 0:
        n = S.pop()

        if isinstance(n, Input):
            n.valor = feed_dict[n]

        L.append(n)
        for m in n.nodes_saida:
            G[n]['out'].remove(m)
            G[m]['in'].remove(n)
            if len(G[m]['in']) == 0:
                S.add(m)
    return L


def forward_and_backward(graph):
    """
    Executa uma passagem para a frente e uma passagem para trás através de uma lista de nós ordenados.

     Argumentos:

         `Graph`: O resultado de `topological_sort`.
    """
    # Forward pass
    for n in graph:
        n.forward()

    # Backward pass
    # O valor negativo no slice permite fazer uma cópia da mesma lista na ordem inversa.
    for n in graph[::-1]:
        n.backward()


def sgd_update(params, learning_rate = 1e-2):
    """
    Atualiza o valor de cada parâmetro treinável com o SGD.

    Argumentos:

     `Trainables`: uma lista de nós `Input` que representam pesos / bias.
     `Learning_rate`: a taxa de aprendizado.
    """
    # Executa o SGD
    #
    # Loop sobre todos os parâmetros
    for t in params:
        # Alterar o valor do parâmetro, subtraindo a taxa de aprendizado 
        # multiplicado pela parte do custo em relação a esse parâmetro
        partial = t.gradientes[t]
        t.valor -= learning_rate * partial