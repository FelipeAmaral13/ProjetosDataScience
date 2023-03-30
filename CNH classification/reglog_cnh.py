import glob
import os
import cv2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from joblib import dump, load
from sklearn.metrics import accuracy_score


class CNHClassifier:
    def __init__(self, baseurl):
        self.baseurl = baseurl
    
    def load_image(self, path):
        img = cv2.imread(path)
        return cv2.resize(img, (250,200)).flatten()

    def load_data(self):
        aberta_files = glob.glob(self.baseurl + "\\aberta\\*.jpg")
        frente_files = glob.glob(self.baseurl + "\\frente\\*.jpg")
        verso_files = glob.glob(self.baseurl + '\\verso\\*.jpg')
        
        X = []
        y = []

        for f in aberta_files:
            X.append(self.load_image(f))
            y.append('Aberta')

        for f in frente_files:
            X.append(self.load_image(f))
            y.append('Frente')

        for f in verso_files:
            X.append(self.load_image(f))
            y.append('Verso')

        return train_test_split(X, y, test_size=0.15)

    def train(self):
        X_train, X_test, y_train, y_test = self.load_data()
        model = LogisticRegression(random_state=0, solver='sag', multi_class='multinomial', max_iter=10000, verbose=1, tol=0.00005)
        model.fit(X_train,y_train)
        dump(model, self.baseurl + "classificacao_cnh_2.pkl")

        y_pred = model.predict(X_test)
        return accuracy_score(y_test, y_pred)

    def predict(self, img_path):
        model_test = load(self.baseurl + "classificacao_cnh_2.pkl")
        img = self.load_image(img_path)
        y_pred = model_test.predict([img])
        return y_pred[0]


classifier = CNHClassifier(os.getcwd())

# Para treinar o modelo
classifier.train()

# Para classificar uma nova imagem
# img_path = 'path/to/new/image.jpg'
# predicted_class = classifier.predict(img_path)
