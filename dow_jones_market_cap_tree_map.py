from urllib import response
# tree map of 30 largest Dow Jones companies by market cap
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import squarify

url = "https://companiesmarketcap.com/dow-jones/largest-companies-by-market-cap/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "lxml")

# parse to get table containing company information (rows)
rows = soup.findChildren("tr")

symbols = []
market_caps = []  # market cap text
sizes = []  # market cap numerical data

for row in rows:
    try:
        symbol = row.find("div", {"class": "company-code"}).text
        # market cap is 3rd col of table
        market_cap = row.findAll('td')[2].text
        symbols.append(symbol)
        market_caps.append(market_cap)

        # formatting
        if market_cap.endswith("T"):
            sizes.append(float(market_cap[1:-2])
                         * 10 ** 12)  # use * to get $tn
        elif market_cap.endswith("B"):
            sizes.append(float(market_cap[1:-2]) * 10 ** 9)  # use * to get $tn
    # have empty list in first row
    except AttributeError:
        pass

# want symbol in each "square" and market cap below in ()
labels = [f"{symbols[i]}\n({market_caps[i]})" for i in range(len(symbols))]

# colour map
# tab20c is a built in colour map
colors = [plt.cm.tab20c(i/float(len(symbols))) for i in range(len(symbols))]

squarify.plot(sizes=sizes, label=labels, color=colors,
              bar_kwargs={"linewidth": 0.5, "edgecolor": "#111"})

figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

plt.show()
