import datetime

from collections import defaultdict

import requests

from bs4 import BeautifulSoup

#ty11x5 = 'http://tubiao.zhcw.com/tubiao/tianJing/11x5/11x5Jsp/11x5static.jsp?url=11x5.jsp'

def get_numbers(start_dt, end_dt):
    '''
    startTime=19010690&endTime=19010729
    '''
    ty11x5 = 'http://tubiao.zhcw.com/tubiao//tianJing/11x5//11x5Jsp/11x5static.jsp?url=11x5.jsp&startTime={0}&endTime={1}'
    print(ty11x5.format(start_dt,end_dt))
    r = requests.get(ty11x5.format(start_dt,end_dt))
    soup = BeautifulSoup(r.text,'lxml')
    tables = soup.findAll('table')
    tab = tables[0]
    rec = defaultdict(list)
    for tr in tab.findAll('tr'):
        for td in tr.findAll('td'):
            if "bd_ft" in td.attrs.get("class",[]):
                cur_issue = td.contents[0].text
            if "td_bc1" in td.attrs.get("class",[]):
                rec[cur_issue].append(td.text.strip())
    return rec

def fetch_history(
    start_dt = datetime.datetime(2019,1,6),
    end_dt = datetime.datetime(2019,1,7)
    ):
    cur_dt = start_dt
    all_res = {}
    while cur_dt <= end_dt:
        all_res.update(get_numbers(cur_dt.strftime("%y%m%d01"), cur_dt.strftime("%y%m%d90")))
        cur_dt += datetime.timedelta(days=1)
    return all_res