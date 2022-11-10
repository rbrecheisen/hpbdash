HPB Dashboard
=============

Background process periodically extracts data from Castor and caches it on the server as a CSV file.
Rows represent surgery treatments identified by a patient ID and surgery date. Columns represent
variables that are relevant for performance.

Example variables:

- Patient ID (text)
- Age (integer)
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
with this file until we have Castor up-and-running