import os
import pandas as pd

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

from castor import CastorJsonToDataFrame, CastorDataFrameQueryRunner


@login_required
def get_queries(request):
    return render(request, 'queries.html')


@login_required
def run_query(request):
    query = request.POST.get('query')
    # convert JSON to dataframe
    j2df = CastorJsonToDataFrame(settings.CASTOR_JSON_FILES['dpca'])
    df = j2df.execute()
    # execute query
    runner = CastorDataFrameQueryRunner(df)
    df = runner.execute(query)
    # convert all data types to string (incl. dates) for correct display in HTML
    df = df.astype(str)
    return render(request, 'queries.html', context={'data': df.to_numpy(), 'columns': df.columns})
