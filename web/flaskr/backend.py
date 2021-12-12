import psycopg2
import os
import csv
# USE_BAO = True
# USE_BAO = False
PG_CONNECTION_STR = "dbname=imdb user=imdb host=localhost"

def run_query(sql, bao_select=False, bao_reward=False):

    try:
        conn = psycopg2.connect(PG_CONNECTION_STR)
        cur = conn.cursor()
        cur.execute(f"SET enable_bao TO {bao_select or bao_reward}")
        cur.execute(f"SET enable_bao_selection TO {bao_select}")
        cur.execute(f"SET enable_bao_rewards TO {bao_reward}")
        cur.execute("SET bao_num_arms TO 5")
        cur.execute("SET statement_timeout TO 300000")
        cur.execute(sql)
        res = cur.fetchall()
        conn.close()
        # print(res)
        with open("/home/slm/pg_related/BaoForPostgreSQL/query_log/query_result.txt","w") as f:
            csv_out = csv.writer(f)
            csv_out.writerows(res)
            
        # NOTE: save sql query
        with open("/home/slm/pg_related/BaoForPostgreSQL/query_log/sql.txt","a") as f:
            f.write(sql+"\n")
        print("Query executed successfully")    

    except psycopg2.Error as e:
        print(e.pgerror)
        with open("/home/slm/pg_related/BaoForPostgreSQL/query_log/query_result.txt","w") as f:
            f.writelines(e.pgerror)
        