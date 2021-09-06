# Simulação de Monte Carlo para fechamento do Ouro

## Analise da tendência do movimento dos preços

Neste exemplo, foi tomado o histórico (todas as datas) do fechamento do preço do Ouro. Deseja-se neste exemplo aplicar a simulção para analisar um movimento futuro levando em consideração a diseperção em torno de alguma tendência observada historicamente. Utilizamos aqui a tendência linear

![Figure_1](https://user-images.githubusercontent.com/5797933/132100603-3f54c0c1-a9c0-45e5-8581-5076c5fc889f.png)

Pode-se perceber que o valor do ouro oscilou ao redor de uma reta, mas essa oscilação é o objeto da simulação de Monte Carlo. Esse movimento errático ou oscilação da pontuação do Ouro é a diferença amostra após amostra entre o que se esperava cado os dados lineares fossem verdadeiro e o que aconteceu com o Ouro. 

O movimento errático dessa diferença é o que se chama **detrends**.

O **detrends** pode ser observado entre a diferença da reta de tedência e os pontos das amostras (esse movimento aleatório corresponde aos valores da área hachurada).

Em termos estatístico, a distribuição das diferenças entre a reta e a linha de tedência apresendou média de $5.55x10^-14$ e o desvio padrão 232.30 pontos. Para a simulação de Monte Carlo, esses valores são utilizados para a projeção futura do Ouro. `A simulção de Monte carlo é uma amostragem de possíveis cenários futuros, pois então recomenda-se cuidados ao fazer essa análise. Muitas das vezes a dsitribuição de probabilidade normal nem sempre se ajusta perfeitamente às oscilações dos preços.` 

![Figure_2](https://user-images.githubusercontent.com/5797933/132100604-9e39b52b-fdef-46ad-8cfb-708959387367.png)

