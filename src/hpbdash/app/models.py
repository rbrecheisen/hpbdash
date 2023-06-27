import os
import pandas as pd

from django.db import models
from django.conf import settings
from django.dispatch import receiver


class QueryModel(models.Model):

    name = models.CharField(max_length=1024)
    sql = models.CharField(max_length=2048)
    
    
class QueryResultModel(models.Model):
    
    query = models.ForeignKey('QueryModel', on_delete=models.CASCADE)
    result_file = models.CharField(max_length=1024)
    
    def as_df(self):
        df = pd.read_csv(self.result_file, sep=';', dtype=str)
        df = df.fillna('unknown')
        return df
    

class ReportModel(models.Model):

    name = models.CharField(max_length=1024, unique=True)
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
    queries = models.ManyToManyField(QueryModel)


@receiver(models.signals.post_delete, sender=QueryResultModel)
def query_result_post_delete(sender, instance, **kwargs):
    # also called when query itself is deleted because result is linked to it
    if os.path.isfile(instance.result_file):
        os.remove(instance.result_file)
