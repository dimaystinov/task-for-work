import datetime

from polygon import RESTClient

AVERAGE_COUNT_BORDER = 20


def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%H:%M')


def main():
    key = "AKNIY7PPQMMYHWCISCX3"
    all_elements = []
    all_element_average = []

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        from_ = "2019-01-01"
        to = "2019-02-01"
        ticker = 'WAB'
        resp = client.stocks_equities_aggregates(ticker, 1, "minute", from_, to, unadjusted=False)

        # print(f"Minute aggregates for {resp.ticker} between {from_} and {to}.")
        # print(resp.results)
        for result in resp.results:
            dt = ts_to_datetime(result["t"])
            #    print(f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
            element = [dt, [result['o'], result['h'], result['l'], result['c']]]
            all_elements.append(element)
            element_average = [dt, (result['o'] + result['c']) / 2]
            all_element_average.append(element_average)

    return all_element_average


list_of_element = main()
print(list_of_element)

count = 0
list_processing = []
for i in list_of_element:
    list_processing.append(i[1])
    average = sum(list_processing) / len(list_processing)
