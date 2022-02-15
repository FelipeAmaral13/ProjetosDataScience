import json
import pandas as pd
from fastapi import FastAPI
import pickle
import os
from pydantic import BaseModel

class Diabetes(BaseModel):
    Pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int 

model = pickle.load(
    open(os.path.join(os.getcwd(), 'model', 'diabeteseModel.pkl'), 'rb'))


# with open('scaling.json') as f:
#     s = json.load(f)

app = FastAPI()

@app.get("/predict")
async def get_predition(diabetes: Diabetes):
    p = diabetes.Pregnancies
    g = diabetes.Glucose
    b = diabetes.BloodPressure
    s = diabetes.SkinThickness
    i = diabetes.Insulin
    B = diabetes.BMI
    d = diabetes.DiabetesPedigreeFunction
    a = diabetes.Age

    X_scaled = [[p, g, b, s, i, B, d, a]]

    y_pred = model.predict(X_scaled)
    df_pred = pd.DataFrame({
        'Diabetes': ['Outcome'],
        'Confidence': y_pred.flatten()
    })


    df_pred['Confidence'] = [round(x,4) for x in df_pred['Confidence']]
    df_pred.set_index('Diabetes', inplace=True)
    return df_pred.to_dict()

