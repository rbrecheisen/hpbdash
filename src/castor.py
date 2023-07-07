import json
import pandas as pd

from barbell2_castor.castor2sqlite import CastorToDict


class CastorToJson:

    def __init__(self, study_name, client_id, client_secret, output_json):
        self.study_name = study_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.output_json = output_json

    def execute(self):
        castor2dict = CastorToDict(self.study_name, self.client_id, self.client_secret)
        data = castor2dict.execute()
        with open(self.output_json, 'w') as f:
            json.dump(data, f)
        return self.output_json


class CastorJsonToDataFrame:

    def __init__(self, input_json):
        self.input_json = input_json
    
    def execute(self):
        with open(self.input_json, 'r') as f:
            data = json.load(f)
        df_data = {}
        for field_name in data.keys():
            df_data[field_name] = data[field_name]['field_values']
        df = pd.DataFrame(data=df_data)
        for field_name in data.keys():
            if data[field_name]['field_type'] == 'date':
                # df[field_name] = pd.to_datetime(df[field_name], dayfirst=True, format='%Y-%m-%d', errors='coerce')
                df[field_name] = pd.to_datetime(df[field_name], dayfirst=True, errors='coerce')
        return df
    

class CastorDataFrameQueryRunner:

    def __init__(self, df):
        self.df = df
    
    def execute(self, query):
        # get columns to be selected in the query result dataframe
        # they're between SELECT and WHERE
        query = query.lower()
        idx_start = 7
        idx_end = query.index('where')
        columns = [x.strip() for x in query[idx_start:idx_end].split(',')]
        # get filter conditions after WHERE clause
        filter_conditions = query[idx_end+6:]
        df = self.df.query(filter_conditions)
        df = df[columns]
        return df
