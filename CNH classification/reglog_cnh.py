import glob
import time
import cv2
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from joblib import dump, load
from sklearn.metrics import accuracy_score


# Cria objeto com a marcação do tempo do inicío da sessão
start = time.time()



baseurl = ''

# Vasculha por arquivos do tipo *.jpg e cria uma lista com endereços
aberta_files = glob.glob(baseurl + "aberta/*.jpg")
frente_files = glob.glob(baseurl + "frente/*.jpg")
verso_files = glob.glob(baseurl + 'verso/*.jpg')

print(aberta_files)
print(frente_files)
print(verso_files)


# Carrega uma imagem de cada classe
img1 = cv2.imread(aberta_files[0])
img2 = cv2.imread(frente_files[0])
img3 = cv2.imread(verso_files[0])

# Redimensiona imagens para melhorar visualização
img1 = cv2.resize(img1,None, fx=.4,fy=.4)
img2 = cv2.resize(img2,None, fx=.4,fy=.4)
img3 = cv2.resize(img3,None, fx=.4,fy=.4)

cv2.imshow("Imagem", img1)
cv2.waitKey(0)

cv2.imshow("Imagem", img2)
cv2.waitKey(0)

cv2.imshow("Imagem", img3)
cv2.waitKey(0)


X = []
y = []


for f in aberta_files:
    img = cv2.imread(f)
    redim = cv2.resize(img, (250,200))
    X.append(redim.flatten())
    y.append('Aberta')


for f in frente_files:
    img = cv2.imread(f)
    redim = cv2.resize(img, (250,200))
    X.append(redim.flatten())
    y.append('Frente')


for f in verso_files:
    img = cv2.imread(f)
    redim = cv2.resize(img, (250,200))
    X.append(redim.flatten())
    y.append('Verso')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

model = LogisticRegression(random_state=0, solver='sag', multi_class='multinomial', max_iter=10000, verbose=1, tol=0.00005)
model.fit(X_train,y_train)

print("-"*20)
dump(model, baseurl + "classificacao_cnh__2.pkl")

model_test = load(baseurl + "classificacao_cnh__2.pkl")

y_pred = model_test.predict(X_test)
precisao = accuracy_score(y_test, y_pred)


# Calcula o tempo da duração da execução
end = time.time()
duracao = end - start

print("Tempo total do processo: {} segundos".format(round(duracao,2)))

for id in range(0,len(X_test)):

  y_pred = model_test.predict([X_test[id]])
  print(y_pred[0], '--', y_train[id])


  img_test = X_test[id].reshape(200,250,3)

  cv2.imshow("Teste", img_test)
  cv2.waitKey(0) 