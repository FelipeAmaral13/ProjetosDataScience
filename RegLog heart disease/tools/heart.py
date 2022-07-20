import joblib
import numpy as np

class Heart:

    # Método construtor
    def __init__(self, heart):
        self.heart = heart

    def prepare(self):
        # Lista de resultados
        result = np.zeros(13)

        # Extrai cada item passado pela aplicação
        result[0] = float(self.heart[0])  #age
        result[1] = float(self.heart[1])  #sex
        result[2] = float(self.heart[2])  #chest pain type (4 values)
        result[3] = float(self.heart[3])  #resting blood pressure
        result[4] = float(self.heart[4])  #serum cholestoral in mg/dl
        result[5] = float(self.heart[5])  #fasting blood sugar > 120 mg/dl
        result[6] = float(self.heart[6])  # resting electrocardiographic results (values 0,1,2)
        result[7] = float(self.heart[7])  #maximum heart rate achieved
        result[8] = float(self.heart[8])  #exercise induced angina
        result[9] = float(self.heart[9])  #oldpeak = ST depression induced by exercise relative to rest
        result[10] = float(self.heart[10])  #the slope of the peak exercise ST segment
        result[11] = float(self.heart[11])  #number of major vessels (0-3) colored by flourosopy
        result[12] = float(self.heart[12])  # thal: 0 = normal; 1 = fixed defect; 2 = reversable defect

        return result

    # Método para as previsões
    def predict(self, heart):
        heart_to_predict = [heart]
        model = joblib.load('modelo/model.pkl')
        predicted_heart_value = model.predict(heart_to_predict)
        value = predicted_heart_value[0]
        return value

