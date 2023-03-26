# hpbdash

- Setup task flow in Prefect that uses barbell2.castor.castor2sqlite package to exract 
  data from Castor and store it in a SQLite database
- Build webapp that runs a bunch of SQL queries on the SQLite database and displays the
  results in a web page.


## MODELS

### QueryModel

A query contains a single SQL statement.

### ReportModel

A report contains a collection of queries that are executed against the SQLite database.
The results of each query are collected in a single report (HTML or PDF). Each query is
assocated with a graph type, e.g., a line graph or bar chart.
A report is also associated with a render() function that specifies exactly what needs to
be in the report in terms of text and images. 


## OBJECT CLASSSES

### QueryRunner

Executes SQL statement taken from the query model and produces a Pandas dataframe.

### ReportGenerator

Generates a report (HTML of PDF) based on a ReportModel


## CANDIDATE VARIABLES

- Patient ID (text)
- Birth Date (date)
- Gender (male/female)
- Body Weight (kg)
- Body Mass Index (kg/m2)
- Surgery Date (date)
- Time Diagnosis to Surgery (days)
- Hospital Stay (days)
- Complications (boolean)
- Organ (categorical: liver/pancreas/biliary_tract)
- Procedure (categorical: ablation/open/laparoscopic)
