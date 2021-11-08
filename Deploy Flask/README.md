# Deploy Flask

Projeto simples para fazer o deploy, através de uma API, de um modelo de ML para pedição de ataque cardiáco.

## Info:

**Idade**: idade do paciente [anos]

**Sexo**: sexo do paciente [M: Masculino, F: Feminino]

**Tipo de dor torácica**: tipo de dor torácica [TA: angina típica, ATA: angina atípica, NAP: dor não anginosa, ASY: assintomática]

**BP em repouso**: pressão arterial em repouso [mm Hg]

**Colesterol**: colesterol sérico [mm / dl]

**SB em jejum:** açúcar no sangue em jejum [1: se SB em jejum> 120 mg / dl, 0: caso contrário]

**ECG em repouso**: resultados de eletrocardiograma em repouso [Normal: Normal, ST: tendo anormalidade da onda ST-T (inversões da onda T e / ou elevação ou depressão de ST> 0,05 mV), HVE: mostrando hipertrofia ventricular esquerda provável ou definitiva pelos critérios de Estes]

**MaxHR**: freqüência cardíaca máxima alcançada [valor numérico entre 60 e 202]

**ExerciseAngina**: angina induzida por exercício [S: Sim, N: Não]

**Oldpeak**: oldpeak = ST [valor numérico medido na depressão]

**ST_lope**: a inclinação do pico do segmento ST do exercício [Up: uploping, Flat: flat, Down: downsloping]

**HeartDisease**: classe alvo[1: doença cardíaca, 0: Normal]

## API

Postman:
* POST - http://127.0.0.1:5000/api/
* Authorization - Basic Auth 
* Headers - Content-Type (application/json)
