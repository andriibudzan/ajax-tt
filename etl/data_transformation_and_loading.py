import os
import json

import psycopg2
import pandas as pd

with open('./etl/datasource_configs.json') as f:
    config = json.load(f)

db_employees = config['db_employees']

query = """
select e.id as id, reports, position, hired, salary, team_id, team_name from employees e
left join teams t on e.team_id = t.id;
"""



if __name__ == '__main__':
    df_legacy_data = pd.read_csv('./data/silver/employees.csv')

    # connecting to db
    conn = psycopg2.connect(
            **db_employees
            )

    with conn.cursor() as cur:
        try:
            cur.execute(query)
            rows = cur.fetchall()
        except psycopg2.Error as e:
            print("Error while executing SELECT query: ", e)
        finally:
            cur.close()
            conn.close()

    df_columns = [
        x.strip() for x in query.split('from')[0].split('as')[-1].split(',')
        ]

    df_employees_db = pd.DataFrame(rows, columns=df_columns)

    df = (
        df_legacy_data
        .set_index('id')
        .join(df_employees_db.set_index('id'))
        .reset_index()
        .drop('team_id', axis=1)
        .rename(mapper={'team_name': 'team'}, axis=1)
        .astype({'reports': 'Int64'})
    )
    os.makedirs('./data/gold/', exist_ok=True)
    df.to_csv('./data/gold/employees_detailed.csv', index=False)
    print(df.head(5))
