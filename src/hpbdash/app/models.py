from django.db import models


class QueryModel(models.Model):

    title = models.CharField(max_length=1024)
    sql_statement = models.CharField(max_length=2048)

    def __str__(self):
        return self.title
