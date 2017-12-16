# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httplib
import sys
import urllib

from bs4 import BeautifulSoup
from datetime import date, timedelta
import time

FIRST_DATE = date(2017, 12, 01)  # year, month, day
LAST_DATE = date(2017, 12, 18)
ONE_DAY = timedelta(days=1)


def main():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    httpClient = None

    try:
        httpClient = httplib.HTTPConnection('www.taifex.com.tw')

        d = FIRST_DATE

        with open('output.txt', 'w') as f:

            while d <= LAST_DATE:

                params = urllib.urlencode({
                    'qtype': 2,
                    'commodity_id': 'TXO',
                    'commodity_id2': '',
                    'market_code': 1,
                    'goday': '',
                    'dateaddcnt': 0,
                    'DATA_DATE_Y': d.year,
                    'DATA_DATE_M': d.month,
                    'DATA_DATE_D': d.day,
                    'syear': d.year,
                    'smonth': d.month,
                    'sday': d.day,
                    'datestart': '%s / %s / %s' % (d.year, d.month, d.day),
                    'MarketCode': 1,
                    'commodity_idt': 'TXO',
                    'commodity_id2t': '',
                    'commodity_id2t2': '',
                })

                print 'Request %s/%s/%s' % (d.year, d.month, d.day)

                httpClient.request('POST', '/chinese/3/3_2_2.asp', params)

                response = httpClient.getresponse()

                if response.status == 200:
                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    table = soup.find('table', class_='table_c')

                    if table:
                        f.write('%s,%s,%s\n' % (d.year, d.month, d.day))
                        for tr in table.find_all('tr')[1:]:
                            output = []
                            for td in tr.find_all('td'):
                                data = td.string.strip() if td.string else ''
                                output.append(data)

                            f.write(','.join(output) + '\n')
                        f.write('\n')

                d += ONE_DAY

                time.sleep(2) # sleep 2 sec to avoid server ban

    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()


if __name__ == '__main__':
    main()
