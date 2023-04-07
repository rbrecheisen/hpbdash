from django.db import models


class QueryModel(models.Model):

    name = models.CharField(max_length=1024)
    sql_statement = models.CharField(max_length=2048)

    def __str__(self):
        return self.name
    
    
class QueryResultModel(models.Model):
    
    query = models.ForeignKey('QueryModel', on_delete=models.CASCADE)
    result_file = models.CharField(max_length=1024)
    
    def as_df(self):
        import pandas as pd
        return pd.read_csv(self.result_file)
    
    def __str__(self):
        return f'QueryResult(Query("{self.query.name}"))'


# class ReportModel(models.Model):
    
#     name = models.CharField(max_length=1024)

#     def __str__(self):
#         return self.name
    
    
# class ReportItemModel(models.Model):
    
#     report = models.ForeignKey('ReportModel', on_delete=models.CASCADE)
#     query_result = models.ForeignKey('QueryResultModel', on_delete=models.DO_NOTHING)
    
#     def __str__(self):
#         return f'ReportItem(QueryResult("{self.query_result.query.name}"))'