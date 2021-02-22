import datetime

from polygon import RESTClient

import pandas as pd
import csv


def ts_to_datetime(ts) -> str:
    return [int(i) for i in datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%d %H %M').split()]


def main(ticker):
    key = "AKNIY7PPQMMYHWCISCX3"

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        from_ = "2021-02-01"
        to = "2021-02-12"

        resp = client.stocks_equities_aggregates(ticker, 1, "minute", from_, to, unadjusted=False)
        # print(f"Minute aggregates for {resp.ticker} between {from_} and {to}.")
        # print(resp.results)
        all_elements = []
        all_element_average = []
        for result in resp.results:
            dt = ts_to_datetime(result["t"])
            #    print(f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
            element = [dt, [result['o'], result['h'], result['l'], result['c']]]
            if 4 <= dt[1] <= 19:
                all_elements.append(element)
                element_average = [dt, result['o'], result['c'], (result['o'] + result['c']) / 2]
                all_element_average.append(element_average)

        list_of_element = all_element_average

        count = 0
        list_processing = []
        for count, i in enumerate(list_of_element):
            list_processing.append(i[3])
            if count >= 21:
                moving_average = []
                for j in range(20):
                    moving_average.append(list_processing[count - j - 1])
                average = sum(moving_average) / len(moving_average)
                list_of_element[count].append(average)
        return list_of_element

if __name__ == '__main__':


    data_csv = pd.read_csv('mycsvfile.csv', delimiter=',')
    all_name_ticker = data_csv.ticker
    c = 0
    legal = []
    illegal = []
    for ticker in all_name_ticker:
        try:
            main(ticker)
            print(ticker)
            legal.append(ticker)
        except:
            c += 1
            print(c, ticker)
            illegal.append(ticker)



    with open('legal.csv', 'w') as f:
        writer = csv.writer(f)
        for val in legal:
            writer.writerow([val])
        writer.writerow([len(legal)])

    with open('illegal.csv', 'w') as f:
        writer = csv.writer(f)
        for val in illegal:
            writer.writerow([val])
        writer.writerow([len(illegal)])





