import pymysql
import time as tm
from datetime import datetime, timedelta
from makelog import writelog
import statistics
import calendar

def finmin(cur, table):
    cur.execute(f"SELECT a.SEC_CD_S, a.min_LOW, a.PR_DATE FROM(SELECT SEC_CD_S, min(LOW) as min_LOW , PR_DATE FROM history.{table} GROUP BY SEC_CD_S) AS a WHERE a.PR_DATE < date_add(now(), INTERVAL -12 month)")
    result = cur.fetchall()
    store_min_values = {x[0]: x[1] for x in result}
    store_min_date = {x[0]: x[2] for x in result}
    return store_min_values, store_min_date

def get_today():
    return datetime.today().strftime('%Y%m%d')

def get_recent_tradingday(cur, date, n):
    query = f"SELECT PR_DATE FROM history.CH6111 WHERE PR_DATE < '{date}' GROUP BY PR_DATE ORDER BY pr_date DESC LIMIT {n}"
    cur.execute(query)
    dates = cur.fetchall()
    dates = [x[0] for x in dates]
    return dates

def cross_share_price(cur, target, date, x = 10, n = 4):
    query = f"SELECT CLOSE FROM history.ch6121 WHERE SEC_CD_S = '{target}' AND PR_DATE <= '{date}' ORDER BY PR_DAET DESC LIMIT N"
    cur.execute(query)
    closes = cur.fetchall()
    closes = [x[0] for x in closes]
    iscross_share_price = True
    for i, close in enumerate(closes):
        if i == 0:
            before = close
        else:
            if close < (100-x)/100 * before or close > (100+x)/100 * before:
                iscross_share_price = False
                break
    return iscross_share_price


def find_five_percent(cur, store_min_values, store_min_date):
    today = get_today()
    target_list = []
    text = "start find list"
    writelog(text)
    i = 0
    try:
        for k, v in  store_min_values.items():
            query  = f"SELECT SEC_CD_S FROM history.ch6111 WHERE PR_DATE = '{today}' AND SEC_CD_S = '{k}' AND LOW < {v*1.05} and LOW > {v}"
            cur.execute(query)
            targets =  cur.fetchall()
            if targets != ():
                target_list.append(targets)
        target_list = [x[0] for x in target_list]
        writelog("finish finding list")
    except Exception as e:
        text = str("query: "+query + " error: "+str(e))
        assert e
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

def gettargetlist(cur):
    today = get_today()
    today = "20220617"
    query = f"SELECT SEC_CD_S FROM history.ch6111 WHERE pr_date = '{today}';"
    cur.execute(query)
    text = "Extracting list..."
    writelog(text)
    target_list = cur.fetchall()
    target_list = [x[0] for x in target_list]
    return target_list


def getNma(cur,  target_id, n = 20, table = "ch6110"):
    today = get_today()
    text = f"Start get{n}ma"
    writelog(text)
    query = f"SELECT LOW, PR_DATE, SEC_CD_S FROM history.{table} WHERE SEC_CD_S = '{target_id}' ORDER BY PR_DATE"
    try: 
        cur.execute(query)
        text = f"finish getting data  from db"
        datum = cur.fetchall()
    except Exception as e:
        text = "query: "+query + "error: "+str(e)
    print(datum)
    lows = [x[0] for x in datum]
    writelog(text)
    avg = []
    for i, low in enumerate(lows):
        if i < n:
            avg.append(statistics.mean(lows[:i+1]))
        else:
            avg.append(statistics.mean(lows[i-n+1:i+1]))
    text = "finish get moving average"
    writelog(text)
    return 

def getTodayNma(cur,  target_id, n = 20, table = "ch6111"):
    today = get_today()
    text = f"Start get{n}ma"
    writelog(text)
    query = f"SELECT  a.PR_DATE, a.SEC_CD_S, AVG(a.CLOSE) FROM( SELECT PR_DATE, SEC_CD_S, CLOSE FROM history.{table}  AS b WHERE SEC_CD_S = '{target_id}' ORDER BY pr_date DESC  LIMIT {n}) AS a"
    try: 
        cur.execute(query)
        text = f"finish getting data  from db"
        datum = cur.fetchall()
    except Exception as e:
        text = "query: "+query + "error: "+str(e)
    print(datum)
    low = [x[2] for x in datum]
    writelog(text)
    return low


def getPastNma(cur, date, target_id, n = 20, table = "ch6111"):
    text = f"Start get{n}ma"
    year = date[:4]
    month = date[4:6]
    day = date[6:]
    if table == "ch6131":
        if month[0] == "0":
            month = month[1]
        day = calendar.monthrange(int(year), int(month))[1]
        date = year+month+str(day)
    elif table == "ch6121":
        if month[0] == "0":
            month = month[1]
        weekday = calendar.weekday(int(year),int(month),int(day))
        weekday = 4-weekday
        date = (datetime(int(year), int(month), int(day)) + timedelta(weekday)).strftime('%Y%m%d')
    writelog(text)
    query = f"SELECT  a.PR_DATE, a.SEC_CD_S, AVG(a.CLOSE) FROM( SELECT PR_DATE, SEC_CD_S, CLOSE FROM history.{table}  AS b WHERE PR_DATE <= '{date}' AND SEC_CD_S = '{target_id}' ORDER BY pr_date DESC  LIMIT {n}) AS a"
    try: 
        cur.execute(query)
        text = f"finish getting data  from db"
        datum = cur.fetchall()
    except Exception as e:
        text = "query: "+query + "error: "+str(e)
    low = [x[2] for x in datum]
    writelog(text)
    return low    

def islesstrade(cur, target, date, n =50,  x = 10, type = "w"):
    ret = False
    year = date[:4]
    month = date[4:6]
    day = date[6:]
    if type == "m":
        table = "ch6131"
        if month[0] == "0":
            month = month[1]
        day = calendar.monthrange(int(year), int(month))[1]
        date = year+month+str(day)
    if type == "w":
        weekday = calendar.weekday(int(year),int(month),int(day))
        weekday = 4-weekday
        date = (datetime(int(year), int(month), int(day)) + timedelta(weekday)).strftime('%Y%m%d')
        table = "ch6121"
    if type == "d":
        table = "ch6111"
    try:
        query = f"SELECT max(a.VOLUME) FROM (SELECT SEC_CD_S, VOLUME FROM history.{table} WHERE PR_DATE <= '{date}' AND  SEC_CD_S = '{target}' ORDER BY PR_DATE DESC limit {n}) as a "
        cur.execute(query)
        max_volume = cur.fetchall()[0][0]
        query = f"SELECT VOLUME FROM history.{table} WHERE SEC_CD_S = '{target}' and PR_DATE <= '{date}' ORDER BY PR_DATE DESC LIMIT 1"
        cur.execute(query)
        cur_volume = cur.fetchall()[0][0]
        text = "check is lesstrade st."
    except Exception as e:
        text = "query: "+query + "error: "+str(e)
        writelog(text)
        assert e
    writelog(text)
    if cur_volume < x/100 * max_volume:
        ret = True
    return ret


def Pattern1(cur):
    text = "starting find pattern 1... \n step 1 find min start"
    writelog(text)
    store_min_values , store_min_date = finmin(cur, "ch6111")
    text = "step2 find_five_percent start..."
    writelog(text)
    target_list = find_five_percent(cur, store_min_values , store_min_date )
    flags = [False for _ in range(len(target_list))]
    text = "step2 find_five_percent finish..  step 3.  find reverse"
    writelog(text)
    for i ,target in enumerate(target_list):
        d_20ma = getTodayNma(cur,  target , n = 20, table = "ch6111")[0]
        d_60ma = getTodayNma(cur,  target , n = 60, table = "ch6111")[0]
        if d_60ma <= d_20ma:
            continue
        w_20ma = getTodayNma(cur,  target , n = 20, table = "ch6121")[0]
        w_60ma = getTodayNma(cur,  target , n = 60, table = "ch6121")[0]
        if w_60ma <= w_20ma:
            continue
        m_20ma = getTodayNma(cur,  target , n = 20, table = "ch6131")[0]
        m_60ma = getTodayNma(cur,  target , n = 60, table = "ch6131")[0]
        if m_60ma <= m_20ma:
            continue
        flags[i] = True
    Pattern1_list = []
    for i, flag in enumerate(flags):
        if flag:
            Pattern1_list.append(target_list[i])
    
    text = "finishing find pattern 1... "
    writelog(text, finish = True)
    return Pattern1_list


def Pattern2(cur):
    text = "starting find pattern 2... \n step 1 find min start"
    writelog(text)
    today = get_today()
    today = "20220318"
    fivedaylist = get_recent_tradingday(cur, today, 5)
    query = f"SELECT SEC_CD_S FROM history.ch6111 WHERE pr_date = '{today}';"
    cur.execute(query)
    target_list = cur.fetchall()
    target_list = [x[0] for x in target_list]
    Pattern2_list = []
    possible_list = []
    for target in target_list:
        isfound = True
        try:
            for date in fivedaylist:
                query = f"SELECT LOW FROM history.ch6111 WHERE pr_date = '{date}' AND SEC_CD_S = '{target}';"
                cur.execute(query)
                low = cur.fetchall()[0][0]
                d_20ma = getPastNma(cur, date, target , n = 20, table = "ch6111")[0]
                d_60ma = getPastNma(cur, date,  target , n = 60, table = "ch6111")[0]
                if d_60ma <= d_20ma or low < d_60ma or low < d_20ma:
                    isfound = False
                    break
                w_20ma = getPastNma(cur, date,  target , n = 20, table = "ch6121")[0]
                w_60ma =getPastNma(cur,  date, target , n = 60, table = "ch6121")[0]
                if w_60ma <= w_20ma or low < w_60ma or low < w_20ma:
                    isfound = False
                    break
                m_20ma = getPastNma(cur,  date, target , n = 20, table = "ch6131")[0]
                m_60ma = getPastNma(cur,  date, target , n = 60, table = "ch6131")[0]
                if m_60ma <= m_20ma or low < m_60ma or low < m_20ma:
                    isfound = False
                    break
        except Exception as e:
            text = "query: "+query + "error: "+str(e)
            writelog(text)
        if isfound:
            possible_list.append(target)
    for possible in possible_list:
        if islesstrade(cur, possible, today, n =20,  x = 30, type = "w"):
            Pattern2_list.append(possible)
    print(Pattern2_list)
    return Pattern2_list

def Pattern3(cur):
    text = "Start finding pattern3"
    today = get_today()
    writelog(text)
    today = "20220617"
    target_list = gettargetlist(cur)
    Pattern3_list = [] 
    try:
        for target in target_list:
            query = f"SELECT close FROM HISTORY.ch6131 WHERE SEC_CD_S = '{target}' AND PR_DATE <= '{today}' ORDER BY PR_DATE DESC LIMIT 1"
            cur.execute(query)
            m_close = cur.fetchall()[0][0]
            m_60ma =  getPastNma(cur,  today, target , n = 60, table = "ch6131")[0]
            isreverse = False
            if m_60ma > m_close:
                m_20ma =  getPastNma(cur,  today, target , n = 20, table = "ch6131")[0]
                if m_20ma < m_60ma:
                    w_60ma =  getPastNma(cur,  today, target , n = 60, table = "ch6121")[0]
                    w_20ma =  getPastNma(cur,  today, target , n = 20, table = "ch6121")[0]
                    if w_20ma < w_60ma:
                        isreverse = True
            if isreverse:
                if islesstrade(cur, target, today, n = 20, x = 30):
                    Pattern3_list.append(target)
    except Exception as e:
        text = "query: "+query + "error: "+str(e)
        writelog(text)

    return Pattern3_list

def Pattern4(cur):
    text = "Start finding pattern3"
    writelog(text)
    today = get_today()
    target_list = gettargetlist(cur)
    Pattern4_list = [] 
    target_list = ['362320']
    try: 
        for target in target_list:
            m_60ma =  getPastNma(cur,  today, target , n = 60, table = "ch6131")[0]
            m_20ma =  getPastNma(cur,  today, target , n = 20, table = "ch6131")[0]
            query = f"SELECT CLOSE FROM history.ch6131 WHERE SEC_CD_S = '{target}' ORDER BY PR_DATE DESC LIMIT 1"
            cur.execute(query)
            if target == '362320':
                print(1)
            try:
                m_close = cur.fetchall()[0][0]
            except:
                continue
            if not islesstrade(cur, target, today, n=20, x = 30):
                continue

            if m_60ma > m_close and m_close > m_20ma:
                w_60ma =  getPastNma(cur,  today, target , n = 60, table = "ch6121")[0]
                w_20ma =  getPastNma(cur,  today, target , n = 20, table = "ch6121")[0]
                query = f"SELECT CLOSE FROM history.ch6121 WHERE SEC_CD_S = '{target}' ORDER BY PR_DATE DESC LIMIT 1"
                cur.execute(query)
                try:
                    w_close = cur.fetchall()[0][0]
                except:
                    continue
                query = f"SELECT HIGH FROM history.ch6131 WHERE SEC_CD_S = '{target}' ORDER BY PR_DATE DESC LIMIT 1"
                cur.execute(query)
                try:
                    m_high = cur.fetchall()[0][0]
                except:
                    continue
                if w_close > w_60ma and m_high >= m_60ma:
                    query = f"SELECT HIGH FROM history.ch6121 WHERE SEC_CD_S = '{target}' ORDER BY PR_DATE DESC LIMIT 1"
                    cur.execute(query)
                    try:
                        w_high = cur.fetchall()[0][0]
                    except:
                        continue
                    query = f"SELECT LOW FROM history.ch6121 WHERE SEC_CD_S = '{target}' ORDER BY PR_DATE DESC LIMIT 1"
                    cur.execute(query)
                    try:
                        w_low = cur.fetchall()[0][0]
                    except:
                        continue
                    if (w_20ma > w_high and  w_high >  w_60ma) or (w_20ma > w_low and  w_low > w_60ma):
                        if w_close > w_20ma and abs(w_close - w_20ma) < w_close * 0.1:
                            Pattern4_list.append(target)
    except Exception as e:
        text = "query: "+query + "error: "+str(e)
        writelog(text)
        print(e)
        assert e
    return Pattern4_list



def Pattern4_1(cur):
    pass



try:
    conn = pymysql.connect(host="124.198.124.188", user="root", password="fmsoft1004",
                           db="history", charset="utf8")  # 1. DB 연결
except Exception as e:
    print(e)
    assert e
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
#make1(cur, "ch6130", "ch6131")
#getNma(cur,  id = "000020", n = 20, where = "ch6110")
#store_min_values , store_min_date = finmin(cur)
plist = Pattern3(cur)
print(plist)
try:
    cur.close()
except Exception as e:
    print(e)
    pass
#target_list = find_five_percent(cur, store_min_values, store_min_date)
#print(target_list)
try:
    conn.close() # 6. DB 닫기 (=연결 해제)
except Exception as e:
    print(e)
#print(store_min_values)
print('OK~')

