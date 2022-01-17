import requests
import pandas
import pickle

class Process:

    runtime = None

    pipeline = None

    db = None

    def __init__(self, runtime, pipeline, db):
        self.runtime = runtime
        self.pipeline = pipeline
        self.db = db

    def train_model(self, dataset):
        model = self.runtime.train(dataset)
        if model != None:
            self.runtime.model = model
            outfile = open('/app/model/model.pkl', 'wb')
            pickle.dump(model, outfile)
            outfile.close()

    def upload(self, loader, append):
        output = self.runtime.process_dataset(loader.data)
        loader.store(output, append)
        self.train_model(output)
        self.runtime.generate_statics(output)        
        self.pipeline.trigger_downstream(self.db)
        

    def refresh(self):
        response = requests.get(f'http://{self.pipeline.dependency}/api/v1/data')
        data = response.json()
        df = pandas.DataFrame(data)
        self.runtime.process_dataset(df)
        self.db.store_pandas(df)
        self.train_model(df)
        self.runtime.generate_statics(df)        
        self.pipeline.trigger_downstream(self.db)
