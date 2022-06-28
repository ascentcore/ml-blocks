import logging
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier


logger = logging.getLogger(__name__)

'''
Use generator script (generator_script.py) to populate server with data

Sample request

 curl -X 'POST' \
  'http://localhost:9080/api/v1/model/predict' \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -d '[ {"x": -0.2,"y": -0.3}, {"x": 0.5,"y": -0.7}, {"x": -0.3, "y": 0.3}, {"x": 0.5, "y": 0.7} ]' 
'''
class Block:
    name = os.getenv("BLOCK_NAME", "Random Forest Classifier")

    loaders = ['file_loader', 'pandas_loader']

    def train(self, runtime):
        data = runtime.loader.dataset
        clf = RandomForestClassifier(max_depth=2, random_state=0)
        model = clf.fit(data.iloc[:, 1:-1].values, data.iloc[:, -1:].values)
        return model


    def on_before_predict(self, runtime):
        logger.info(runtime.last_op_data);
        return [[item['x'], item['y']] for item in runtime.last_op_data]

    def predict(slef, runtime):
        logger.info('Local Predict')
        model = runtime.model
        return model.predict(runtime.last_op_data)

    def on_after_predict(self, runtime):
        return runtime.last_op_data.tolist()
