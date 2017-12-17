# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httplib
import urllib

from bs4 import BeautifulSoup
from datetime import date, timedelta
import time

FIRST_DATE = date(2017, 12, 14)  # year, month, day
LAST_DATE = date(2017, 12, 18)

ONE_DAY = timedelta(days=1)

MARKET_CODE_NORMAL = 0
MARKET_CODE_AFTER_HOURS = 1


def main():

    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain',
    }

    httpClient = None

    try:
        httpClient = httplib.HTTPConnection('www.taifex.com.tw')

        d = FIRST_DATE

        with open('output.csv', 'w') as f:

            while d <= LAST_DATE:

                params = urllib.urlencode({
                    'qtype': 3,
                    'commodity_id': 'TXO',
                    'commodity_id2': '',
                    'market_code': MARKET_CODE_NORMAL,
                    'goday': '',
                    'dateaddcnt': 0,
                    'DATA_DATE_Y': d.year,
                    'DATA_DATE_M': d.month,
                    'DATA_DATE_D': d.day,
                    'syear': d.year,
                    'smonth': d.month,
                    'sday': d.day,
                    'datestart': '%s/%s/%s' % (d.year, d.month, d.day),
                    'MarketCode': MARKET_CODE_NORMAL,
                    'commodity_idt': 'TXO',
                    'commodity_id2t': '',
                    'commodity_id2t2': '',
                })

                print 'Request %s/%s/%s' % (d.year, d.month, d.day)

                httpClient.request('POST', '/chinese/3/3_2_2.asp', params, headers)

                response = httpClient.getresponse()

                if response.status == 200:
                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    table = soup.find('table', class_='table_c')

                    if table:
                        f.write(b'%s,%s,%s\n' % (d.year, d.month, d.day))
                        for tr in table.find_all('tr')[1:]:
                            output = []
                            for td in tr.find_all('td'):
                                element = td
                                if td.font:
                                    element = td.font

                                data = element.string.strip() if element.string else ''
                                output.append(data)

                            f.write(
                                (','.join(output) + '\n').encode('big5')
                            )
                        f.write(b'\n')

                d += ONE_DAY

                time.sleep(2) # sleep 2 sec to avoid server ban

    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()


if __name__ == '__main__':
    main()
