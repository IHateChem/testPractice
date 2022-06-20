import pymysql
import time as tm
from datetime import datetime

def finmin(cur):
    cur.execute("SELECT SEC_CD_S, min(LOW), PR_DATE as min_low FROM history.ch6110 GROUP BY SEC_CD_S")
    result = cur.fetchall()
    store_min_values = {x[0]: x[1] for x in result}
    store_min_date = {x[0]: x[2] for x in result}
    return store_min_values, store_min_date

def get_today():
    return datetime.today().strftime('%Y%m%d')

def print_log():
    pass

def find_five_percent(cur, store_min_values, store_min_date):
    today = get_today()
    target_list = []
    print("start find list")
    i = 0
    for k, v in  store_min_values.items():
        cur = conn.cursor()
        cur.execute(f"SELECT SEC_CD_S FROM history.ch6110 WHERE PR_DATE = {today} AND SEC_CD_S = {k} AND LOW < {v*1.05} and LOW > {v}")
        targets =  cur.fetchall()
        if targets != ():
            target_list.append(targets)
            print(targets[0][0], )
        cur.close()
    print("DD")
    target_list = [x[0] for x in target_list]
    return target_list

conn = pymysql.connect(host="124.198.124.188", user="root", password="fmsoft1004",
                       db="history", charset="utf8")  # 1. DB 연결
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
store_min_values , store_min_date = finmin(cur)
cur.close()
target_list = find_five_percent(cur, store_min_values, store_min_date)
print(target_list)
conn.close() # 6. DB 닫기 (=연결 해제)
#print(store_min_values)
print('OK~')

