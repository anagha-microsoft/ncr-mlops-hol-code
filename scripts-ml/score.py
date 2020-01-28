import os
import json
import numpy as np
import pickle
from azureml.core.model import Model
from azureml.monitoring import ModelDataCollector

def init():
    global model
    global inputs_dc
    global prediction_dc
    
    try:
        model_name = 'MODEL-NAME' # Placeholder model name
        print('Looking for model path for model: ', model_name)
        model_path = Model.get_model_path(model_name = model_name)
        print('Loading model from: ', model_path)
        model = pickle.load(open(model_path, 'rb'))
        print("Model loaded from disk.")
        print(model.summary())

        #inputs_dc = ModelDataCollector("model_telemetry", identifier="inputs")
        #prediction_dc = ModelDataCollector("model_telemetry", identifier="predictions", feature_names=["prediction"])
    except Exception as e:
        print(e)
        
# note you can pass in multiple rows for scoring
def run(raw_data):
    import time
    try:
        print("Received input: ", raw_data)        
        inputs = json.loads(raw_data)["data"]    
        inputs = np.array(inputs)
        results = model.predict(inputs)

        #inputs_dc.collect(inputs) #this call is saving our input data into Azure Blob
        #prediction_dc.collect(results) #this call is saving our output data into Azure Blob

        print("Prediction created " + time.strftime("%H:%M:%S"))
        
        results = results.tolist()
        return json.dumps(results)
    except Exception as e:
        error = str(e)
        print("ERROR: " + error + " " + time.strftime("%H:%M:%S"))
        return error
