import requests
import json
import time
import csv

start_time = time.time()
per_page = 2000


def tick(page):
    global per_page
    return 'https://api.polygon.io/v2/reference/tickers?sort=ticker&market=stocks&perpage={0}&page={' \
           '1}&apiKey=AKNIY7PPQMMYHWCISCX3'.format(
        str(per_page), str(
            page))


go = []

response1 = requests.get(tick(1))
response_dict1 = json.loads(response1.text)
count = response_dict1['count']


def all_tickets(j):
    global go
    response = requests.get(tick(j))
    response_dict = json.loads(response.text)
    tickers = response_dict['tickers']
    for item in tickers:
        go.append(
            {'ticker': item['ticker'], 'name': item['name'], 'locale': item['locale'], 'currency': item['currency']})


amount = count // per_page

for i in range(amount+1):
    try:
        all_tickets(i)
    except:
        print("Error")

'''for i in go:
    print(i)'''
print(len(go))

with open('mycsvfile.csv', 'w') as f:
    w = csv.DictWriter(f, go[0].keys())
    w.writeheader()
    for item in go:
        w.writerow(item)

print("--- %s seconds ---" % (time.time() - start_time))
