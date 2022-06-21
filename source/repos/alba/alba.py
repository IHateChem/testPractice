import pymysql
import time as tm
from datetime import datetime
from makelog import writelog

def finmin(cur):
    cur.execute("SELECT SEC_CD_S, min(LOW), PR_DATE as min_LOW FROM history.ch6110 GROUP BY SEC_CD_S")
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
        cur.CLOSE()
    print("DD")
    target_list = [x[0] for x in target_list]
    return target_list
def make1(cur, cur_tablename, target_tablename):
    text = "Start data collecting"
    writelog(text)
    query = f"SELECT SEC_CD_S FROM HISTORY.{cur_tablename} GROUP BY SEC_CD_S;"
    cur.execute(query)
    SEC_CD_S_list =  cur.fetchall()
    query = f"SELECT SEC_CD_S, PR_DATE, VOLUME, PRATE, VRATE FROM HISTORY.{cur_tablename} WHERE PRATE <> 1 AND PRATE <> 0 ORDER BY  SEC_CD_S , PR_DATE;"
    cur.execute(query)
    PRATE_targets =  cur.fetchall()
    query = f"SELECT SEC_CD_S, PR_DATE, VOLUME, PRATE, VRATE FROM HISTORY.{cur_tablename} WHERE VRATE <> 1 AND VRATE <> 0 ORDER BY  SEC_CD_S , PR_DATE;"
    cur.execute(query)
    VRATE_targets =  cur.fetchall()
    text = f"finish data collecting and start making {target_tablename}"
    writelog(text)#{target_tablename} {cur_tablename}
    try:
        query = f"INSERT INTO history.{target_tablename} (PR_DATE, SEC_CD_S, HIGH, LOW, VOLUME, OPEN, CLOSE) SELECT PR_DATE, SEC_CD_S,  HIGH, LOW, VOLUME, OPEN, CLOSE FROM history.{cur_tablename}"
        cur.execute(query)
        conn.commit()
        text = f"finish making {target_tablename} starting changing values"
    except Exception as e:
        text = "query: "+query + "error: "+str(e)
    writelog(text)
    try:
        for PRATE_target in PRATE_targets: #prate_target: (SEC_CD_S, PR_DATE, VOLUME, PRATE, VRATE)
            query = f"UPDATE HISTORY.{target_tablename} SET OPEN = OPEN*{float(PRATE_target[3])}, HIGH = HIGH *{float(PRATE_target[3])}, LOW  = LOW*{float(PRATE_target[3])}, CLOSE = CLOSE*{float(PRATE_target[3])} WHERE SEC_CD_S = '{PRATE_target[0]}' AND PR_DATE < '{PRATE_target[1]}';"
            cur.execute(query)
            conn.commit()
        text = "finish changing prate"
    except Exception as e:
        text = str("query: "+query + " error: "+str(e))
    writelog(text)
    try: 
        for VRATE_target in VRATE_targets:
            query = f"UPDATE HISTORY.{target_tablename} SET VOLUME = VOLUME*{float(VRATE_target[4])} WHERE SEC_CD_S = '{PRATE_target[0]}' AND PR_DATE < '{VRATE_target[1]}';"
            cur.execute(query)
            conn.commit()
        text = f"finish chanig values CLOSE program.."
    except Exception as e:
        text = str("query: "+query + " error: "+str(e))
    writelog(text, finish = True)




def get_20MA(cur):
    cur.execute(f"SELECT SEC_CD_S FROM history.ch6110 WHERE PR_DATE = {today} AND SEC_CD_S = {k} AND LOW < {v*1.05} and LOW > {v}")
    pass
conn = pymysql.connect(host="124.198.124.188", user="root", password="fmsoft1004",
                       db="history", charset="utf8")  # 1. DB 연결
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
make1(cur, "ch6110", "ch6111")
#store_min_values , store_min_date = finmin(cur)
cur.CLOSE()
#target_list = find_five_percent(cur, store_min_values, store_min_date)
#print(target_list)

conn.CLOSE() # 6. DB 닫기 (=연결 해제)
#print(store_min_values)
print('OK~')

