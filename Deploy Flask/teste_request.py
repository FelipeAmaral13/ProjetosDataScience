import requests

url = 'http://127.0.0.1:5000/api/'

dados = {
    "Age":56.0,
    "Sex":1.0,
    "ChestPainType":0.0,
    "RestingBP":120.0,
    "Cholesterol":85.0,
    "FastingBS":0.0,
    "RestingECG":1.0,
    "MaxHR":140.0,
    "ExerciseAngina":0.0,
    "Oldpeak":0.0,
    "ST_Slope":2.0
}

auth = requests.auth.HTTPBasicAuth('teste','teste_post')

response = requests.post(url, json=dados, auth=auth)

response.json()