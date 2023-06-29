import json

from barbell2_castor.castor2sqlite import CastorToDict


class CastorToJSON:

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
