import os
import json
import zipfile

import requests
import pandas as pd

from requests.auth import HTTPBasicAuth

# uploading configs
with open('./etl/datasource_configs.json') as f:
    config = json.load(f)

db_legacy = config['db_legacy']

if __name__ == '__main__':
    # downloading and unzipping data from legacy db
    url = os.getenv('DBL_URL')
    endpoint_employees = f"{url}{db_legacy['endpoint_employees']}"
    endpoint_employee_details = f"{endpoint_employees}{db_legacy['endpoint_employee_details']}"
    auth = HTTPBasicAuth(os.getenv("DBL_USERNAME"), os.getenv("DBL_PASSWORD"))
    datastorage = './data'
    legacy_data_path = f'{datastorage}/bronze'

    # downloading data archive
    res = requests.get(url=endpoint_employees, auth=auth)
    if res.status_code == 200:
        print('Connected to legacy db')
        os.makedirs(f'{datastorage}/bronze', exist_ok=True)
        with open(f'{legacy_data_path}/data.zip', 'wb') as f:
            f.write(res.content)
            print('Data archive downloaded')

    # unzipping archive
    with zipfile.ZipFile(f'{legacy_data_path}/data.zip', 'r') as zip:
        zip.extractall(legacy_data_path)
        print('Data archive unzipped')

    # reading data from unzipped file
    df_tokens = pd.read_excel(f'{legacy_data_path}/tokens.xlsx')
    df_tokens = df_tokens.rename(
            mapper={x: x.lower() for x in df_tokens.columns},
            axis=1
            )
    print(df_tokens.head(5))
    user_details = []
    for token in df_tokens['token'].values:
        res_user_details = requests.get(
                url=endpoint_employee_details.format(token=token),
                auth=auth
                )
        if res_user_details.status_code == 200:
            user_details.append(res_user_details.json())
        else:
            print(f"Error: {res_user_details.status_code}")
    df_users = pd.DataFrame.from_records(user_details)
    df_users = (
        df_users.set_index('id')
        .join(df_tokens.set_index('id'))
        .reset_index()
    )
    os.makedirs(f'{datastorage}/silver/', exist_ok=True)
    df_users.to_csv(f'{datastorage}/silver/employees.csv', index=False)
    print(df_users.head(5))
