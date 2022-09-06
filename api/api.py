from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pickle
import pandas as pd
from sklearn.pipeline import Pipeline

app = FastAPI()

class ScoringItem(BaseModel):
    HighBP:  int
    HighChol:  int
    CholCheck:  int
    BMI:  int
    Smoker:  int
    Stroke:  int
    HeartDiseaseorAttack:  int
    PhysActivity:  int
    Fruits:  int
    Veggies:  int
    HvyAlcoholConsump:  int
    AnyHealthcare:  int
    NoDocbcCost:  int
    GenHlth:  int
    MentHlth:  int
    PhysHlth:  int
    DiffWalk:  int
    Sex:  int
    Age:  int
    Education:  int
    Income:  int


with open('pipe.pkl', 'rb') as f_model:
    pipe: Pipeline = pickle.load(f_model)


@app.get('/dataset')
async def get_dataset():
    return FileResponse('dataset.csv')

@app.post('/predict')
async def scoring_endpoint(item: ScoringItem):
    df = pd.DataFrame([item.dict().values()], columns= item.dict().keys())
    yhat = pipe.predict(df)
    return { 'Outcome' : int(yhat) }

