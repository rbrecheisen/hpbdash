from django.db import models


class ReportModel(models.Model):

    title = models.CharField(max_length=1024)

    def __str__(self):
        return self.title


class QueryModel(models.Model):

    title = models.CharField(max_length=1024)
    sql_statement = models.CharField(max_length=2048)
    report = models.ForeignKey('ReportModel', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
