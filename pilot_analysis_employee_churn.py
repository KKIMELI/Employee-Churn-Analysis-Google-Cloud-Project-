# -*- coding: utf-8 -*-
"""Pilot_Analysis_Employee_Churn.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NL46m1-MlL8khTh_zThBZxtY6Q2vxbW3
"""

!pip install google-cloud

!pip show google-cloud

"""# Connect to Big Query"""

#libraries that we need
from google.cloud import bigquery
from google.colab import auth

# authenticate
auth.authenticate_user()

#initialize the client for BigQuery
project_id = 'churn-analysis-cloud-project'
client = bigquery.Client(project=project_id, location='US')

#get the dataset and table
dataset_ref = client.dataset('employeedata', project=project_id)
dataset = client.get_dataset(dataset_ref)
table_ref = dataset.table('tbl_hr_data')
table = client.get_table(table_ref)
table.schema

new_table_ref = dataset.table('tbl_new_employees')
new_table = client.get_table(new_table_ref)
new_table.schema

# convert to dataframe
df = client.list_rows(table=table).to_dataframe()
df.head()

# convert to dataframe
df2 = client.list_rows(table=new_table).to_dataframe()
df2.head()

"""# Build Model

## Install Pycaret
"""

!pip install pycaret

"""# Code and Train Model"""

# get our model
from pycaret.classification import *

df.columns

# setup or model
setup(df, target='Quit_the_Company',
      session_id=123,
      ignore_features=['employee_id'],
      categorical_features=['salary','Departments'])

compare_models()

rf_model = create_model('rf')

final_df = predict_model(rf_model)

final_df.head()

new_predictions = predict_model(rf_model, data = df2)

new_predictions.head()

#write back to bigquery
new_predictions.to_gbq('employeedata.pilot_predictions',
                       project_id,
                       chunksize=None,
                       if_exists='replace')

plot_model(rf_model,plot='feature')

# create a feature table
rf_model.feature_names_in_

rf_model.feature_importances_

import pandas as pd
feature_table = pd.DataFrame(zip(rf_model.feature_names_in_,rf_model.feature_importances_),columns=['feature','importance'])
feature_table

feature_table.to_gbq('employeedata.feature_table',
                     project_id,
                     chunksize=None,
                     if_exists='replace')