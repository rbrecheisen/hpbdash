HPB Dashboard
=============

Background process periodically extracts data from Castor and caches it on the server as a CSV or JSON file.
Rows represent surgery treatments identified by a patient ID and surgery date. Columns represent
variables that are relevant for performance.

Example variables:

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

Generate synthetic CSV file with generated values for the above variables. Test the application
with this file until we have Castor up-and-running.

How does this work in practice? Our background process periodically extracts data from Castor using certain search
criteria. For example, extract all treatment records from the last month or last year. Or we could just extract
everything and let the dashboard application decide what to show, and in what level of detail. How do we keep the
background process and dashboard application from clashing? When the background process is downloading data, the app
should not try to load it. We could let the background process download the data to a file data.json.downloading and
rename that file to data.json when it's finished. The app simply looks for the file data.json and imports it. Should
the background process keep track of previous versions of the data? Is that useful to have? Is there a need to keep
multiple copies of the data? Not really. So let it overwrite the previous data.json file. Or better, first delete it
and then create a new file data.json.downloading.