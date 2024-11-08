# Prevendo o Churn de Alunos com RandomForest

Este projeto visa prever a evasão de alunos (churn) em um contexto educacional. Ele utiliza o algoritmo Random Forest e calibrações de probabilidade para melhorar a acurácia das previsões. O projeto é composto por um notebook de análise, um script de deploy em Streamlit e um dataset para treino e teste.

## Estrutura do Projeto

- **Projeto_churn_aluno.ipynb**: Notebook contendo a análise exploratória de dados, treinamento do modelo e calibração.
- **deploy.py**: Script em Python para deploy do modelo utilizando Streamlit. Permite entrada de dados do usuário e exibe a previsão de churn.
- **student_churn_dataset.csv**: Dataset contendo informações dos alunos e se houve ou não churn. As variáveis incluem idade, horas de estudo semanais, satisfação com o curso, mensalidade, tipo de curso, duração do curso, entre outros.

## Requisitos

- pip install -r requirements.txt

## Dataset

O dataset **student_churn_dataset.csv** possui as seguintes colunas:

- `Idade`: Idade do aluno.
- `HorasEstudoSemanal`: Quantidade de horas que o aluno estuda por semana.
- `SatisfacaoCurso`: Nível de satisfação com o curso (escala de 1 a 5).
- `Mensalidade`: Valor da mensalidade paga pelo aluno.
- `TipoCurso`: Tipo do curso, que pode ser "Online", "Presencial" ou "Semi-Presencial".
- `DuracaoCurso`: Duração do curso, podendo ser "Anual", "Médio" ou "Semestral".
- `Churn`: Variável alvo, indicando se o aluno evadiu ou não.

## Uso

### Notebook de Análise

1. Abra o notebook **Projeto_churn_aluno.ipynb** para visualizar a análise exploratória de dados, o treinamento e a calibração do modelo.
2. O notebook apresenta as métricas de Brier Score e Log Loss para avaliar a calibração antes e depois de aplicar o Platt Scaling e a Isotonic Regression.
3. A partir dessa análise, o modelo mais calibrado é salvo para ser utilizado no deploy.
   

### Deploy do Modelo com Streamlit

1. Execute o script **deploy.py** para abrir a interface de usuário via Streamlit.
   ```bash
   streamlit run deploy.py
