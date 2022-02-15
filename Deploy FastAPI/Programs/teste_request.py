import json
import requests

data = {
  "Pregnancies": 6,
  "Glucose": 148,
  "BloodPressure": 72,
  "SkinThickness": 35,
  "Insulin": 0,
  "BMI": 33.6,
  "DiabetesPedigreeFunction": 0.627,
  "Age": 50
}
data_json = json.dumps(data)
url_string = f'http://localhost:8000/predict'
r = requests.get(url_string, data=data_json)

print(r.json())

