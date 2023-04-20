import os
import json
import pandas as pd

from django.db import models
from django.conf import settings
from django.dispatch import receiver


class QueryModel(models.Model):

    name = models.CharField(max_length=1024)
    sql_statement = models.CharField(max_length=2048)

    def __str__(self):
        return self.name
    
    
class QueryResultModel(models.Model):
    
    query = models.ForeignKey('QueryModel', on_delete=models.CASCADE)
    result_file = models.CharField(max_length=1024)
    
    def as_df(self):
        # with open(settings.CASTOR_DD_FILE, 'r') as f:
        #     dd = json.load(f)        
        df = pd.read_csv(self.result_file, sep=';', dtype=str)
        df = df.fillna('unknown')
        return df
    
    def __str__(self):
        return f'QueryResult(Query("{self.query.name}"))'
    

@receiver(models.signals.post_delete, sender=QueryResultModel)
def query_result_post_delete(sender, instance, **kwargs):
    if os.path.isfile(instance.result_file):
        os.remove(instance.result_file)


class ReportModel(models.Model):    

    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
    

class ReportItemModel(models.Model):

    report = models.ForeignKey('ReportModel', on_delete=models.CASCADE)
    query = models.ForeignKey('QueryModel', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'ReportItem(Query("{self.query.name}"))'
